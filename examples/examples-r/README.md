<img src="https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/saturn.png" width="600" />

# Start Using R in Saturn Cloud
## Welcome to Saturn Cloud!

This project gives you an environment ready for conducting data science in R in Jupyter. Open a new notebook and select the R kernel to begin.

The following libraries are included in the image, and you can install others with `install.packages()`, `devtools`, or `remotes` according to your preference.

The following packages and all of their `Imports`, `Depends`, and `LinkingTo` dependencies are included in the image.

>To see the full list of installed packages, run the following in an R session in Jupyter.  
>`as.data.frame(installed.packages())[, c("Package", "Version")]`

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

## Next steps

Thanks for trying out this project! To learn more about how Saturn Cloud works, check out our [Documentation](https://www.saturncloud.io/docs/), [blog](https://www.saturncloud.io/s/blog/), or join an [upcoming event](https://www.saturncloud.io/s/events/).

If you have any questions or suggestions for example projects, reach out to us at support@saturncloud.io or open an issue on the [examples Github repo](https://github.com/saturncloud/examples).
