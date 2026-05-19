# 📝 NVIDIA NeMo Text Processing

### **Overview**

This template demonstrates [NVIDIA NeMo Text Processing](https://github.com/NVIDIA/NeMo-text-processing) — a library for normalizing text in speech AI pipelines. It covers both directions of text conversion used in production ASR and TTS systems.

* **Hardware:** CPU Large (2 cores, 16 GB RAM) — no GPU required
* **Python:** 3.10+
* **Use Case:** Speech AI preprocessing — TTS pipelines, ASR post-processing, multilingual text normalization

---

### **What it does**

| Operation | Direction | Example |
|-----------|-----------|---------|
| **Text Normalization (TN)** | Written → Spoken | `"$4.99"` → `"four dollars and ninety nine cents"` |
| **Inverse Text Normalization (ITN)** | Spoken → Written | `"three thirty p m"` → `"3:30 p.m."` |

Both operations are powered by **Weighted Finite-State Transducers (WFST)** — fast, rule-based grammars that require no model download and no GPU.

---

### **Tech Stack**

* **NeMo Text Processing (`nemo_text_processing`):** Core normalization library from NVIDIA.
* **Pynini / OpenFst:** WFST engine that powers the grammar rules.
* **15 languages supported:** English, German, Spanish, French, Hungarian, Swedish, Mandarin, Arabic, Italian, Armenian, Japanese, Hindi, Korean, Vietnamese, Portuguese.

---

## 🪐 Using on Saturn Cloud

### 1. Create the workspace from the template

In Saturn Cloud, go to **New Resource → Workspace → Templates** and select **NeMo Text Processing**.

### 2. Start the workspace

Click **Start**. The startup script installs `nemo_text_processing` automatically. This takes 3–5 minutes on first start — watch progress in the **Logs** panel.

### 3. Open the notebook

Once the workspace shows **Running**, click **JupyterLab**. Open `nemo_text_processing_demo.ipynb` from the file browser and run the cells top to bottom.

---

## 🛠️ Local Setup

```bash
pip install nemo_text_processing
```

Then open `nemo_text_processing_demo.ipynb` in JupyterLab.

> **Note:** pip install requires Linux x86_64. On macOS or Windows use conda:
> ```bash
> conda create --name nemo_tn python=3.10
> conda activate nemo_tn
> conda install -c conda-forge pynini
> pip install nemo_text_processing
> ```

---

## 📓 Notebook contents

The demo notebook covers six sections:

1. **Verify Installation** — confirms the library is ready
2. **Text Normalization** — numbers, dates, times, abbreviations, measurements in English
3. **Multilingual TN** — same operations in German and Spanish
4. **Inverse Text Normalization** — convert ASR output back to written form
5. **Batch Processing** — normalize a list of texts in parallel
6. **TTS / ASR Pipeline Examples** — end-to-end pre/post-processing scenarios
7. **Try It Yourself** — sandbox cells to test your own text

---

## ⚙️ Changing the language

Pass any supported language code to the `Normalizer` or `InverseNormalizer`:

```python
normalizer = Normalizer(input_case='cased', lang='de')   # German
normalizer = Normalizer(input_case='cased', lang='es')   # Spanish
normalizer = Normalizer(input_case='cased', lang='zh')   # Mandarin
```

Supported codes: `en` `de` `es` `fr` `hu` `sv` `zh` `ar` `it` `hy` `ja` `hi` `ko` `vi` `pt`

---

## 🔗 Resources

* **NeMo Text Processing repo:** [github.com/NVIDIA/NeMo-text-processing](https://github.com/NVIDIA/NeMo-text-processing)
* **Official tutorials:** [github.com/NVIDIA/NeMo-text-processing/tree/main/tutorials](https://github.com/NVIDIA/NeMo-text-processing/tree/main/tutorials)
* **Saturn Cloud:** [saturncloud.io](https://saturncloud.io/)
