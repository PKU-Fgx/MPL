#!/bin/bash

OUTPUT_NAME="<PATH_TO_SAVE_CHECKPOINT>"
TRAIN_DATA_PATH="../dataTrain/MPL_train_data.jsonl"
BASEMODEL_PATH="meta-llama/Meta-Llama-3-8B"

bash ./scripts/MPL_qlora.sh $OUTPUT_NAME $TRAIN_DATA_PATH $BASEMODEL_PATH