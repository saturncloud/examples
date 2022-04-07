results <- lintr::lint_dir(
  linters =
    lintr::with_defaults(line_length_linter = lintr::line_length_linter(100)),
  pattern = "\\.(R|r|Rmd|rmd)"
)

print(results)

error_count <- sum(sapply(results, function(x) x$type) != "warning")

if(error_count > 0){
  stop("R/Rmd files failed linting")
}
