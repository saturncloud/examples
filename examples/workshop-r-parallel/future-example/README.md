# future Example

This example is how to use future to split up a task within an R session by passing parts 
of it to different sessions. Here we have a large dataset `data`, that within it has
retail transaction data (the date, revenue, customer, region, etc.). We want to
figure out, for each customer, how long it was between their first and second purchases.
If we just use standard dplyr, that computation will take a minute. The goal is instead
to make the command happen faster by computing the times across multiple processors.
First we'll try with future and then with furrr.

The completed example can be found in `future-example-solutions.R`.