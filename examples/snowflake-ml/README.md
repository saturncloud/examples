<img src="saturncloud-logo.png" alt="Saturn Cloud" width="300"/>


# Machine Learning on Unstructured Data with Saturn Cloud and Snowflake
## Supplementary Materials

Welcome! This repository contains scripts to accompany our guide to using Snowflake and Saturn Cloud together for machine learning on unstructured data (in this case, image files). 

Image files are stored in a Snowflake data table, and results of inference are saved back to Snowflake at the end of the project. A pretrained model state dict is provided in the `model` folder for users who don't want to wait on training their own.

* Model training: [training.py](training.py)
* Parallelize inference on Dask: [inference.ipynb](inference.ipynb)
* PyTorch data class for Snowflake stored image files: [pytorch_snowflake_class.py](pytorch_snowflake_class.py)

Use these files along with [our full guide on the Snowflake website](https://quickstarts.snowflake.com/). 