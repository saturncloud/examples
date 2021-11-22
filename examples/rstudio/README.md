<img src="https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/rstudio.png" width="600" />

# RStudio in Saturn Cloud

This resource gives you an environment ready for conducting data science in RStudio.

The following packages and all of their `Imports`, `Depends`, and `LinkingTo` dependencies are included in the image.

* data.table
* devtools
* IRkernel
* tidyverse (full installation including dplyr, ggplot2, and other packages)
* lubridate
* Rcpp
* remotes
* reticulate

To see the full list of installed packages, run the following in an R session in RStudio.
`as.data.frame(installed.packages())[, c("Package", "Version")]`. You can install other libraries with `install.packages()`, `devtools`, `remotes` or other commands. Note that those will only stay installed until you turn off the resource--to install packages permanently see our documentation on [installing software to Saturn Cloud resources](https://saturncloud.io/docs/using-saturn-cloud/install-packages/).