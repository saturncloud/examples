# Single-Node Bodo - Python Script

This example shows how to do manipulate data using the HPC-like platform Bodo using on a single node.
Using Bodo can be a straightforward way to make Python code run faster that it would otherwise without requiring much change to the code.

**The Bodo parallel cluster in this example runs within the same Saturn Cloud resource as the python script calling it.** 
Thus, to increase the performance of the Bodo cluster you only need to increase the instance size of the Jupyter Server resource it's running on.

To run Python scripts with Bodo, use `mpiexe` from the command line and specify the number of parallel processes you would like to use:

```shell
mpiexec -n 8 python bodo-terminal-example/example.py
```
