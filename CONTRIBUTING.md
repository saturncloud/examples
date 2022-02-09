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

When your pull request is opened, a set of automated checks will run to check that your code conforms with the structure described in ["`examples/` Directory Structure"](#dir-structure).

# Adding a new example <a name="new-example"></a>

When you add a new example, add an entry to [`CODEOWNERS`](./.github/CODEOWNERS) to be sure you'll be added as a reviewer on future updates to it.

## `examples/` Directory Structure <a name="dir-structure"></a>

Examples in the `examples/` directory follow a specific directory structure so that they can be cloned into Saturn from recipes.

Each directory below `examples/` corresponds to one potential resource that users can clone either from the recipe directly, or from a corresponding  resource template.

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
make install test validate
```

If this raises any issues, try automatically fixing them

```shell
make format
```

# Releasing

Releases of this repository lag releases of Saturn Cloud. Anytime after a new release makes it to [hosted](https://app.community.saturnenterprise.io) and you want to take advantage of some new features in it, you can make a release of this repo.

Follow these steps:

1. Create a pull request into `main` which updates all of the `"image_uri"` entries in `saturn.json` files to the latest images released from https://github.com/saturncloud/images (if you want).
2. Create a new branch from `main`. It's name must start with `release-`.

    ```shell
    git pull origin main
    git checkout -b release-2022.01.06
    git push release-2022.01.06
    ```

3. On `main` update RECIPE_SCHEMA_VERSION to the version on [hosted](https://app.community.saturnenterprise.io).
4. Update all the `schema_version` fields in all the recipes and make any changes.
5. Update the button on README.md to point to the new RECIPE_SCHEMA_VERSION
6. Create a pull request with these changes with `main` as the base.

This repo has branch protection to prevent deletion or changes without a pull request on all `release-*` branches.

# Frequently Asked Questions <a name="faq"></a>

#### Can I include other code or add more sub-directories under and example in the `examples/` directory?

All other directories included under the example directory will be included in the example, and an arbitrary amount of nesting is permitted. Non-code files such as data should be stored on S3.

#### What do I do if my example needs a custom image?

All images referenced in an example's `.saturn/saturn.json` should be publicly available on Docker Hub. This repository does not handle building new images.

If you need a new image, you can make a pull request in https://github.com/saturncloud/images to add it.

#### Why does this repository use long-lived release branches instead of GitHub releases and tags on `main`?

Using long-lived release branches allows for the possibility of hot-fixing older versions of this repository if issues arise.
