# 🔥 ONNX/TensorRT Optimization

This project demonstrates how to accelerate inference in image classification tasks using **ONNX** and **TensorRT**, powered by **AutoGluon MultiModalPredictor**. You’ll train a lightweight image model and optimize it for **low-latency prediction**, comparing vanilla PyTorch vs. optimized inference.

> 🚀 Ideal for real-time AI applications, edge deployment, and cloud inference.

---

## 📦 Key Features

- ✅ Train image classification models with [AutoGluon](https://www.autogluon.ai/)
- ✅ Convert models to ONNX for hardware-agnostic inference
- ✅ Accelerate inference using NVIDIA [TensorRT](https://developer.nvidia.com/tensorrt)
- ✅ Benchmark PyTorch vs. TensorRT speed
- ✅ Fully reproducible in Jupyter / Colab / [Saturn Cloud](https://saturncloud.io)

---

## 📁 Project Structure

```

.
├── ag_automm_tutorial/
│   └── petfinder_for_tutorial/
├── notebook.ipynb  # Main inference pipeline
└── README.md       # This file

````

---

## ⚙️ Dependencies

Install in Jupyter or Colab:

```bash
pip install autogluon
pip install onnx onnxruntime-gpu
pip install matplotlib
````

> 💡 TensorRT is used automatically by ONNXRuntime on supported NVIDIA GPUs. No manual installation required for ONNXRuntime-GPU.

---

## 🚀 How to Run

1. Launch the notebook: `notebook.ipynb`
2. Follow the **7 steps** to:

   * Load and clean dataset
   * Train image model
   * Export to ONNX
   * Optimize with TensorRT
   * Compare inference speed (PyTorch vs. ONNX)
3. Visualize performance

---

## 📊 Sample Speedup

| Framework | Inference Speed |
| --------- | --------------- |
| PyTorch   | ~50 rows/sec    |
| TensorRT  | ~150 rows/sec   |

> 🔧 Results will vary based on GPU model and batch size.

---

## ☁️ Recommended Environment: Saturn Cloud

This notebook runs great on [**Saturn Cloud**](https://saturncloud.io):

* 🔁 NVIDIA GPU preinstalled with CUDA + TensorRT
* 💡 Jupyter, VSCode, and Python environments
* 🕒 Schedule jobs or deploy as APIs
* 🔍 Great for prototyping + production AI workflows

🟢 Try it free: [https://saturncloud.io](https://saturncloud.io)

---

## 🧠 Related Projects

* [AutoGluon Examples](https://github.com/autogluon/autogluon/tree/master/examples)
* [ONNX Runtime](https://onnxruntime.ai/)
* [TensorRT Developer Docs](https://docs.nvidia.com/deeplearning/tensorrt/)
* [Saturn Cloud Templates](https://saturncloud.io/resources/templates/)

---


