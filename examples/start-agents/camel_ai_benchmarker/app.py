import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Core CAMEL-AI imports
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent

# Load environment variables for the fallbacks
load_dotenv()

# Configure the Streamlit page layout
st.set_page_config(page_title="CAMEL Benchmark", page_icon="🐫", layout="wide")

# Initialize session state to store our dynamic list of models
if "models_to_test" not in st.session_state:
    st.session_state.models_to_test = []

def resolve_credentials(provider, custom_key, custom_url):
    """Smartly resolves keys and URLs, falling back to .env if UI fields are blank."""
    # Resolve API Key
    if custom_key:
        key = custom_key
    else:
        if provider == "OpenAI":
            key = os.getenv("OPENAI_API_KEY")
        elif provider == "Nebius Studio":
            key = os.getenv("NEBIUS_API_KEY")
        elif provider == "OpenAI-Compatible (Custom)":
            # Defaults to Crusoe if you are primarily testing that infrastructure
            key = os.getenv("CRUSOE_API_KEY") 
        else:
            key = None
            
    # Resolve Base URL
    if custom_url:
        url = custom_url
    elif provider == "OpenAI-Compatible (Custom)" and not custom_url:
        url = os.getenv("CRUSOE_API_BASE")
    else:
        url = None
        
    return key, url

# --- UI: SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    st.markdown("Use the main form to add models. Keys are stored securely in session state.")
    st.divider()
    if st.button("🗑️ Clear Model Queue", use_container_width=True):
        st.session_state.models_to_test = []
        st.rerun()

# --- UI: MAIN DASHBOARD ---
st.title("🐫 CAMEL-AI Multi-Infrastructure Benchmark")
st.markdown("Dynamically add models across different cloud providers. Specify unique API keys and Base URLs per model, or leave them blank to fall back to your `.env` variables.")

# Section 1: Add Models to the Queue
st.subheader("1. Add Models to Benchmark")
with st.form("add_model_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        provider_choice = st.selectbox(
            "Platform Integration Framework", 
            ["OpenAI", "Nebius Studio", "OpenAI-Compatible (Custom)"],
            help="Tells CAMEL how to format the API request."
        )
        model_name = st.text_input("Model ID", placeholder="e.g., gpt-4o-mini, meta-llama/Llama-3-8b")
        
    with col2:
        custom_key = st.text_input("API Key (Optional)", type="password", placeholder="Leave blank to use .env fallback")
        custom_endpoint = st.text_input("Base URL (Optional)", placeholder="e.g., https://managed-inference-api-proxy.crusoecloud.com/v1")
        
    submit_model = st.form_submit_button("➕ Add to Queue")
    
    if submit_model and model_name:
        resolved_key, resolved_url = resolve_credentials(provider_choice, custom_key, custom_endpoint)
        
        st.session_state.models_to_test.append({
            "Provider": provider_choice,
            "Model ID": model_name,
            "API Key": resolved_key,
            "Base URL": resolved_url
        })
        st.success(f"Added {model_name} to queue!")

# Display current queue
if st.session_state.models_to_test:
    st.write("**Current Testing Queue:**")
    
    # We create a display copy of the dataframe to securely mask the API keys in the UI
    display_df = pd.DataFrame(st.session_state.models_to_test)
    display_df["API Key"] = display_df["API Key"].apply(lambda x: "🔑 Loaded" if x else "❌ Missing")
    display_df["Base URL"] = display_df["Base URL"].fillna("Default")
    
    st.dataframe(display_df, use_container_width=True)

# Section 2: Prompt Configuration
st.subheader("2. Configure Benchmark")
test_prompt = st.text_area(
    "Benchmark Prompt", 
    value="Write a concise, high-level overview of the history of artificial intelligence, highlighting the major winters and breakthroughs. Keep it strictly under 150 words.",
    height=100
)

# Section 3: Execution
if st.button("🚀 Run Benchmark", type="primary"):
    if not st.session_state.models_to_test:
        st.warning("Please add at least one model to the queue first.")
        st.stop()
        
    results_data = []
    
    # Map UI selections to CAMEL Platform Enums
    platform_map = {
        "OpenAI": ModelPlatformType.OPENAI,
        "Nebius Studio": ModelPlatformType.NEBIUS,
        "OpenAI-Compatible (Custom)": ModelPlatformType.OPENAI 
    }

    # Create a visual progress bar
    progress_text = "Benchmarking in progress. Please wait..."
    my_bar = st.progress(0, text=progress_text)
    
    for idx, m in enumerate(st.session_state.models_to_test):
        platform_enum = platform_map[m["Provider"]]
        api_key = m["API Key"]
        
        if not api_key:
            results_data.append({"Model": m["Model ID"], "Status": "⚠️ Skipped (No Key)", "Exec Time (s)": None, "Length": None})
            continue
            
        try:
            # Build the dynamic arguments for the ModelFactory
            factory_kwargs = {
                "model_platform": platform_enum,
                "model_type": m["Model ID"],
                "model_config_dict": {"temperature": 0.0},
                "api_key": api_key
            }
            if m["Base URL"]:
                factory_kwargs["url"] = m["Base URL"]

            # Initialize CAMEL agent
            camel_model = ModelFactory.create(**factory_kwargs)
            agent = ChatAgent(system_message="You are a highly efficient, objective technical writer.", model=camel_model)
            
            # Measure execution
            start_time = time.time()
            response = agent.step(test_prompt)
            end_time = time.time()
            
            exec_time = round(end_time - start_time, 2)
            content = response.msgs[0].content if hasattr(response, 'msgs') else response.msg.content
            
            results_data.append({"Model": m["Model ID"], "Status": "✅ Success", "Exec Time (s)": exec_time, "Length": len(content)})
            
        except Exception as e:
            results_data.append({"Model": m["Model ID"], "Status": f"❌ Error: {str(e)[:40]}", "Exec Time (s)": None, "Length": None})
            
        # Update progress bar
        my_bar.progress((idx + 1) / len(st.session_state.models_to_test), text=f"Processed {m['Model ID']}...")

    # Clear progress bar and display results
    my_bar.empty()
    st.subheader("📊 Benchmark Results")
    
    df_results = pd.DataFrame(results_data)
    st.dataframe(df_results, use_container_width=True)
    
    # Automatically generate a bar chart for successful runs
    success_df = df_results[df_results["Status"] == "✅ Success"]
    if not success_df.empty:
        st.write("**Execution Latency Comparison (Seconds)**")
        st.bar_chart(data=success_df, x="Model", y="Exec Time (s)", color="#ff9900")