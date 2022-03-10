import streamlit as st
import pandas as pd
import numpy as np
from umap import UMAP
import plotly.express as px

st.set_page_config(page_title="UMAP Projections", layout="wide")
st.title("UMAP Projections for MNIST and Fashion-MNIST Datasets")

st.markdown(
    """
    Uniform Manifold Approximation and Projection (UMAP) is a general-purpose dimension reduction algorithm. Similar to t-distributed stochastic neighbor embedding (t-SNE), you can use UMAP to visualize the relationships between datapoints. In this example, we are training a three-component UMAP model on MNIST datasets and then displaying the 3D graph of the result. The color of the point in the graph is based on the label. In the resulting graph, blobs of colors show that UMAP correctly clustered the datapoints.
    """
)


@st.cache
def load_data(selected_dataset):
    if selected_dataset == "MNIST-Digits":
        X = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/mnist-1000-input.csv"
        )
        y = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/mnist-1000-labels.csv"
        )
        y = np.unique(y, return_inverse=True)[1]

    elif selected_dataset == "MNIST-Fashion":
        X = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/fashion-1000-input.csv"
        )
        y = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/fashion-1000-labels.csv"
        )
        y = np.unique(y, return_inverse=True)[1]

    else:
        X = None
        y = None

    return X, y


@st.cache
def create_figure(X, y):
    umap_3d = UMAP(n_components=3, init="random", random_state=0)
    proj_3d = umap_3d.fit_transform(X, y=y)

    fig = px.scatter_3d(proj_3d, x=0, y=1, z=2, color=y)
    fig.update_layout(transition_duration=500, height=1000)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(marker_size=2)

    return fig


col1, col2 = st.columns([1, 3])


with col1:

    selected_dataset = st.selectbox("Please select a dataset:", ("MNIST-Digits", "MNIST-Fashion"))

    data_load_state = st.text("Loading data...")
    X, y = load_data(selected_dataset)
    data_load_state.text("Done loading data!")

with col2:
    fig = create_figure(X, y)
    plot_3d = st.plotly_chart(create_figure(X, y), use_container_width=True)
