<img src="https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/saturn.png" width="600" />

# R in Saturn Cloud

This resource gives you an environment ready for conducting data science in R in Jupyter. Open a new notebook and select the R kernel to begin.

The following packages and all of their `Imports`, `Depends`, and `LinkingTo` dependencies are included in the image.

>To see the full list of installed packages, run the following in an R session in Jupyter.
> `as.data.frame(installed.packages())[, c("Package", "Version")]`
> You can install other libraries with `install.packages()`, `devtools`, or `remotes` according to your preference.

* data.table
* devtools
* IRkernel
* tidyverse (full installation including dplyr, ggplot2, and other packages)
* lubridate
* Rcpp
* remotes
* reticulate

R is not compatible with Dask or Dask clusters, so you will not be able to take advantage of parallelization with Dask in R. However, we have provided the `reticulate` library, which can enable interaction between R and Python code.

## Next steps

Thanks for trying out this resource! To learn more about how Saturn Cloud works, check out our [Documentation](https://saturncloud.io/docs/), [blog](https://saturncloud.io/s/blog/), or join an [upcoming event](https://saturncloud.io/s/events/).

If you have any questions or suggestions reach out to us at support@saturncloud.io or open an issue on the [examples Github repo](https://github.com/saturncloud/examples).
