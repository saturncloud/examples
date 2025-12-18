import streamlit as st
import torch
import numpy as np
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import os

# --- Configuration ---
MODEL_ID = "ali-vilab/text-to-video-ms-1.7b" 

# --- Resource Loading ---
@st.cache_resource
def load_pipeline():
    """Initializes the Text-to-Video Diffusion Pipeline."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the pipeline with float16 for memory efficiency
    pipe = DiffusionPipeline.from_pretrained(
        MODEL_ID, 
        torch_dtype=torch.float16, 
        variant="fp16"
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    
    # Memory Optimizations for Cloud GPUs
    pipe.enable_model_cpu_offload() 
    pipe.enable_vae_slicing()      
    
    return pipe, device

# --- Dashboard Interface ---
def main():
    st.set_page_config(page_title="Text→Video Diffusion", layout="wide")
    st.title("🎬 Text→Video Diffusion Dashboard")
    st.markdown("Enter a prompt below to generate a short AI-powered video.")

    # 1. Load Model
    with st.spinner("Initializing Model..."):
        try:
            pipe, device = load_pipeline()
        except Exception as e:
            st.error(f"Failed to load model: {e}")
            return
    
    # 2. Sidebar Configuration
    st.sidebar.header("Generation Settings")
    num_frames = st.sidebar.slider("Number of Frames", 8, 24, 16)
    inference_steps = st.sidebar.slider("Inference Steps", 15, 50, 25)
    
    # 3. Main Interface
    prompt = st.text_area("Video Prompt:", value="A panda eating bamboo on a rock, high quality")
    
    if st.button("Generate Video", type="primary"):
        if not prompt:
            st.warning("Please enter a prompt.")
            return

        with st.spinner("Denoising Latents... (This may take ~1-2 minutes)"):
            try:
                # 3.1 Run the Pipeline
                output = pipe(
                    prompt, 
                    num_inference_steps=inference_steps, 
                    num_frames=num_frames
                )
                
                # Extract the inner list and convert each frame to a numpy array.
                video_frames = [np.array(frame) for frame in output.frames[0]]
                
                # 3.3 Export to local file
                output_video_path = "generated_video.mp4"
                export_to_video(video_frames, output_video_path)
                
                st.success("Generation Complete!")
                st.video(output_video_path)
                
            except Exception as e:
                st.error(f"Generation Error: {e}")

if __name__ == "__main__":
    main()