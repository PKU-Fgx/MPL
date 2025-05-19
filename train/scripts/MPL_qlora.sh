#!bin/bash

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

export DS_SKIP_CUDA_CHECK=1
export OMP_NUM_THREADS=8
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

NUM_GPUS=8
BATCH_SIZE_PER_GPU=8
GRADIENT_ACC_STEPS=2

LR=1e-4
EPOCH_NUM=5
OUTPUT_NAME=$1  # Save Checkpoint Path
TRAIN_DATA_PATH=$2  # Train Data Path
BASEMODEL_PATH=$3  # Base Model Path (Train from Base Model)

bash ./scripts/run.sh \
    $NUM_GPUS \
    $BASEMODEL_PATH \
    $TRAIN_DATA_PATH \
    $BATCH_SIZE_PER_GPU \
    $GRADIENT_ACC_STEPS \
    $LR \
    $EPOCH_NUM \
    $OUTPUT_NAME