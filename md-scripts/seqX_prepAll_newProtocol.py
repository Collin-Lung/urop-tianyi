#!/usr/bin/env python

import os
import subprocess
import sys
import shutil

sequenceNumber = sys.argv[1]
sequenceString = sys.argv[2]

title = f"seq{sequenceNumber}"
sequence = sequenceString
folder = f"seq{sequenceNumber}"
dt = 0.002
#For the equilibration:
eqT = 500
timeEq1 = 2
timeEq2 = 18
#For the anneallling:
initialT = 500
highT1 = 500
lowT1 = 300
timeHold = 20
timeCool1 = 40

#Calculations
nstepsEq1 = int((timeEq1 * 1000) / dt)
nstepsEq2 = int((timeEq2 * 1000) / dt)
nstepsHold = int((timeHold * 1000) / dt)
nstepsCool1 = int((timeCool1 * 1000) / dt)

os.mkdir(folder)
os.chdir(folder)
subprocess.run(["cp", "/pool/tianyi/Backbone_p5_M/includes/*", "."])
os.environ["AMBERHOME"] = "/pool/shared/amber18"

with open(f"tleap_{title}_pre.in", "w") as file:
    file.write(
        f"""\
source leaprc.gaff
"""
    )
    with open("tleapLoad.txt", "r") as load_file:
        file.write(load_file.read())
    file.write(
        f"""\
mol = sequence {{{sequence}}}
savepdb mol {title}_chain.pdb
setbox mol "vdw" 5
saveamberparm mol {title}_pre.parm7 {title}_pre.rst7
quit
"""
    )
subprocess.run(["tleap", "-s", "-f", f"tleap_{title}_pre.in"], stdout=subprocess.PIPE)

with open(f"rotate_{title}_pre.in", "w") as file:
    file.write(
        f"""\
parm {title}_pre.parm7
trajin {title}_pre.rst7
principal dorotation
trajout {title}_pre_rotated.pdb
"""
    )
subprocess.run(["cpptraj", "-i", f"rotate_{title}_pre.in"], stdout=subprocess.PIPE)

with open(f"tleap_{title}_1.in", "w") as file:
    file.write(
        f"""\
source leaprc.gaff
"""
    )
    with open("tleapLoad.txt", "r") as load_file:
        file.write(load_file.read())
    file.write(
        f"""\
mol = loadpdb {title}_pre_rotated.pdb
savepdb mol {title}_pdb_1.pdb
setbox mol "vdw" 5
saveamberparm mol {title}_1.parm7 {title}_1.rst7
quit
"""
    )

shutil.copy("nvt_heat_igb.in", f"{title}_nvt_heat_1.in")
shutil.copy("eq_igb.in", f"{title}_eq_1.in")
shutil.copy("production_igb.in", f"{title}_production_1.in")
shutil.copy("anneal_holdCool_igb.in", f"{title}_anneal_1.in")

with open(f"{title}_nvt_heat_1.in", "r+") as file:
    content = file.read()
    content = content.replace("TEMPERATURE", str(eqT))
    file.seek(0)
    file.write(content)
    file.truncate()

with open(f"{title}_eq_1.in", "r+") as file:
    content = file.read()
    content = content.replace("TEMPERATURE", str(eqT))
    content = content.replace("NSTEPS", str(nstepsEq1))
    file.seek(0)
    file.write(content)
    file.truncate()

with open(f"{title}_production_1.in", "r+") as file:
    content = file.read()
    content = content.replace("TEMPERATURE", str(eqT))
    content = content.replace("NSTEPS", str(nstepsEq2))
    file.seek(0)
    file.write(content)
    file.truncate()

