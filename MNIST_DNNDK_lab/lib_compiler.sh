#!/bin/bash

# Define variables
KERNEL_PATH="${PWD}/compile"
NET_NAME=MNIST   # change if needed

# Enter compile directory
cd "${KERNEL_PATH}" || { echo "Cannot enter directory ${KERNEL_PATH}"; exit 1; }

# Create shared object (.so) from ELF
aarch64-xilinx-linux-gcc --sysroot=/opt/vitis_ai/petalinux_sdk/sysroots/aarch64-xilinx-linux \
    -fPIC -shared dpu_deploy.elf -o libdpumodel_${NET_NAME}.so

echo "Shared library libdpumodel_${NET_NAME}.so created in ${KERNEL_PATH}"
