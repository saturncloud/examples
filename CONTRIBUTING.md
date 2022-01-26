# contributing

This document describes how to contribute to `saturncloud/examples`.

#### Contents

* [Making changes to this repo](#changes)
* [Adding a new example](#new-example)
    - [`examples/` Directory Structure](#dir-structure)
* [Releasing](#releasing)
* [Frequently Asked Questions](#faq)

# Making changes to this repo <a name="changes"></a>

All changes to this repository are required to go through pull requests. Create a new branch, commit your changes, and [submit a pull request](https://github.com/saturncloud/examples/compare).

When your pull request is opened, a set of automated checks will run to check that your code conforms with the structure described in ["Example Directory Structure"](#example-directory-structure).

# Adding a new example <a name="new-example"></a>

When you add a new example, add an entry to [`CODEOWNERS`](./.github/CODEOWNERS) to be sure you'll be added as a reviewer on future updates to it.

## `examples/` Directory Structure <a name="dir-structure"></a>

Examples in this the `examples/` directory follow a specific directory structure that allows Saturn to automatically seed them in a new user's environment with these.

Each directory below `examples/` corresponds to one new resource that will be created in users' environments. Those resources will be named using the directory name, so the names of these directories should have names which only contain lowercase alphanumeric characters and dashes.

```text
examples/
├── api
│   ├── houseprice.py
│   ├── README.md
│   └── .saturn
│       └── saturn.json
├── autoshutoff-jupyter-kernel
│   ├── autoshutoff.py
│   ├── README.md
│   ├── .saturn
│   │   └── saturn.json
│   └── userautoshutoff.py
├── dashboard
│   ├── dashboard.ipynb
│   ├── README.md
│   └── .saturn
│       └── saturn.json
├── dask
│   ├── README.md
│   ├── .saturn
│   │   └── saturn.json
│   └── start-with-dask.ipynb

```

NOTE: this is part of the output from `tree -a examples/`.

To test if you've added a new example correctly, run the following from the root of this repo:

```shell
make test validate
```

If this raises any issues, try automatically fixing them

```shell
make format
```

# Releasing

Releases of this repository follow releases of Saturn Cloud.

When it is time to cut a new release, follow these steps:

1. Create a pull request into `main` which updates all of the `"image_uri"` entries in `saturn.json` files to the latest images released from https://github.com/saturncloud/images (if you want).
1. Create a new branch from `main`. It's name must start with `release-`.

    ```shell
    git pull origin main
    git checkout -b release-2022.01.06
    python .ci/update-references.py release-2022.01.06
    git add *.json
    git commit -m "Update reference in every recipe"
    git push release-2022.01.06
    ```

1. In the private repo with Saturn's backend, update the setting `EXAMPLE_PROJECTS_BRANCH` to this release branch's name.

This repo has a branch protection to prevent deletion or changes without a pull request on all `release-*` branches.

# Frequently Asked Questions <a name="faq"></a>

#### Can I include other code or add more sub-directories under and example in the `examples/` directory?

All other directories included under the example directory will be included in the example, and an arbitrary amount of nesting is permitted. Non-code files such as data should be stored on S3.

#### What do I do if my example needs a custom image?

All images referenced in an example's `.saturn/saturn.json` should be publicly available on Docker Hub. This repository does not handle building new images.

If you need a new image, you can make a pull request in https://github.com/saturncloud/images to add it.

#### Why does this repository use long-lived release branches instead of GitHub releases and tags on `main`?

Using long-lived release branches allows for the possiblility of hotfixing older versions of this repository if issues arise.

Releases of this repository are intended to be tightly coupled to releases of Saturn's main product. Releasing a version of Saturn's main product with code that says "grab the latest commit from a particular branch" allows us to release hotfixes without needing to interrupt any running Saturn installations.
