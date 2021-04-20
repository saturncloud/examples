# Start Using R in Saturn Cloud

Welcome! This project gives you an environment ready for conducting data science in R in Jupyter. Open a new notebook and select the R kernel to begin.

The following libraries are included in the image, and you can install others with `install.packages()`, `devtools`, or `remotes` according to your preference.

* caret
* data.table
* devtools
* dplyr
* ggplot2
* IRkernel
* keras
* lightgbm
* lubridate
* Rcpp
* readr
* remotes
* reticulate
* stringr
* tensorflow
* tidyr
* xgboost 

R is not compatible with Dask or Dask clusters, so you will not be able to take advantage of parallelization with Dask in R. However, we have provided the `reticulate` library, which can enable interaction between R and Python code.

