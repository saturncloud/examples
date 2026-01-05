import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EDA Profiler", layout="wide")

# --- INTRODUCTION ---
st.title("📊 One-Click EDA Dashboard")
st.markdown("This dashboard provides instant statistical profiling and visualization for the Tips dataset.")

# --- STEP 2: LOAD AND PREPARE DATASET ---
# We load the Tips dataset from seaborn's built-in repository.
@st.cache_data # Cache data to prevent reloading on every interaction
def load_data():
    return sns.load_dataset('tips')

df = load_data()

# --- STEP 3: SIDEBAR FILTERS ---
# We enable global filters to allow users to slice data by specific days of the week.
st.sidebar.header("Global Filters")
selected_day = st.sidebar.multiselect(
    "Select Day", 
    options=df['day'].unique(), 
    default=df['day'].unique()
)
filtered_df = df[df['day'].isin(selected_day)]

# --- STEP 4: STATISTICS PROFILER ---
# This block calculates and displays the numerical summary statistics for the filtered data.
col1, col2 = st.columns(2)
with col1:
    st.subheader("🔢 Statistical Summary")
    st.dataframe(filtered_df.describe(), use_container_width=True)

with col2:
    st.subheader("📋 Raw Data Sample")
    st.write(filtered_df.head(10))

# --- STEP 5: VISUALIZATION ---
# Using Seaborn and Matplotlib to render the distribution of bill amounts interactively.
st.subheader("📈 Distribution of Total Bills")
fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(filtered_df['total_bill'], kde=True, ax=ax, color="#FF4B4B")
st.pyplot(fig)