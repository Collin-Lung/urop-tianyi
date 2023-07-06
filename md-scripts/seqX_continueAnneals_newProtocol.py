#!/usr/bin/env python

import os
import subprocess
import sys

sequenceNumber = sys.argv[1]

title = f"seq{sequenceNumber}"
folder = f"seq{sequenceNumber}"
#timeHold=120
#timeProd=20
ncycles = 10  # 10 total cycles. This script starts #2 out of 10, so it queues up 9
os.chdir(folder)
os.environ["AMBERHOME"] = "/workGPU/shared/amber18"

# Perform necessary AMBER setup and simulation steps
for i in range(2, ncycles):
    b4 = str(i - 1)
    input_file = f"{title}_anneal_{i}.in"
    output_file = f"{title}_anneal_{i}.out"
    restart_file = f"{title}_anneal_{i}.rst"
    trajectory_file = f"{title}_anneal_{i}.nc"

    # Prepare input file for the current cycle
    with open(input_file, "w") as file:
        file.write(f"""
# AMBER input file for annealing cycle {i}
# Set simulation parameters here

""")

    # Run AMBER simulation
    subprocess.run(
        [
            "$AMBERHOME/bin/pmemd.cuda",
            "-O",
            "-i",
            input_file,
            "-o",
            output_file,
            "-p",
            f"{title}_1.parm7",
            "-c",
            f"{title}_anneal_{b4}.rst",
            "-r",
            restart_file,
            "-x",
            trajectory_file,
            "-inf",
            f"anneal{i}inf",
        ],
        shell=True,
    )

# Continue with the remaining parts of the script (job submission)
job_scripts = []

# Create job scripts for each cycle
for i in range(2, ncycles):
    job_script = f"launch_anneal_{i}.sh"
    job_scripts.append(job_script)

    with open(job_script, "w") as file:
        file.write(f"""\
#!/bin/bash
#SBATCH -J {title}_anneal_{i}
#SBATCH -o {title}_slurmoutput_anneal_{i}.out
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --gres=gpu:1
export CUDA_HOME=/usr/local/cuda-10.1
export AMBERHOME=/workGPU/shared/amber18
source $AMBERHOME/amber.sh
$AMBERHOME/bin/pmemd.cuda -O -i {title}_anneal_1.in -o {title}_anneal_{i}.out -p {title}_1.parm7 -c {title}_anneal_{b4}.rst -r {title}_anneal_{i}.rst -x {title}_anneal_{i}.nc -inf anneal{i}inf
""")

# Create the job submission script
job_submission_script = f"launch_full_2_{ncycles}.sh"

with open(job_submission_script, "w") as file:
    file.write(f"""\
job2=$(sbatch launch_EqProd_1.sh)
jid2=$(echo ${{job2}} | awk '{{print $4}}')
job3=$(sbatch --dependency=afterok:$jid2 launch_anneal.sh)
jid3=$(echo ${{job3}} | awk '{{print $4}}')
job1=$(sbatch --dependency=afterok:$jid3 launch_anneal_2.sh)
jid1=$(echo ${{job1}} | awk '{{print $4}}')
""")

# Add job submission commands for remaining cycles
with open(job_submission_script, "a") as file:
    for i in range(3, ncycles):
        file.write(f"""\
job1=$(sbatch --dependency=afterok:$jid1 {job_scripts[i-2]})
jid1=$(echo ${{job1}} | awk '{{print $4}}')
""")

# Submit the job submission script
subprocess.run(["sbatch", job_submission_script])

# Clean up the job scripts
for job_script in job_scripts:
    os.remove(job_script)


