# 🪐 Saturn Cloud Template: Object Detection with Faster R-CNN

This template provides a ready-to-run **object detection project** built for **Saturn Cloud**.  
It uses a pre-trained **Faster R-CNN** model to detect common objects in images and visualize results — all powered by **GPU acceleration**.

Use this template as a **fast start** for your own computer vision or image analysis projects on Saturn Cloud.

---

## 🧠 What This Template Does

- Load and analyze images from **local paths** or **URLs**  
- Detect objects using a pre-trained **Faster R-CNN** model  
- Display bounding boxes and confidence scores  
- Run interactively from a terminal or Jupyter Notebook  
- Easily extend to **custom training, datasets, or scaling** with Saturn Cloud’s GPU clusters  

---

## ⚙️ Saturn Cloud Environment Setup

This template is pre-configured for **Saturn Cloud GPU environments**.  
You can run it immediately on a GPU-backed resource — no setup required beyond installing dependencies.

### Default Environment
- **Image**: `saturncloud/pytorch:latest`  
- **Hardware**: GPU instance (recommended: 1× NVIDIA T4 or A10G)  
- **Python**: 3.10+  
- **Memory**: 8GB+  

### Dependencies (from `requirements.txt`)
```

torch
torchvision
matplotlib
pillow
requests

````

To reproduce the environment manually:

```bash
pip install -r requirements.txt
````

---

## 🚀 Quickstart (in Saturn Cloud)

1. **Launch this template** in your Saturn Cloud workspace:

   * Go to [Saturn Cloud](https://saturncloud.io/)
   * Click **New Project → From Template**
   * Choose **Object Detection with Faster R-CNN**

2. **Open the Jupyter notebook and run all the code cells**.

3. When prompted, enter an image path or URL.
   You can test with this example URL:

   ```
   https://plus.unsplash.com/premium_photo-1667030489905-d8e6309ebe0e?ixlib=rb-4.1.0&auto=format&fit=crop&q=60&w=200
   ```

   Output:

   ```
   📡 Downloading image from URL...
   ✅ Image downloaded successfully
   🎯 Detected 3 objects (threshold: 0.5):
     1. Person: 99.3%
     2. Dog: 97.1%
     3. Chair: 88.4%
   ```

4. A visualization window will display the bounding boxes drawn over the detected objects.

---

## 🧩 Core Components

### `detect_in_uploaded_image(image_input, threshold=0.5)`

Detects objects in an image (from a local file or URL) using the pre-trained model.
Returns the bounding boxes, labels, and confidence scores.

---

## 📚 References

* [Saturn Cloud Examples Repository](https://github.com/saturncloud/examples)
* [Faster R-CNN Model Implementation](https://github.com/trzy/FasterRCNN)
* [COCO Dataset Classes](https://cocodataset.org/#home)
* [Saturn Cloud Documentation](https://saturncloud.io/docs/)


