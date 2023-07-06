#!/bin/bash
#SBATCH --job-name=generate_qa_v1
##SBATCH --output=%x%j.out    # job-name + jobid
#SBATCH --error=%x%j.err    #
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=compil
#SBATCH --cpus-per-task=2   
#SBATCH --hint=nomultithread 
#SBATCH --time=20:00:00
#SBATCH --account=owt@v100

module load python/3.9.12
export PYTHONUSERBASE=/gpfswork/rech/owt/uka17ma/galaxy_zoo/.local
export PATH=$PATH:$PYTHONUSERBASE/bin
source $HOME/.bashrc

## for debugging
set -x

## run script in parallel
srun python -u /gpfswork/rech/owt/uka17ma/2023-galaxy-zoo-llm/scripts/generate_qa.py \
    --input-file /gpfsscratch/rech/owt/commun/galaxy_zoo_datasets/gz_data/json/GZ_talk_comments_notes_urls_AISSAI.json \
    --output-file /gpfsscratch/rech/owt/commun/galaxy_zoo_datasets/v1/dataset_v1.json \
    --prompt-file /gpfswork/rech/owt/uka17ma/2023-galaxy-zoo-llm/scripts/prompt.py \
    --openai-api-key OPENAI_API_KEY_V1 \
    --mode conv 
date
