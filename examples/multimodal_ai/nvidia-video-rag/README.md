# 🎥 Video Q&A Pipeline (LangChain + Transformers)

A lightweight, modular pipeline that enables question-answering from video content using frame extraction, image captioning, semantic retrieval, and LLM-based response generation.

## 🚀 Features

* ✅ Frame extraction from video (OpenCV)
* 🧠 Image captioning using ViT-GPT2 (Hugging Face)
* 🔍 Semantic retrieval with ChromaDB + LangChain
* 🤖 Q&A using `flan-t5-small` (Text2Text pipeline)
* 💻 Works in CPU/GPU environments

## 📦 Dependencies

* `torch`, `transformers`, `opencv-python-headless`
* `langchain`, `langchain-community`, `langchain-huggingface`
* `sentence-transformers`, `chromadb`, `Pillow`


## 🧩 Pipeline Overview

```text
Video → Frames → Captions → Embeddings → ChromaDB → Retriever + LLM → Answer
```

## 🛠️ Usage

1. **Run in Jupyter**

2. **Open the notebook** and follow steps:

   * 📥 Download video
   * 🖼️ Extract frames
   * 🧾 Generate captions
   * 💾 Store in ChromaDB
   * ❓ Ask questions via LLM

## 🧠 Example Questions

* What is happening in the video?
* What objects or people appear?
* Describe the main activity.

## ✅ Conclusion

This template provides a clean foundation for building **video understanding** applications using modern AI tooling. Extend it with your own videos, models, or use cases.

