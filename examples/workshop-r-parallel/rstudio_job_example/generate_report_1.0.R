rmarkdown::render("rstudio_job_example/complex_report.Rmd",
                  output_file = "results_1.0.html",
                  params = list(frac = 1.0))
