# callr Example

This example is how to use callr to run a task in the background of a Shiny app. 

Suppose we have a shiny app that we want to add a button that starts a long-running
R task. We want it so when users press the button, it doesn't freeze the whole app.
Instead, the task runs in the background while other things happen. The objective
here is to add to `app.R` the code that causes the `process_the_data` command to
run silently.

The final app can be found in `app-solutions.R`.