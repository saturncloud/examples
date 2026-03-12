# 🔍 Clip Search (CLIP Retrieval Demo)

This template demonstrates how to build a **text-to-image retrieval system** using **CLIP embeddings**. Users can input natural language queries (like _“brain coral”_ or _“a man riding a horse”_), and the system will return the most visually relevant images from a dataset.

Powered by:
- 🧠 **Sentence-Transformers (CLIP-ViT-B-32)** for unified text and image embeddings
- 🖼️ **Towhee Image Search Dataset** (1,000+ labeled images)
- 🧪 **Gradio UI** for interactive image querying
- ☁️ **Runs seamlessly on Saturn Cloud**

---

## 💡 Use Case

This is ideal for:
- Reverse image search
- Visual semantic search systems
- Image tagging and organization
- Educational demos for computer vision and AI retrieval
---

- GPU-powered Jupyter environments
- Persistent storage and shared workspaces
- Scalable cloud infrastructure for deep learning

---

## 📦 Dependencies

```bash
pip install sentence-transformers gradio scikit-learn pandas pillow tqdm
````

---

## 📁 Dataset Info

We use a curated subset of **ImageNet-style data** available here:
[Reverse Image Search Dataset (Towhee)](https://github.com/towhee-io/examples)

Images are labeled for supervised retrieval, and we use the `label` field as pseudo-captions for prompt-to-image similarity.

---

## 📜 License

This project is for **educational and research** purposes only. Data sourced from Towhee and ImageNet subsets.

---

## 📚 Learn More

* [Saturn Cloud Docs](https://saturncloud.io/docs/?utm_source=github&utm_medium=template&utm_campaign=prompt-image-search) – GPU scaling, environments, and deployment
* [More Templates](https://saturncloud.io/resources/templates/?utm_source=github&utm_medium=template&utm_campaign=prompt-image-search) – NLP, vision, LLM, and ML pipelines
