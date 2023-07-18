import subprocess
import sys
import os

sequenceNumber = sys.argv[1]

title = f"seq{sequenceNumber}"
folder = f"seq{sequenceNumber}"
dt = 0.002
angstromsWat = 50  # 16 angstroms was what it used to be in the old protocol
rhpRes = 100
keepWats = 40000
# For the equilibration:
eqT = 300
timeEq = 2
# Heat/cool
T1 = 650
T2 = 650
T3 = 475
T4 = 300
timeHold = 20
timeCool1 = 20
timeCool2 = 20
# Production to reequilibrate then record data
prodT = 300
timeProd1 = 20
timeProd2 = 20
timeProd3 = 20
# Calculations
nstepsEq = int((timeEq * 1000) / dt)
nsteps1 = int((timeHold * 1000) / dt)
nsteps2 = int((timeCool1 * 1000) / dt)
nsteps3 = int((timeCool2 * 1000) / dt)
nstepsProd1 = int((timeProd1 * 1000) / dt)
nstepsProd2 = int((timeProd2 * 1000) / dt)
nstepsProd3 = int((timeProd3 * 1000) / dt)

subprocess.run(["cd", folder])
subprocess.run(["scp", f"qhe@txe1-login.mit.edu:/home/gridsan/qhe/Backbone_p5_M/{folder}/*anneal*rst", "."])
subprocess.run(["rm", "-r", "explicit_protocol"])
subprocess.run(["mkdir", "explicit_protocol"])
subprocess.run(["cd", "explicit_protocol"])
subprocess.run(["cp", "/pool/tianyi/Backbone_p5_D/includes/*", "."])
os.environ["AMBERHOME"] = "/pool/shared/amber18"
subprocess.run(["source", "/pool/shared/amber18/amber.sh"])

# Make input files
subprocess.run(["cp", "nvt_heat.in", f"{title}_nvt_heat_exp.in"])
subprocess.run(["cp", "eq.in", f"{title}_eq_exp.in"])
subprocess.run(["cp", "nvt_t1t2.in", f"{title}_nvt_t1t2_exp_12.in"])
subprocess.run(["cp", "nvt_t1t2.in", f"{title}_nvt_t1t2_exp_23.in"])
subprocess.run(["cp", "nvt_t1t2.in", f"{title}_nvt_t1t2_exp_34.in"])
subprocess.run(["cp", "production.in", f"{title}_production1_exp.in"])
subprocess.run(["cp", "production.in", f"{title}_production2_exp.in"])

# Modify input files
# eq
subprocess.run(["sed", "-i", "-e", f"s/TEMPERATURE/{eqT}/g", f"{title}_nvt_heat_exp.in"])
subprocess.run(["sed", "-i", "-e", f"s/TEMPERATURE/{eqT}/g", f"{title}_eq_exp.in"])
subprocess.run(["sed", "-i", "-e", f"s/NSTEPS/{nstepsEq}/g", f"{title}_eq_exp.in"])
# quickanneal
subprocess.run(["sed", "-i", "-e", f"s/NSTEPS/{nsteps1}/g", f"{title}_nvt_t1t2_exp_12.in"])
subprocess.run(["sed", "-i", "-e", f"s/T1/{T1}/g", f"{title}_nvt_t1t2_exp_12.in"])
subprocess.run(["sed", "-i", "-e", f"s/T2/{T2}/g", f"{title}_nvt_t1t2_exp_12.in"])
subprocess.run(["sed", "-i", "-e", f"s/NSTEPS/{nsteps2}/g", f"{title}_nvt_t1t2_exp_23.in"])
subprocess.run(["sed", "-i", "-e", f"s/T1/{T2}/g", f"{title}_nvt_t1t2_exp_23.in"])
subprocess.run(["sed", "-i", "-e", f"s/T2/{T3}/g", f"{title}_nvt_t1t2_exp_23.in"])
subprocess.run(["sed", "-i", "-e", f"s/NSTEPS/{nsteps3}/g", f"{title}_nvt_t1t2_exp_34.in"])
subprocess.run(["sed", "-i", "-e", f"s/T1/{T3}/g", f"{title}_nvt_t1t2_exp_34.in"])
subprocess.run(["sed", "-i", "-e", f"s/T2/{T4}/g", f"{title}_nvt_t1t2_exp_34.in"])
# production
subprocess.run(["sed", "-i", "-e", f"s/TEMPERATURE/{prodT}/g", f"{title}_production1_exp.in"])
subprocess.run(["sed", "-i", "-e", f"s/NSTEPS/{nstepsProd1}/g", f"{title}_production1_exp.in"])
subprocess.run(["sed", "-i", "-e", f"s/TEMPERATURE/{prodT}/g", f"{title}_production2_exp.in"])
subprocess.run(["sed", "-i", "-e", f"s/NSTEPS/{nstepsProd2}/g", f"{title}_production2_exp.in"])

