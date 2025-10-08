# PyTorch CIFAR10 Classifier Dashboard

Train a ResNet18 deep learning model on the CIFAR10 image dataset using PyTorch with GPU acceleration and visualize results in an interactive dashboard.

## Overview

This example shows how you can use the power of a GPU to quickly train an image classification neural network in Saturn Cloud. This code runs on a single GPU of a Jupyter server resource.

This is an example of a computer vision neural network which is trained on the CIFAR10 dataset to classify images into 10 categories: airplane, car, bird, cat, deer, dog, frog, horse, ship, and truck. The model uses a ResNet18 architecture which is especially good at image recognition tasks. ResNet uses "residual connections" that allow the network to learn complex patterns while avoiding the vanishing gradient problem. The results are displayed in an interactive dashboard that can be viewed in the notebook or deployed to Saturn Cloud for continuous hosting.

## What is CIFAR10?

CIFAR10 is a dataset of 60,000 32×32 color images across 10 classes:
- 50,000 training images
- 10,000 test images
- 10 classes: airplane, car, bird, cat, deer, dog, frog, horse, ship, truck

## What is ResNet18?

ResNet18 is an 18-layer convolutional neural network that uses "residual connections" (skip connections) to enable training of deeper networks. These skip connections allow gradients to flow more easily during backpropagation, solving the vanishing gradient problem that plagued earlier deep networks. With approximately 11 million parameters, ResNet18 strikes an ideal balance between accuracy and computational efficiency for image classification tasks.

## Requirements

### Hardware
- **NVIDIA GPU (1×)** - Required for training acceleration

### Software
- Python 3.8+
- PyTorch
- Torchvision
- Panel
- hvPlot
- Pandas
- NumPy
- Matplotlib

## What This Template Does

1. **Downloads** the CIFAR10 dataset automatically (~170MB)
2. **Applies** data augmentation (random flips and crops) to training images
3. **Trains** a ResNet18 model for 5 epochs on GPU
4. **Tracks** training loss and accuracy metrics
5. **Evaluates** model performance on test data after each epoch
6. **Visualizes** training curves showing loss and accuracy over time
7. **Displays** sample predictions with correct/incorrect labels
8. **Creates** an interactive dashboard with:
   - Training and test accuracy curves
   - Loss curve over epochs
   - Sample prediction grid (16 images)
   - Key performance indicators (KPIs)