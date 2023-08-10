# Registering Users

This example illustrates how to write a script to register users in Saturn Cloud.

This example takes a list of email addresses (passed in via an `EMAILS_FOR_ACCOUNTS` environment variable). It will check if a user account exists or not, and if not, create an account for the user. The reason we are passing this in via an ENV var is so that we can pass this via the Saturn secrets manager.