# FOR THIS IGB ANNEAL, (1 through 10), do the explicit thing:
for i in range(1, 11):
    # Extract the last frame
    subprocess.run(["rm", f"{title}_extract_{i}.in"])
    with open(f"{title}_extract_{i}.in", "w") as file:
        file.write(f"parm ../{title}_1.parm7\n")
        file.write(f"trajin ../{title}_anneal_{i}.rst lastframe\n")
        file.write(f"trajout {title}_extracted_{i}.pdb\n")
    subprocess.run(["$AMBERHOME/bin/cpptraj", "-i", f"{title}_extract_{i}.in", "&>", f"extract_{i}.log"])

    # Solvate it
    with open(f"tleap_{title}_solvate_{i}.in", "w") as file:
        file.write("source leaprc.gaff\n")
        subprocess.run(["grep", "load", "tleapLoad.txt"], stdout=file)
        file.write(f"source leaprc.water.spce\n")
        file.write(f"mol = loadpdb {title}_extracted_{i}.pdb\n")
        file.write(f"solvateOct mol SPC {angstromsWat}\n")
        file.write("addionsRand mol K+ 0.0\n")
        file.write(f"savepdb mol {title}_{i}_solvated.pdb\n")
        file.write(f"saveamberparmmol {title}_exp_waters_{i}.parm7 {title}_exp_waters_{i}.rst7")

    #prep script
    subprocess.run(["export", f"AMBERHOME=/pool/shared/amber18"])
    subprocess.run(["source", f"/pool/shared/amber18/amber.sh"])
    subprocess.run(["echo", f"{angstromsWat}", ">>", f"record_angstromsWat_{i}.txt"])
    subprocess.run(
        ["$AMBERHOME/bin/tleap", "-s", "-f", f"tleap_{title}_solvate_{i}.in", ">", f"tleap_{title}_solvate_{i}.out"])

    while True:
        lastRes = subprocess.run(["grep", "WAT", f"{title}_{i}_solvated.pdb"],
                                 stdout=subprocess.PIPE).stdout.decode().strip().split()[-1]
        lastRes = int(lastRes) if lastRes.isdigit() else 0

        gtVal = float(rhpRes) + 1.1 * float(keepWats)
        gtInt = int(gtVal)
        if lastRes > gtInt:
            subprocess.run(["sed", "-i", "-e", f"s/solvateOct mol SPC {angstromsWat}/solvateOct mol SPC temp/g",
                            f"tleap_{title}_solvate_{i}.in"])
            angstromsWat *= 0.9
            subprocess.run(["echo", f"{angstromsWat}", ">>", f"record_angstromsWat_{i}.txt"])
            subprocess.run(["sed", "-i", "-e", f"s/solvateOct mol SPC temp/solvateOct mol SPC {angstromsWat}/g",
                            f"tleap_{title}_solvate_{i}.in"])
            subprocess.run(["$AMBERHOME/bin/tleap", "-s", "-f", f"tleap_{title}_solvate_{i}.in", ">",
                            f"tleap_{title}_solvate_{i}.out"])
            lastRes = subprocess.run(["grep", "WAT", f"{title}_{i}_solvated.pdb"],
                                     stdout=subprocess.PIPE).stdout.decode().strip().split()[-1]
            lastRes = int(lastRes) if lastRes.isdigit() else 0
        else:
            break

    while True:
        lastRes = subprocess.run(["grep", "WAT", f"{title}_{i}_solvated.pdb"],
                                 stdout=subprocess.PIPE).stdout.decode().strip().split()[-1]
        lastRes = int(lastRes) if lastRes.isdigit() else 0

        ltVal = float(rhpRes) + float(keepWats)
        ltInt = int(ltVal)
        if lastRes < ltInt:
            subprocess.run(["sed", "-i", "-e", f"s/solvateOct mol SPC {angstromsWat}/solvateOct mol SPC temp/g",
                            f"tleap_{title}_solvate_{i}.in"])
            angstromsWat *= 1.1
            subprocess.run(["echo", f"{angstromsWat}", ">>", f"record_angstromsWat_{i}.txt"])
            subprocess.run(["sed", "-i", "-e", f"s/solvateOct mol SPC temp/solvateOct mol SPC {angstromsWat}/g",
                            f"tleap_{title}_solvate_{i}.in"])
            subprocess.run(["$AMBERHOME/bin/tleap", "-s", "-f", f"tleap_{title}_solvate_{i}.in", ">",
                            f"tleap_{title}_solvate_{i}.out"])
            lastRes = subprocess.run(["grep", "WAT", f"{title}_{i}_solvated.pdb"],
                                     stdout=subprocess.PIPE).stdout.decode().strip().split()[-1]
            lastRes = int(lastRes) if lastRes.isdigit() else 0
        else:
            break

    firstStrip = int(float(rhpRes) + float(keepWats) + 1)
    adjustwaters_input = f"""
    parm {title}_exp_waters_{i}.parm7
    loadRestrt {title}_exp_waters_{i}.rst7
    strip :{firstStrip}-{lastRes}
    outparm {title}_exp_{i}.parm7 {title}_exp_{i}.rst7
    """
    with open(f"adjustwaters_{title}_{i}.in", "w") as file:
        file.write(adjustwaters_input)
    subprocess.run(
        ["$AMBERHOME/bin/parmed", "-i", f"adjustwaters_{title}_{i}.in", ">", f"adjustwaters_{title}_{i}.out"])

    # Launch script: launch_min_${i}.sh
    with open(f"launch_min_{i}.sh", "w") as file:
        file.write(f"""#!/bin/bash
    #SBATCH -J {title}_min_{i}
    #SBATCH -o {title}_slurmoutput_min_{i}.out
    #SBATCH -N 1
    #SBATCH -n 8
    #SBATCH -p regular-cpu
    export AMBERHOME=/pool/shared/amber18
    source /pool/shared/amber18/amber.sh
    mpirun -np 8 -mca btl ^openib /pool/shared/amber18/bin/pmemd.MPI -O -i min.in -o {title}_min_exp_{i}.out -p {title}_exp_{i}.parm7 -c {title}_exp_{i}.rst7 -r {title}_min_exp_{i}.rst -inf min_{i}inf
    mpirun -np 8 -mca btl ^openib /pool/shared/amber18/bin/pmemd.MPI -O -i {title}_nvt_heat_exp.in -o {title}_nvt_heat_exp_{i}.out -p {title}_exp_{i}.parm7 -c {title}_min_exp_{i}.rst -r {title}_nvt_heat_exp_{i}.rst -x {title}_nvt_heat_exp_{i}.nc -inf nvtheat_{i}info
    mpirun -np 8 -mca btl ^openib /pool/shared/amber18/bin/pmemd.MPI -O -i {title}_eq_exp.in -o {title}_eq_exp_{i}.out -p {title}_exp_{i}.parm7 -c {title}_nvt_heat_exp_{i}.rst -r {title}_eq_exp_{i}.rst -x {title}_eq_exp_{i}.nc -inf eq_{i}inf
    INPUT\n""")

    # Launch script: launch_anneal12_${i}.sh
    with open(f"launch_anneal12_{i}.sh", "w") as file:
        file.write(f"""#!/bin/bash
    #SBATCH -J {title}_anneal12_{i}
    #SBATCH -o {title}_slurmoutput_anneal12_{i}.out
    #SBATCH -N 1
    #SBATCH -n 1
    #SBATCH --gres=gpu:volta:1
    export AMBERHOME=/home/gridsan/tjin/amber18
    source /home/gridsan/tjin/amber18/amber.sh
    export CUDA_HOME=/usr/local/pkg/cuda/cuda-10.1
    /home/gridsan/tjin/amber18/bin/pmemd.cuda -O -i {title}_nvt_t1t2_exp_12.in -o {title}_nvt_t1t2_exp_12_{i}.out -p {title}_exp_{i}.parm7 -c {title}_eq_exp_{i}.rst -r {title}_nvt_t1t2_exp_12_{i}.rst -x {title}_nvt_t1t2_exp_12_{i}.nc -inf nvtanneal12_{i}inf
    INPUT\n""")

    # Launch script: launch_anneal23_${i}.sh
    with open(f"launch_anneal23_{i}.sh", "w") as file:
        file.write(f"""#!/bin/bash
    #SBATCH -J {title}_anneal23_{i}
    #SBATCH -o {title}_slurmoutput_anneal23_{i}.out
    #SBATCH -N 1
    #SBATCH -n 1
    #SBATCH --gres=gpu:volta:1
    export AMBERHOME=/home/gridsan/tjin/amber18
    source /home/gridsan/tjin/amber18/amber.sh
    export CUDA_HOME=/usr/local/pkg/cuda/cuda-10.1
    /home/gridsan/tjin/amber18/bin/pmemd.cuda -O -i {title}_nvt_t1t2_exp_23.in -o {title}_nvt_t1t2_exp_23_{i}.out -p {title}_exp_{i}.parm7 -c {title}_nvt_t1t2_exp_12_{i}.rst -r {title}_nvt_t1t2_exp_23_{i}.rst -x {title}_nvt_t1t2_exp_23_{i}.nc -inf nvtanneal23_{i}inf
    INPUT\n""")

    # Launch script: launch_anneal34_${i}.sh
    with open(f"launch_anneal34_{i}.sh", "w") as file:
        file.write(f"""#!/bin/bash
    #SBATCH -J {title}_anneal34_{i}
    #SBATCH -o {title}_slurmoutput_anneal34_{i}.out
    #SBATCH -N 1
    #SBATCH -n 1
    #SBATCH --gres=gpu:volta:1
    export AMBERHOME=/home/gridsan/tjin/amber18
    source /home/gridsan/tjin/amber18/amber.sh
    export CUDA_HOME=/usr/local/pkg/cuda/cuda-10.1
    /home/gridsan/tjin/amber18/bin/pmemd.cuda -O -i {title}_nvt_t1t2_exp_34.in -o {title}_nvt_t1t2_exp_34_{i}.out -p {title}_exp_{i}.parm7 -c {title}_nvt_t1t2_exp_23_{i}.rst -r {title}_nvt_t1t2_exp_34_{i}.rst -x {title}_nvt_t1t2_exp_34_{i}.nc -inf nvtanneal34_{i}inf
    INPUT\n""")

    # Launch script: launch_prod_${i}.sh
    with open(f"launch_prod_{i}.sh", "w") as file:
        file.write(f"""#!/bin/bash
    #SBATCH -J {title}_prod_{i}
    #SBATCH -o {title}_slurmoutput_prod_{i}.out
    #SBATCH -N 1
    #SBATCH -n 1
    #SBATCH --gres=gpu:volta:1
    export AMBERHOME=/home/gridsan/tjin/amber18
    source /home/gridsan/tjin/amber18/amber.sh
    export CUDA_HOME=/usr/local/pkg/cuda/cuda-10.1
    /home/gridsan/tjin/amber18/bin/pmemd.cuda -O -i {title}_production1_exp.in -o {title}_production1_exp_{i}.out -p {title}_exp_{i}.parm7 -c {title}_nvt_t1t2_exp_34_{i}.rst -r {title}_production1_exp_{i}.rst -x {title}_production1_exp_{i}.nc -inf prod1_{i}inf
    /home/gridsan/tjin/amber18/bin/pmemd.cuda -O -i {title}_production2_exp.in -o {title}_production2_exp_{i}.out -p {title}_exp_{i}.parm7 -c {title}_production1_exp_{i}.rst -r {title}_production2_exp_{i}.rst -x {title}_production2_exp_{i}.nc -inf prod2_{i}inf
    INPUT\n""")

    # Launch script: launch_prod3_${i}.sh
    with open(f"launch_prod3_{i}.sh", "w") as file:
        file.write(f"""#!/bin/bash
    #SBATCH -J {title}_prod3_{i}
    #SBATCH -o {title}_slurmoutput_prod3_{i}.out
    #SBATCH -N 1
    #SBATCH -n 1
    #SBATCH --gres=gpu:volta:1
    export AMBERHOME=/home/gridsan/tjin/amber18
    source /home/gridsan/tjin/amber18/amber.sh
    export CUDA_HOME=/usr/local/pkg/cuda/cuda-10.1
    /home/gridsan/tjin/amber18/bin/pmemd.cuda -O -i {title}_production2_exp.in -o {title}_production3_exp_{i}.out -p {title}_exp_{i}.parm7 -c {title}_production2_exp_{i}.rst -r {title}_production3_exp_{i}.rst -x {title}_production3_exp_{i}.nc -inf prod3_{i}inf
    INPUT\n""")

    # sbatch_script.sh
    with open("sbatch_script.sh", "a") as file:
        file.write(f"job0=$(sbatch launch_prep_{i}.sh)\n")
        file.write(f"jid0=$(echo ${{job0}} | awk '{{print $4}}')\n")
        file.write(f"job1=$(sbatch --dependency=afterok:$jid0 launch_min_{i}.sh)\n")
        file.write(f"jid1=$(echo ${{job1}} | awk '{{print $4}}')\n")

    # sbatch_script_GPU.sh
    with open("sbatch_script_GPU.sh", "a") as file:
        file.write(f"job2=$(sbatch launch_anneal12_{i}.sh)\n")
        file.write(f"jid2=$(echo ${{job2}} | awk '{{print $4}}')\n")
        file.write(f"job3=$(sbatch --dependency=afterok:$jid2 launch_anneal23_{i}.sh)\n")
        file.write(f"jid3=$(echo ${{job3}} | awk '{{print $4}}')\n")
        file.write(f"job4=$(sbatch --dependency=afterok:$jid3 launch_anneal34_{i}.sh)\n")
        file.write(f"jid4=$(echo ${{job4}} | awk '{{print $4}}')\n")
        file.write(f"job5=$(sbatch --dependency=afterok:$jid4 launch_prod_{i}.sh)\n")
        file.write(f"jid5=$(echo ${{job5}} | awk '{{print $4}}')\n")
        file.write(f"job6=$(sbatch --dependency=afterok:$jid5 launch_prod3_{i}.sh)\n")

    # Run sbatch_script.sh
    os.system("bash sbatch_script.sh")

    # Run sbatch_script_GPU.sh
    os.system("bash sbatch_script_GPU.sh")
