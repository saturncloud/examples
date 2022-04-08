results <- lintr::lint_dir(
  linters =
    lintr::with_defaults(line_length_linter = lintr::line_length_linter(100)),
  pattern = "\\.(R|r|Rmd|rmd)"
)

non_warning_results <- results[sapply(results, function(x)x$type != "warning")]

print(non_warning_results)

if(length(non_warning_results) > 0){
  stop("R/Rmd files failed linting")
}
