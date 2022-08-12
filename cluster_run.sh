#!/bin/bash
#SBATCH --job-name=coco_extraction # Job name
#SBATCH --ntasks=1                # Number of tasks (see below)
#SBATCH --nodes=1                 # Ensure that all cores are on one machine
#SBATCH --time=3-00:00            # Runtime in D-HH:MM
#SBATCH --partition=gpu-2080ti    # Partition to submit to
#SBATCH --mem=12G                 # Memory pool for all cores
#SBATCH --output=slurm/%x_%j.out  # File to which STDOUT will be written
#SBATCH --error=slurm/%x_%j.err   # File to which STDERR will be written
#SBATCH --gres=gpu:1              # Request one GPU
#SBATCH --cpus-per-task=4       

# include information about the job in the output
scontrol show job=$SLURM_JOB_ID

# run the actual command
srun singularity exec \
--bind /mnt/qb/datasets/ \
--nv \
/mnt/qb/bethge/shared/mmdetection_singularity_image/cmichaelis_mmdetection_official_extended-2022-06-20-2a7122a32898.sif \
python  -i /mnt/qb/datasets/coco/annotations/instances_train2017.json -o /mnt/qb/datasets/coco/annotations/instances_train2017_subset.json -c "potted plant" "sports ball" "person" "bird" "apple" "orange" "banana" "broccoli" "carrot" "vase"


echo DONE.

