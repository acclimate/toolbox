#!/bin/bash
#SBATCH --qos=priority
#SBATCH --job-name=climate_ensemble
#SBATCH --account=acclimat
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --chdir=/p/projects/acclimate/projects/post-proc-dev
#SBATCH --cpus-per-task=16
#SBATCH --ntasks=1
#SBATCH --time=0-01:59:00
#SBATCH --export=ALL,OMP_PROC_BIND=FALSE
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
source activate compacts-simulations
python post-processing/scripts/demo_climate_ensemble.py