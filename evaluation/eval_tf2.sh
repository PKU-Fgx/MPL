#!/bin/bash

TRAIN_DATA_PATHS=("mpl_ftq_llama3_8b_3E4")
for i in "${!TRAIN_DATA_PATHS[@]}"; do
    OUTPUT_NAME="${TRAIN_DATA_PATHS[$i]}"
    
    python3 eval_vllm.py  --model_id $OUTPUT_NAME
    python3 get_scores.py --model_id $OUTPUT_NAME
done
