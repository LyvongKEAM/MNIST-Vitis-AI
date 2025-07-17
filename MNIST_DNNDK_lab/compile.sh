#!/bin/bash

# delete previous results
rm -rf ./compile
mkdir ./compile

#conda activate decent_q3
FROZEN_PB_PATH="${PWD}/quantize_results/deploy_model.pb"
OUTPUT_DIR="${PWD}/compile"
# Compile
echo "#####################################"
echo "COMPILE WITH VAI_C_TENSORFLOW"
echo "#####################################"
vai_c_tensorflow \
       --frozen_pb="${FROZEN_PB_PATH}" \
       --arch=./AXU2CGB_DPU_B1152.json \
       --output_dir="${OUTPUT_DIR}"    

echo "#####################################"
echo "COMPILATION COMPLETED"
echo "#####################################"

