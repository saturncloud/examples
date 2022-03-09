# Create A Dashboard on Saturn Cloud Using Dash

![Plotly and Dash logos](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plotly_dash_logo.png)

## Overview
[Plotly's Dash](https://dash.plotly.com/) enables data scientists to produce low-code data apps by abstracting away much of the technologies and protocols required for interactive data visualization. With only a few additional lines of code, data scientists can 

Deploying a Dash app on Saturn Cloud allows for a scalable backend for your app and a url link for dissemination (this sentence sucks).

In this example, we create a simple UI showing a [UMAP](https://umap-learn.readthedocs.io/en/latest/) model projection of the famous MNIST digits and fashion datasets. The app will read in the data, train the model, and output a 3d graph of the result.

## Creating the App
All of our app code is contained in a file called "app.py." To deploy this app on Saturn Cloud, we simply need to call `python app.py` as our command. See the [Saturn Cloud docs](https://saturncloud.io/docs/examples/dashboards/dashboard/) for more detailed instructions for how to deploy this and other dashboards.

The "app.py" file contains several sections to create the Dash app. 

### Imports

This exercise uses Dash and UMAP to create a dashboard app:
* [dash](https://dash.plotly.com/): low-code data app framework
* [UMAP](https://umap-learn.readthedocs.io/en/latest/): dimensionality reduction and visualization

``` python
import base64
import time
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from PIL import Image
from umap import UMAP
```
### Define the App and Layout

Next, we define the app and then specify the layout. Some of this might seem familiar if you are used to working with HTML. Dash uses functions like `html.div` to define html components (in this case a `div`). 

We also are using Dash Core Components (`dcc`) such as `Dropdown` and `Graph` to define our user input and output components. `dcc` also allows you to use markdown!

This example creates two columns. The first contains a dropdown for the user to select a dataset and the second a visualization of the UMAP projection.

See the [Dash documentation](https://dash.plotly.com/) for more information about how to define specific layouts.

``` python
app = Dash(__name__)
app.title = "UMAP Projections"

app.layout = html.Div(
    [
        html.Div(
            children=[
                html.H1(
                    "UMAP Projections for MNIST and Fashion-MNIST Datasets",
                    style={"text-align": "center"},
                ),
                dcc.Markdown(
                    """
                    Uniform Manifold Approximation and Projection (UMAP) is a general-purpose dimension reduction algorithm. Similar to t-distributed stochastic neighbor embedding (t-SNE), you can use UMAP to visualize the relationships between datapoints. In this example, we are training a three-component UMAP model on MNIST datasets and then displaying the 3D graph of the result. The color of the point in the graph is based on the label. In the resulting graph, blobs of colors show that UMAP correctly clustered the datapoints.
                """,
                ),
            ],
            style={"padding": 10},
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
                            children=[dcc.Graph(id="graph", style={"height": "60vh"})],
                            type="circle",
                        ),
                        html.Center(html.H3("Loading...", id="out_message")),
                    ],
                    style={"padding": 10, "flex": 3},
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
    ]
)
```

### Define the Callbacks
Dash uses callbacks to run functions based on user input. For this example, we define a single callback to update the graph when the dataset changes.

Dash uses `Input` and `Output` to define callback inputs and outputs. The first parameter is the id of the associated component in the layout and the second is the type of information passed to and from the function.

For this example, the callback downloads the correct dataset based on the dropdown selection, runs `fit_transform` on the dataset to create the projection, and finally creates a 3D scatter plot of the result. This function is timed to give the user feedback. 

``` python
@app.callback(
    Output("graph", "figure"),
    Output("out_message", "children"),
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

    return fig, out_msg
```

### Run the App

Finally, we define the code to run the app. The important point here are the host and port numbers. For deployments to work on Saturn Cloud, the host value must be `"0.0.0.0"` and the port number `8000`. 

``` python
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8000", debug=True)
```

We then only need to load the app code and data to github and to link the code appropriately to a Saturn Cloud deployment. 

[Click here]("https://app.community.saturncloud.org/dash/resources?recipeUrl=https://raw.githubusercontent.com/saturncloud/examples/main/examples/dashboard-dash/.saturn/saturn.json") to see how this is accomplished, or simply click [this link]() to see and interact with the dashboard. 

## Conclusion
Dash makes it easy to develop interactive apps and Saturn Cloud makes it easy to deploy these apps. Check out our other [dashboard resources](https://saturncloud.io/docs/examples/python/production/) for examples using other frameworks.