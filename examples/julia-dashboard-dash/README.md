# Create A Dashboard on Saturn Cloud Using Dash in Julia

![Plotly and Julia logos](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plotly_julia_logo.png "doc-image")

## Overview
With [Dash](https://dash.plotly.com/) by Plotly, data scientists can produce low-code data apps by abstracting away much of the technologies and protocols typically required for interactive data visualization. Deploying a Dash app on Saturn Cloud provides not only a scalable backend for your app but also a url link for dissemination.

In this example, we create a simple UI showing a [Uniform Manifold Approximation and Projection (UMAP)](https://umap-learn.readthedocs.io/en/latest/) model projection of the famous MNIST digits and fashion datasets. The app will read the data, train the UMAP model, and produce a 3D graph of the result using [PlotlyJS](http://juliaplots.org/PlotlyJS.jl/stable/).

## Creating the App
All the app code is contained in a file called "app.jl." To deploy this app on Saturn Cloud, call `julia app.jl` as the command in a Saturn Cloud deployment. See [Saturn Cloud docs](https://saturncloud.io/docs/examples/dashboards/dashboard/) for more detailed instructions on deploying this and other dashboards.

The "app.jl" file contains several sections to create the Dash app. 

### Import the Libraries

This exercise uses Dash, PlotlyJS, and UMAP to create a dashboard app.

``` julia
using AWS
using AWSS3
using CSV
using Dash
using DataFrames
using PlotlyJS
using UMAP
```
### Define the App and Layout

Next, define the app, then specify the layout. Some of this code might seem familiar if you work with HTML. Dash uses functions like `html_div` to define html components. 

You can use Dash Core Components (`dcc`) such as `Dropdown` and `Graph` to define user input and output components.

This example creates two columns. The first contains a dropdown for the user to select a dataset, and the second a visualization of the UMAP projection. The first column consists of the left quarter of the layout and the second the right three quarters.

See the [Dash documentation](https://dash.plotly.com/julia) for more information about defining specific layouts.

``` julia
app = dash()
app.title = "UMAP Projections"

app.layout = html_div() do
    children = [
        html_div(
            children = [
                html_h1(
                    "UMAP Projections for MNIST and Fashion-MNIST Datasets",
                    style = ("text-align" => "center"),
                ),
                dcc_markdown(
                    """
                    Uniform Manifold Approximation and Projection (UMAP) is a general-purpose dimension reduction algorithm. Similar to t-distributed stochastic neighbor embedding (t-SNE), you can use UMAP to visualize the relationships between data points. In this example, we are training a three-component UMAP model on MNIST datasets and then displaying the 3D graph of the result. The color of the point in the graph is based on the label. In the resulting graph, blobs of colors show that UMAP clustered data points with similar labels together.
                """,
                ),], style = ("padding" => 10),
        ),
        html_div(
            children = [
                html_div(
                    children = [
                        html_h1("Input"),
                        html_label("Dataset"),
                        dcc_dropdown(
                            options = [
                                Dict("label" => "MNIST-Digits", "value" => "MNIST-Digits"),
                                Dict("label" => "MNIST-Fashion", "value" => "MNIST-Fashion")
                            ],
                            value = "MNIST-Fashion",
                            id = "dataset_dropdown"),
                    ], style = (width = "24%", display = "inline-block")
                ),
                html_div(
                    children = [
                        html_h1("Output"),
                        dcc_loading(
                            id = "loading-1",
                            children = [dcc_graph(id = "graph")],
                            type = "circle"
                        )
                    ], style = (width = "74%", height = "1000px", display = "inline-block", float = "right")
                )]
        )
    ]
end
```

### Define the Callbacks
Dash uses callbacks to run functions based on user input. For this example, we define a single callback to update the graph when the dataset changes.

Dash uses `Input` and `Output` to define callback inputs and outputs. The first parameter is the id of the associated component in the layout, and the second is the type of information passed to and from the function.

For this example, the callback downloads the correct dataset based on the dropdown selection, runs `umap` on the dataset to create the embedding, converts the resultant embedding to a DataFrame, and finally creates a 3D scatter plot of the result.

``` julia
callback!(
    app,
    Output("graph", "figure"),
    Input("dataset_dropdown", "value"),
) do selected_dataset
    if selected_dataset == "MNIST-Digits"
        X = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/mnist-1000-input.csv", config = global_aws_config(; region = "us-east-2")))))
        y = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/mnist-1000-labels.csv", config = global_aws_config(; region = "us-east-2")))))

    elseif selected_dataset == "MNIST-Fashion"
        X = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/fashion-1000-input.csv", config = global_aws_config(; region = "us-east-2")))))
        y = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/fashion-1000-labels.csv", config = global_aws_config(; region = "us-east-2")))))
    end

    embedding = umap(transpose(Matrix(X)), 3, ; n_neighbors = 10, min_dist = 0.001, n_epochs = 200)

    data = DataFrame(hcat(transpose(embedding), y."0"), :auto)

    fig = plot(
        data,
        x = :x1,
        y = :x2,
        z = :x3,
        color = :x4,
        mode = "markers",
        marker = attr(size = 2),
        type = "scatter3d",
        Layout(height = 1000))

    return fig

end
```

### Run the App

Finally, define the code to run the app. The important points here are the host and port numbers. For users to access the server, the host value must be `"0.0.0.0"` and the port number `"8000"`. `8000` is the only port exposed on Saturn Cloud deployments.

``` julia
run_server(app, "0.0.0.0", 8000)
```

Then load the app code and data to git, and link the code appropriately to a Saturn Cloud deployment. 

Check out our other [Julia examples](https://saturncloud.io/docs/examples/julia/) for more guides on how to use Julia on Saturn Cloud.