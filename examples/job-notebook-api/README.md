# Example Job API

This notebook is an example of one you might want to run as an API. We will deploy it as a Saturn Cloud Job which has an HTTP endpoint to trigger it running. While Saturn Cloud jobs are normally run either on a schedule or by pressing the start button, they do have the ability to also be triggered by a HTTP request as an API.

The only thing the notebook does in this example is writes a line to the logs (you probably want to make it do more interesting things in practice).

## Set up the job

_(By using the recipe file included in this example you can skip this setup step)_

In Saturn Cloud, create a new **Job resource** that has the following options:

* **Run Command**: `papermill example.ipynb out.ipynb --stdout-file - --stderr-file - --kernel python3`
* **Home Directory**: `/home/jovyan/examples/examples/job-notebook-api`
* **Extra Packages**: `papermill` (as a pip package)

Then, in the **git repositories** of the resource, use this materials resource as a connected repository (`git@github.com:saturncloud/examples.git`). In practice, you'd want to use your own git repo with your particular notebook. 

This will set up the job that when triggered runs the notebook. This will use the papermill package to execute a notebook and record the output.

## Execute the job

If you want to manually run the job, you can press the green start button in the resource page of Saturn Cloud. To run it programmatically, you need a few things:

* **Your saturn instance string** - each Saturn Cloud enterprise account has a unique name that's needed for the API requests. When you log into Saturn Cloud you can get it from the url: `https://app.{saturn_instance}.saturnenterprise.io`.
* **User token** - this is needed to authenticate the request. Get your user token for Saturn Cloud using `https://app.{saturn_instance}.saturnenterprise.io/api/user/token` where again the Saturn Cloud instance is specific to your company. The token is the hexadecimal value in quotes.
* **Resource ID** - the ID of the job can be found in the URL on the resource page for the job. The URL will be something like `https://app.{saturn_instance}.saturnenterprise.io/dash/resources/job/{job_id}` where the job ID is a long hexadecimal value.

With those, you can kick off the job using a HTTP POST request with an empty body. In Python it would be done using the following parameters:

```python
import requests

saturn_instance = "yoursaturninstance"
user_token = "youusertoken" # (don't save this directly in a file!)
job_id = "yourjobid"

url = f'https://app.{saturn_instance}.saturnenterprise.io/api/jobs/{job_id}/start'
headers={"Authorization": f"token {user_token}"}
r = requests.post(url, headers=headers)
```

You can see the logs from the previous execution by clicking the **Status** link on the job page.
