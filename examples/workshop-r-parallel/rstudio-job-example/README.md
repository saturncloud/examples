# RStudio Job Example

This example is how to use RStudio jobs to run ad hoc tasks on request in the background.


Suppose we have a long running report `complex-report.Rmd`, and we want to run it with a bunch of different
parameter sets, in this case with `func` taking a value of 0.1, 0.5, or 1.0. We can write a script to generate
each version of the report (`generate-report-xx.R` where `xx` is the value), but rather than running each 
script one at a time let's run them in parallel with RStudio Jobs. Use `rstudio-job-example.R` as a script
that will start a job for each different report generation.

_The solution can be found in `rstudio-job-example-solutions.R`._