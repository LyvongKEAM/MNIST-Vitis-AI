## Vitis-AI

[Vitis AI](https://www.xilinx.com/products/design-tools/vitis/vitis-ai.html) is Xilinx's development platform for AI inference on Xilinx hardware platforms, including both edge devices (like Zynq UltraScale+ MPSoC and Versal ACAP) and data center accelerators. It provides a comprehensive toolchain for optimizing, quantizing, compiling, and deploying deep learning models efficiently on Xilinx devices.

Vitis AI supports popular frameworks such as TensorFlow, PyTorch, and Caffe, and includes:
- Pre-optimized models in the Model Zoo
- Quantizers to convert floating-point models to fixed-point
- DNNDK and VART runtimes for target-side deployment
- Compiler tools for DPU (Deep Processing Unit) acceleration

In this project, we use **Vitis AI v1.2.4** to train, quantize, and deploy an MNIST digit classification model on the **AXU2CGB UltraScale+ FPGA board**.

---

This guide walks you through:
- Training the MNIST model
- Preparing it with the Vitis AI toolchain
- Deploying it on hardware for real-time inference
