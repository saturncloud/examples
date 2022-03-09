# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from umap import UMAP
import time
from PIL import Image
import base64
from io import BytesIO


def numpy_to_b64(array, scalar=True):
    # Convert from 0-1 to 0-255
    if scalar:
        array = np.uint8(255 * array)

    im_pil = Image.fromarray(array)
    buff = BytesIO()
    im_pil.save(buff, format="png")
    im_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")
    return im_b64


app = Dash(__name__)
app.title = "UMAP Projections"

app.layout = html.Div(
    [
        html.Div(
            children=[html.Center(html.H1("UMAP Projections for MNIST and Fashion-MNIST Datasets"))]
        ),
        html.Div(
            [
                html.Div(
                    children=[
                        html.H1("Input"),
                        html.Label("Dataset"),
                        dcc.Dropdown(["MNIST", "Fashion-MNIST"], "MNIST", id="dataset_dropdown"),
                    ],
                    style={"padding": 10, "flex": 1},
                ),
                html.Div(
                    children=[
                        html.H1("Output"),
                        dcc.Loading(
                            id="loading-1",
                            children=[dcc.Graph(id="graph", style={"height": "80vh"})],
                            type="circle",
                        ),
                        html.Center(html.H3("Loading...", id="out_message")),
                    ],
                    style={"padding": 10, "flex": 2},
                ),
                html.Div(
                    children=[html.H1("Individual Value"), html.Div(id="encoded_image"),],
                    style={"padding": 10, "flex": 1},
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
        dcc.Store(id="images"),
    ]
)


@app.callback(
    Output("graph", "figure"),
    Output("out_message", "children"),
    Output("images", "data"),
    Input("dataset_dropdown", "value"),
)
def update_figure(selected_dataset):
    t0 = time.time()
    if selected_dataset == "MNIST":
        X = pd.read_csv("data/mnist_1000_input.csv")
        y = pd.read_csv("data/mnist_1000_labels.csv")
        y = np.unique(y, return_inverse=True)[1]

    elif selected_dataset == "Fashion-MNIST":
        X = pd.read_csv("data/fashion_1000_input.csv")
        y = pd.read_csv("data/fashion_1000_labels.csv")
        y = np.unique(y, return_inverse=True)[1]

    umap_3d = UMAP(n_components=3, init="random", random_state=0)

    proj_3d = umap_3d.fit_transform(X, y=y)

    fig = px.scatter_3d(proj_3d, x=0, y=1, z=2, color=y)

    fig.update_layout(transition_duration=500, clickmode="event+select")
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(marker_size=2)

    t1 = time.time()
    out_msg = f"Projected in {t1-t0:.2f}s."

    return fig, out_msg, X.to_json()


@app.callback(
    Output("encoded_image", "children"), Input("graph", "clickData"), Input("images", "data")
)
def display_click_data(clickData, X):
    if clickData:
        X = pd.read_json(X)
        img_array = np.reshape(X.loc[clickData["points"][0]["pointNumber"], :].to_numpy(), [28, 28])
        encoded_img = numpy_to_b64(img_array)
        return html.Img(
            src="data:image/png;base64, " + encoded_img,
            style={"height": "25vh", "display": "block", "margin": "auto"},
        )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8000", debug=True)
