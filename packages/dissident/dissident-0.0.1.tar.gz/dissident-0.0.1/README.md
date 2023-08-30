# Dissident Package

> This package is part of the dissertation of Evgeny Noi, who is working at UC Santa Barbara MoveLab with Dr. Dodge and Dr. Murray on context-aware movement analytics.

## Visualizing spatial and temporal coverage in SG and MB

- [ ] Partition space based on counties, tracts, block groups and blocks and map percentage of non-missing values for the observation period (2019-mid 2021)  

## Setting up computational environment

Python environment management is handled via Mamba. Dependencies are managed by Poetry. This is an experimental set-up.

### Initial Set-up

**Since the initial set-up for this package was done on Windows I record the instructions on how to run initial set-up of a computational environment on Windows.

1. Install Mambaforge by following the instructions in the [official docs](mamba activate dissident).

```bash
mamba create -n "dissident"

mamba activate dissident

mamba install geopandas

pip install matcouply

mamba install mercantile osmnx

mamba install xarray dask netCDF4 bottleneck ipykernel contextily
```

2. Create an ipy kernel 

```bash
python -m ipykernel install --user --name dissident --display-name "Python (dissident)"
```

3. Export the env requirements you can use mamba to create a .yml file. Because the env is create on Windows we NEED to add --from-history, otherwise it fails. 

```bash
mamba env export --from-history > environment.yml
```

4. Create a Github repo in the existing project and push to Github. On Windows - simply use Github Desktop. 
5. Clone the repo on the server using ```bash git clone```. 
6. Create a computational environment on server 
```bash
micromamba env create -f environment.yml
```

## What's included

### Utility Functions