#anneal
with open(f"{title}_anneal_1.in", "r+") as file:
    content = file.read()
    content = content.replace(
        "NSTEPS", str(nstepsHold + nstepsCool1)
    ).replace("INITIALT", str(initialT)).replace(
        "CHANGESTEP1", str(nstepsHold)
    ).replace(
        "CHNGSTEP1PLUS", str(nstepsHold + 1)
    ).replace(
        "HIGHT1", str(highT1)
    ).replace(
        "LOWT1", str(lowT1)
    ).replace(
        "CHANGESTEP2", str(nstepsHold + nstepsCool1)
    )
    file.seek(0)
    file.write(content)
    file.truncate()


#Launch scripts:
with open("launch_minsCPU.sh", "w") as file:
    file.write(
        f"""\
#!/bin/bash
#SBATCH -J {title}_cpu
#SBATCH -o {title}_slurmoutput_minsCPU.out
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -p regular-cpu
#SBATCH --exclude=node[107,113-114,117-118,122,126,135,137,141,151,154,171,173,213]
export AMBERHOME=/pool/shared/amber18
source $AMBERHOME/amber.sh
tleap -s -f tleap_{title}_1.in > tleap_{title}_1.out
mpirun -np 8 -mca btl ^openib $AMBERHOME/bin/pmemd.MPI -O -i min.in -o {title}_min_1.out -p {title}_1.parm7 -c {title}_1.rst7 -r {title}_min_1.rst -inf min1info
mpirun -np 8 -mca btl ^openib $AMBERHOME/bin/pmemd.MPI -O -i min_igb.in -o {title}_min_igb_1.out -p {title}_1.parm7 -c {title}_min_1.rst -r {title}_min_igb_1.rst -inf minigb1info
"""
    )

with open("launch_EqProd_1.sh", "w") as file:
    file.write(
        f"""\
#!/bin/bash
#SBATCH -J {title}_eqprod_1
#SBATCH -o {title}_slurmoutput_EqProd_1.out
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --gres=gpu:1
export CUDA_HOME=/usr/local/cuda-10.1
export AMBERHOME=/workGPU/shared/amber18
source $AMBERHOME/amber.sh
$AMBERHOME/bin/pmemd.cuda -O -i {title}_nvt_heat_1.in -o {title}_nvt_heat_1.out -p {title}_1.parm7 -c {title}_min_igb_1.rst -r {title}_nvt_heat_1.rst -x {title}_nvt_heat_1.nc -inf nvtheat1info
$AMBERHOME/bin/pmemd.cuda -O -i {title}_eq_1.in -o {title}_eq_1.out -p {title}_1.parm7 -c {title}_nvt_heat_1.rst -r {title}_eq_1.rst -x {title}_eq_1.nc -inf eq1info
$AMBERHOME/bin/pmemd.cuda -O -i {title}_production_1.in -o {title}_production_1.out -p {title}_1.parm7 -c {title}_eq_1.rst -r {title}_production_1.rst -x {title}_production_1.nc -inf production1inf
"""
    )

with open("launch_anneal.sh", "w") as file:
    file.write(
        f"""\
#!/bin/bash
#SBATCH -J {title}_anneal
#SBATCH -o {title}_slurmoutput_anneal.out
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --gres=gpu:1
export CUDA_HOME=/usr/local/cuda-10.1
export AMBERHOME=/workGPU/shared/amber18
source $AMBERHOME/amber.sh
$AMBERHOME/bin/pmemd.cuda -O -i {title}_anneal_1.in -o {title}_anneal_1.out -p {title}_1.parm7 -c {title}_production_1.rst -r {title}_anneal_1.rst -x {title}_anneal_1.nc -inf anneal1inf
"""
    )

with open("launch_full1.sh", "w") as file:
    file.write(
        f"""\
job1=$(sbatch launch_minsCPU.sh)
jid1=$(echo ${{job1}} | awk '{{print $4}}')
"""
    )

#####move to GPU
with open("launch_full1_5.sh", "w") as file:
    file.write(
        f"""\
job2=$(sbatch launch_EqProd_1.sh)
jid2=$(echo ${{job2}} | awk '{{print $4}}')
job3=$(sbatch --dependency=afterok:$jid2 launch_anneal.sh)
"""
    )


