# Auto-shutoff based on Jupyter kernel inactivity

This repository contains a Saturn Cloud job which can be run to shut down any Jupyter Server resources where all the kernels
are idle. The process works by having an admin user create login credentials for each user on the application, then queries their
resources on their behalf to shutdown the ones that have idled for too long. The job turns off any
resources that have been idling for too long based on the resources auto-shutoff variable. You can set it up to run on a recurring
schedule in the UI.

## Installation

The `saturn.json` recipe file can be used to load this job into a Saturn Cloud application. The Saturn Cloud Data Science team
can help set this up.

You'll need to also set the admin user to use to run the job. Once you've picked a user, get their access token by having the user
log in then navigate to https://app.{organization}.saturnenterprise.io/api/user/token --once you have the hexidecimal token, save it as
a Saturn Cloud environment variable credential with the name `ADMIN_ACCESS_TOKEN`

## Notes

* There is an edge case where you have Jupyter Server which is online but doesn't have any kernels at all--such as
when someone has turned on a resource but hasn't used it yet. It's not clear what the "correct" behavior is. This script does not
attempt to turn off these servers, but the script could be adjusted to handle them if needed. Since this script doesn't turn off
those resources, they'll still be caught by the built in Saturn Cloud auto-shutoff functionality.
* This script does not attempt to shut off group-level resources, since they are often used for production systems. This script
could be adjusted to included that functionality if desired.
