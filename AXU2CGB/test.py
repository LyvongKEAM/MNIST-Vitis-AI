import os
import cv2
import numpy as np
import time
from dnndk import n2cube

# Configurations
TEST_IMAGE_PATH = "/home/root/MNIST/MNIST_deploy/MNIST_JPG_testing/6/9999.jpg"
OUTPUT_DIR = "./output_result_mnist/"

KERNEL_NAME = "deploy"
INPUT_NODE = "conv2d_Conv2D"
OUTPUT_NODE = "dense_1_MatMul"
INPUT_SHAPE = (28, 28)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Cannot load image: {img_path}")
    img = cv2.resize(img, INPUT_SHAPE)
    img = img.astype(np.float32) / 255.0
    img = img.reshape(1, 28, 28, 1)  # NHWC format
    return img

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=-1, keepdims=True)

def run_inference():
    n2cube.dpuOpen()
    kernel = n2cube.dpuLoadKernel(KERNEL_NAME)
    task = n2cube.dpuCreateTask(kernel, 0)

    if os.path.isdir(TEST_IMAGE_PATH):
        image_files = sorted([f for f in os.listdir(TEST_IMAGE_PATH) if f.endswith(".png") or f.endswith(".jpg")])
        image_paths = [os.path.join(TEST_IMAGE_PATH, f) for f in image_files]
    else:
        image_paths = [TEST_IMAGE_PATH]

    for img_path in image_paths:
        try:
            input_data = preprocess_image(img_path)
        except ValueError as e:
            print(e)
            continue

        input_len = n2cube.dpuGetInputTensorSize(task, INPUT_NODE)
        n2cube.dpuSetInputTensorInHWCFP32(task, INPUT_NODE, input_data, input_len)

        # Run task and get hardware DPU execution time
        n2cube.dpuRunTask(task)
        fpga_inference_time_us = n2cube.dpuGetTaskProfile(task)
        fpga_inference_time_ms = fpga_inference_time_us / 1000.0

        output_size = n2cube.dpuGetOutputTensorSize(task, OUTPUT_NODE)
        output_data = n2cube.dpuGetOutputTensorInHWCFP32(task, OUTPUT_NODE, output_size)

        # Apply softmax
        probabilities = softmax(output_data)
        prediction = int(np.argmax(probabilities))
        confidence = float(np.max(probabilities))

        print(f"Image: {os.path.basename(img_path)} ? Predicted: {prediction} (Confidence: {confidence:.2f})")
        print(f"DPU Inference Time: {fpga_inference_time_ms:.2f} ms")

        img_vis = cv2.imread(img_path)
        if img_vis is not None:
            cv2.putText(img_vis, f"Pred: {prediction}", (5, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            cv2.putText(img_vis, f"Infer Time: {fpga_inference_time_ms:.2f}ms", (5, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            cv2.imwrite(os.path.join(OUTPUT_DIR, os.path.basename(img_path)), img_vis)

    n2cube.dpuDestroyTask(task)
    n2cube.dpuDestroyKernel(kernel)
    n2cube.dpuClose()

if __name__ == "__main__":
    run_inference()
