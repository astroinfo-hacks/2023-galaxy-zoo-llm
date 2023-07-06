python apply_llavastro.py \
    --model-name ./checkpoints/LLaVA-13B-v0 \
    --question-file \
    playground/data/coco2014_val_qa_eval/qa90_questions.jsonl \
    --image-folder \
    /path/to/coco2014_val \
    --answers-file \
    /path/to/answer-file.jsonl



    python /gpfswork/rech/owt/uka17ma/2023-galaxy-zoo-llm/scripts/apply_llavastro.py \
     --model-name /gpfswork/rech/owt/commun/LLaVA-13B-v0 \
     --image-folder /gpfsscratch/rech/owt/commun/galaxy_zoo \
     --answers-file /gpfswork/rech/owt/commun/galaxy_zoo/answer.jsonl