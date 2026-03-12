import os
import cv2
import torch
import numpy as np
import faiss
import logging
import streamlit as st
from transformers import (
    AutoProcessor, 
    AutoModelForImageTextToText, # Modern class for LLaVA
    AutoTokenizer, 
    CLIPProcessor, 
    CLIPModel,
    BitsAndBytesConfig # For proper quantization
)
from PIL import Image
from typing import List, Any

# --- Configuration ---
VIDEO_DIR = "data"
VIDEO_FILENAME = "input_video.mp4" 
VIDEO_PATH = os.path.join(VIDEO_DIR, VIDEO_FILENAME)
FRAME_RATE_SEC = 5 
VLM_MODEL_ID = "llava-hf/llava-v1.6-mistral-7b-hf" 
CLIP_MODEL_ID = "openai/clip-vit-base-patch32"

logging.basicConfig(level=logging.INFO)

# --- CACHED RESOURCES ---
@st.cache_resource
def load_vlm_components():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    st.info("Loading CLIP Components...")
    clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_ID)
    clip_model = CLIPModel.from_pretrained(CLIP_MODEL_ID).to(device)

    st.info("Loading LLaVA VLM (Quantized)...")
    # Modern way to load in 8-bit to avoid deprecation warnings
    quant_config = BitsAndBytesConfig(load_in_8bit=True)
    
    vlm_model = AutoModelForImageTextToText.from_pretrained(
        VLM_MODEL_ID, 
        quantization_config=quant_config,
        device_map="auto"
    )
    vlm_tokenizer = AutoTokenizer.from_pretrained(VLM_MODEL_ID)
    vlm_processor = AutoProcessor.from_pretrained(VLM_MODEL_ID)

    return clip_processor, clip_model, vlm_tokenizer, vlm_model, vlm_processor, device

# --- STAGE 1: Frame Extraction ---
@st.cache_data
def extract_frames(video_path: str, rate_sec: int) -> List[np.ndarray]:
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * rate_sec)
    frames = []
    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret: break
        if frame_count % frame_interval == 0:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_count += 1
    video.release()
    return frames

# --- STAGE 2: Multimodal Embedding Generation ---
@st.cache_data
# FIX 1: Leading underscores added to prevent Hashing Errors
def generate_embeddings(frames: List[np.ndarray], _clip_processor, _clip_model, device: str):
    frame_embeddings = []
    for frame in frames:
        inputs = _clip_processor(images=[frame], return_tensors="pt").to(device)
        with torch.no_grad():
            image_features = _clip_model.get_image_features(**inputs)
            embedding = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
            frame_embeddings.append(embedding.cpu().numpy().flatten())
            
    embeddings_matrix = np.stack(frame_embeddings).astype('float32')
    dimension = embeddings_matrix.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_matrix)
    return index, embeddings_matrix

# --- STAGE 3: Retrieval-Augmented Q&A (RAG) ---
def answer_question(
    question: str, 
    faiss_index: Any, 
    frames: List[np.ndarray], 
    clip_processor: CLIPProcessor, 
    clip_model: CLIPModel,
    vlm_tokenizer: AutoTokenizer, 
    vlm_model: Any,
    vlm_processor: Any,
    device: str
) -> tuple:
    # 3.1 Retrieval
    text_inputs = clip_processor(text=[question], return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        text_features = clip_model.get_text_features(**text_inputs)
        query_embedding = (text_features / text_features.norm(p=2, dim=-1, keepdim=True)).cpu().numpy().astype('float32')
    
    # 3.2 Search
    distances, indices = faiss_index.search(query_embedding, 1)
    best_frame_index = indices[0][0]
    best_similarity = 1 / (1 + distances[0][0])
    
    # 3.3 Generation
    best_frame_image = Image.fromarray(frames[best_frame_index])
    
    # Correct LLaVA-1.6 Prompt Format
    prompt = f"[INST] <image>\n{question} [/INST]"
    
    # FIX 2: Use the integrated vlm_processor to handle image + text
    inputs = vlm_processor(text=prompt, images=best_frame_image, return_tensors="pt").to(device)
    
    with torch.no_grad():
        output_ids = vlm_model.generate(**inputs, max_new_tokens=128)
    
    # FIX 3: Robust decoding to avoid 'NoneType' or subscription errors
    full_text = vlm_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    # Extract only the assistant response
    if "[/INST]" in full_text:
        final_answer = full_text.split("[/INST]")[-1].strip()
    else:
        final_answer = full_text

    return final_answer, best_frame_index, best_similarity

# --- STREAMLIT DASHBOARD INTERFACE ---
def main_dashboard():
    st.set_page_config(layout="wide", page_title="Video RAG Dashboard")
    st.title("📹 Multimodal Video RAG Dashboard")

    # 1. Load Resources
    try:
        clip_p, clip_m, vlm_t, vlm_m, vlm_p, dev = load_vlm_components()
    except Exception as e:
        st.error(f"Resource Load Error: {e}")
        return

    if not os.path.exists(VIDEO_PATH):
        st.warning("Video file not found in /data.")
        return

    frames = extract_frames(VIDEO_PATH, FRAME_RATE_SEC)
    
    with st.spinner("Indexing Frames..."):
        # Calling with underscores
        faiss_index, _ = generate_embeddings(frames, _clip_processor=clip_p, _clip_model=clip_m, device=dev)

    st.markdown("---")
    question = st.text_input("Ask about the video:", value="What is happening in this video?")
    
    if st.button("Analyze", type="primary"):
        with st.spinner("VLM is thinking..."):
            try:
                ans, idx, sim = answer_question(
                    question, faiss_index, frames, clip_p, clip_m, vlm_t, vlm_m, vlm_p, dev
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Answer")
                    st.write(ans)
                    st.metric("Similarity", f"{sim:.4f}")
                with col2:
                    st.subheader("Reference Frame")
                    st.image(frames[idx])
            except Exception as e:
                st.error(f"RAG Error: {e}")

if __name__ == "__main__":
    main_dashboard()