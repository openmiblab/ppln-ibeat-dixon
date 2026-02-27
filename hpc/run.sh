#!/bin/bash
#SBATCH --mem=32G
#SBATCH --cpus-per-task=1
#SBATCH --time=95:00:00
#SBATCH --mail-user=s.sourbron@sheffield.ac.uk
#SBATCH --mail-type=FAIL,END
#SBATCH --job-name=dxn
#SBATCH --output=logs/dxn.out
#SBATCH --error=logs/dxn.err

unset SLURM_CPU_BIND
export SLURM_EXPORT_ENV=ALL

module load Anaconda3/2024.02-1
module load Python/3.10.8-GCCcore-12.2.0 # essential to load latest GCC
module load CUDA/11.8.0 # must match with version in environment.yml

# Get folder locations
USERNAME=$(whoami)
LOCAL="/mnt/parscratch/users/$USERNAME"
REMOTE="login1:/shared/abdominal_imaging/Archive"

# Define path variables here
ENV="$LOCAL/envs/elastix"
CODE="$LOCAL/scripts/iBEAt-dixon/src"
BUILD="$LOCAL/data/iBEAt_Build"
ARCHIVE="$REMOTE/iBEAt_Build"

# srun runs your program on the allocated compute resources managed by Slurm
# srun "$ENV/bin/python" "$CODE/stage_8_align_dixon.py" --build="$BUILD"
# srun "$ENV/bin/python" "$CODE/stage_9_check_alignment.py" --build="$BUILD"

srun "$ENV/bin/python" "$CODE/stage_10_exclude_alignments.py" --build="$BUILD"
rsync -av --no-group --no-perms --delete "$BUILD/dixon/stage_8_align_dixon_data" "$ARCHIVE/dixon"
rsync -av --no-group --no-perms --delete "$BUILD/dixon/stage_9_check_alignment" "$ARCHIVE/dixon"
rsync -av --no-group --no-perms --delete "$BUILD/dixon/stage_10_exclude_alignments" "$ARCHIVE/dixon"