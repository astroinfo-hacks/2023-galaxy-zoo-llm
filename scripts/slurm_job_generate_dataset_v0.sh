#!/bin/bash
#SBATCH --job-name=generate_qa
#SBATCH --output=%x%j.out    # job-name + jobid
#SBATCH --error=%x%j.out    #
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=10   # 8 per GPU
#SBATCH --hint=nomultithread 
#SBATCH --time=20:00:00
#SBATCH --account=owt@v100

module load cuda/11.7.1 nccl/2.12.12-1-cuda cudnn/8.5.0.96-11.7-cuda gcc/8.5.0 openmpi/4.1.1-cuda intel-mkl/2020.4 magma/2.7.0-cuda sox/14.4.2 sparsehash/2.0.3 libjpeg-turbo/2.1.3 python/3.9.12

export PYTHONUSERBASE=$ALL_CCFRWORK/galaxy_zoo/.local_sample
export PATH=/gpfswork/rech/owt/commun/galaxy_zoo/.local_sample/bin/:$PATH

## for debugging
set -x

## run script in parallel
srun python -u /gpfswork/rech/owt/uka17ma/2023-galaxy-zoo-llm/scripts/generate_qa.py \
    --input-file /gpfsscratch/rech/owt/commun/galaxy_zoo_datasets/gz_data/json/GZ_talk_comments_notes_urls_AISSAI.json \
    --output-file /gpfsscratch/rech/owt/commun/galaxy_zoo_datasets/v0 \
    --prompt-file /gpfswork/rech/owt/uka17ma/2023-galaxy-zoo-llm/scripts/prompt.py \
    --mode desc 
date
