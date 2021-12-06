# Machine Learning on Unstructured Data with Saturn Cloud and Snowflake
## Supplementary Materials

This repository contains scripts to accompany the [Snowflake quickstart](https://quickstarts.snowflake.com/guide/machine_learning_with_saturncloud/index.html) on using Snowflake and Saturn Cloud together for machine learning on unstructured data (in this case, image files). 

Image files are stored in a Snowflake data table, and results of inference are saved back to Snowflake at the end of the project. A pretrained model state dict is provided in the `model` folder for users who don't want to wait on training their own.

* Model training: [training.py](training.py)
* Parallelize inference on Dask: [inference.ipynb](inference.ipynb)
* PyTorch data class for Snowflake stored image files: [pytorchsnowflake.py](pytorchsnowflake.py)

Use these files along with [our full guide on the Snowflake website](https://quickstarts.snowflake.com/). 