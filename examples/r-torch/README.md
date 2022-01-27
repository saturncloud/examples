# Train an Torch model with R on a GPU

This example uses the torch R package to train a model on a GPU.
To run it, use a Saturn Cloud resource with the `saturn-rstudio-torch` image.

If you would rather train it on a CPU you can instead use the `saturn-rstudio` image.
You will need to add `torch` as a CRAN extra package to the resource and add
`Rscript -e "torch::install_torch()"` as a line for the startup script.