# Bodo Examples

Welcome to Bodo examples! These are adapted from the [bodo.ai example repository](https://github.com/Bodo-inc/Bodo-examples).

>**Note**: Bodo works best for very large datasets, so downloading the data used in the examples can take some time. Please be patient while the datasets download for each example - you will see the speed benefits of Bodo when manipulating the downloaded data.

## Examples
There are two types of examples in this repository - notebooks and scripts.

The notebook examples run in a Jupyter notebook session using iPyParallel.

The script examples run using mpiexec in a terminal environment.

    An example performing NYC taxi daily pickups example:

        # run example on 8 cores
        mpiexec -n 8 python scripts/get_daily_pickups.py


---------------------------
More documentation can be found at http://docs.bodo.ai.

Also take a look at [the bodo tutorial](https://github.com/Bodo-inc/Bodo-tutorial) for more inspiration.