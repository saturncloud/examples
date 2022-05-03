using AWS
using AWSS3
using CSV
using Dash
using DataFrames
using PlotlyJS
using UMAP

app = dash()
app.title = "UMAP Projections"

app.layout = html_div() do
    children = [
        html_div(
            children=[
                html_h1(
                    "UMAP Projections for MNIST and Fashion-MNIST Datasets",
                    style=("text-align" => "center"),
                ),
                dcc_markdown(
                    """
                    Uniform Manifold Approximation and Projection (UMAP) is a general-purpose dimension reduction algorithm. Similar to t-distributed stochastic neighbor embedding (t-SNE), you can use UMAP to visualize the relationships between data points. In this example, we are training a three-component UMAP model on MNIST datasets and then displaying the 3D graph of the result. The color of the point in the graph is based on the label. In the resulting graph, blobs of colors show that UMAP clustered data points with similar labels together.
                """,
                ),], style=("padding" => 10),
        ),
        html_div(
            children=[
                html_div(
                    children=[
                        html_h1("Input"),
                        html_label("Dataset"),
                        dcc_dropdown(
                            options=[
                                Dict("label" => "MNIST-Digits", "value" => "MNIST-Digits"),
                                Dict("label" => "MNIST-Fashion", "value" => "MNIST-Fashion")
                            ],
                            value="MNIST-Fashion",
                            id="dataset_dropdown"),
                    ], style=(width="24%", display="inline-block")
                ),
                html_div(
                    children=[
                        html_h1("Output"),
                        dcc_loading(
                            id="loading-1",
                            children=[dcc_graph(id="graph")],
                            type="circle"
                        )
                    ], style=(width="74%", height="1000px", display="inline-block", float="right")
                )]
        )
    ]
end

callback!(
    app,
    Output("graph", "figure"),
    Input("dataset_dropdown", "value"),
) do selected_dataset
    if selected_dataset == "MNIST-Digits"
        X = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/mnist-1000-input.csv", config=global_aws_config(; creds=nothing, region="us-east-2")))))
        y = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/mnist-1000-labels.csv", config=global_aws_config(; creds=nothing, region="us-east-2")))))

    elseif selected_dataset == "MNIST-Fashion"
        X = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/fashion-1000-input.csv", config=global_aws_config(; creds=nothing, region="us-east-2")))))
        y = DataFrame(CSV.File(AWSS3.read(S3Path(
            "s3://saturn-public-data/MNIST-1000/fashion-1000-labels.csv", config=global_aws_config(; creds=nothing, region="us-east-2")))))
    end

    embedding = umap(transpose(Matrix(X)), 3, ; n_neighbors=10, min_dist=0.001, n_epochs=200)

    data = DataFrame(hcat(transpose(embedding), y."0"), :auto)

    fig = plot(
        data,
        x=:x1,
        y=:x2,
        z=:x3,
        color=:x4,
        mode="markers",
        marker=attr(size=2),
        type="scatter3d",
        Layout(height=1000))

    return fig

end

run_server(app, "0.0.0.0", 8000)