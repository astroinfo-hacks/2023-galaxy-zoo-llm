#!/bin/bash
#SBATCH --job-name=lavvastro
#SBATCH --output=%x%j.out    # job-name + jobid
#SBATCH --error=%x%j.out    #
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=64   # 8 per GPU
#SBATCH --hint=nomultithread 
#SBATCH --time=06:00:00
##SBATCH --qos=qos_gpu-dev
#SBATCH --account=owt@a100
#SBATCH -C a100

cd /gpfswork/rech/owt/commun/lavastro_training
module load cuda/11.7.1 nccl/2.12.12-1-cuda cudnn/8.5.0.96-11.7-cuda gcc/8.5.0 openmpi/4.1.1-cuda intel-mkl/2020.4 magma/2.7.0-cuda sox/14.4.2 sparsehash/2.0.3 libjpeg-turbo/2.1.3 python/3.9.12
eval $(idrenv -d owt)

export PYTHONUSERBASE=/gpfswork/rech/owt/commun/galaxy_zoo/.local_sample
export PATH=/gpfswork/rech/owt/commun/galaxy_zoo/.local_sample/bin/:$PATH

# Disable wandb to avoid issues
wandb offline

## for debugging
set -x

## run script in parallel
srun torchrun --nnodes=1 --nproc_per_node=6 --master_port=25001 \
    ~/repo/LLaVA/llava/train/train_mem.py \
    --model_name_or_path /gpfswork/rech/owt/commun/galaxy_zoo/checkpoints/llava-13b-pretrain\
    --version v0 \
    --data_path /gpfsscratch/rech/owt/commun/galaxy_zoo/qa_trimmed.json \
    --image_folder /gpfsscratch/rech/owt/commun/galaxy_zoo \
    --vision_tower openai/clip-vit-large-patch14 \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end True \
    --bf16 True \
    --output_dir /gpfswork/rech/owt/commun/galaxy_zoo/checkpoints/llava-13b-finetune \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 2000  \
    --save_total_limit 1 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True 

date