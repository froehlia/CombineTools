# Combine Tools
A collection of tools for post processing of HiggsCombine results.


## Limit Plots
To create limit plots, use the `plotting/limit_plot.py` script.
The script creates limit plots using data from .csv files.
It requires a config file in the YAML format.

An example for the input files is found in `examples/`:
```
python plotting/limit_plot.py examples/example_limit_config.yml
```

## Nuisance Pulls
Create nuisance pull plots with the `plotting/nuisance_plot.py` script.

Example:
```
python plotting/nuisance_plot.py examples/example_nuisance_pull.csv
```
