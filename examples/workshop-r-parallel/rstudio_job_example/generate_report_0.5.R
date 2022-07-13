rmarkdown::render("rstudio_job_example/complex_report.Rmd",
                  output_file = "results_0.5.html",
                  params = list(frac = 0.5))
