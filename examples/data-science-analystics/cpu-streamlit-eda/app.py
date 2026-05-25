import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EDA Profiler", layout="wide")

# --- TITLE ---
st.title("📊 One-Click EDA Dashboard")
st.markdown("Upload any CSV file to instantly profile your data — or explore the built-in Tips dataset to get started.")

# --- SIDEBAR: DATA SOURCE ---
st.sidebar.header("📂 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload your CSV", type=["csv"])

@st.cache_data
def load_default():
    return sns.load_dataset("tips")

@st.cache_data
def load_uploaded(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    df = load_uploaded(uploaded_file)
    st.sidebar.success(f"✅ Loaded: {uploaded_file.name}")
else:
    df = load_default()
    st.sidebar.info("💡 No file uploaded — showing built-in Tips dataset. Upload a CSV above to use your own data.")

# --- SIDEBAR: FILTERS ---
st.sidebar.header("🔎 Filters")

# Dynamically detect categorical columns and let user pick which one to filter on
categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

if categorical_cols:
    filter_col = st.sidebar.selectbox("Filter by column", options=categorical_cols)
    selected_values = st.sidebar.multiselect(
        f"Select {filter_col} values",
        options=df[filter_col].unique(),
        default=df[filter_col].unique()
    )
    filtered_df = df[df[filter_col].isin(selected_values)]
else:
    filtered_df = df
    st.sidebar.info("No categorical columns found for filtering.")

# --- STEP 4: STATISTICS PROFILER ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔢 Statistical Summary")
    st.dataframe(filtered_df.describe(), use_container_width=True)

with col2:
    st.subheader("📋 Raw Data Sample")
    st.dataframe(filtered_df.head(10), use_container_width=True)

# --- STEP 5: VISUALIZATION ---
st.subheader("📈 Distribution Chart")

numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()

if numeric_cols:
    chart_col = st.selectbox("Select column to visualize", options=numeric_cols)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df[chart_col], kde=True, ax=ax, color="#FF4B4B")
    ax.set_xlabel(chart_col)
    st.pyplot(fig)
else:
    st.info("No numeric columns available for visualization.")
