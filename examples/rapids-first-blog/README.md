# Supporting Code for the Blog Post: My First Experience Using RAPIDS

<img src="https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/rapids.png" width="400">

[RAPIDS](https://rapids.ai/) is a collection of libraries that enable you to take advantage of NVIDIA GPUs to accelerate machine learning workflows. Minimal changes are required to transition from familiar pandas and scikit-learn to GPU accelerated code! For more information on RAPIDS, see ["Getting Started"](https://rapids.ai/start.html) in the RAPIDS docs.


These are supporting files for the Saturn Cloud blog post: [My First Experience Using RAPIDS](https://saturncloud.io/blog/my-experience-of-first-time-using-rapids/).
## [Use Pandas and sklearn](01-python-train.ipynb)

This notebook gives an example of creating a regression model to predict the price of train tickets using pandas dataframe and sklearn. It has no RAPIDS code, it's only the comparison point for RAPIDS.

## [Use RAPIDS CuDF and CuML](02-rapids-train.ipynb)

This notebook gives an example of creating a regression model to predict the price of train tickets using CuDF dataframe and CuML. Hence instead of utilizing CPUs our computations will run on GPUs.