# pyncorr
A python implementation for calculating n-pt correlation functions relevant to understanding the large-scale structure of galaxy clustering. 


# Install

Clone this repository

```
cd pyncorr

python setup.py install
```

# Download the SDSS sample files
*Note that there is some test data in this repository*

You only need to do this once

```
cd pyncorr/scripts

sh download_sdss_data_and_mocks_for_testing.sh
```

# Test

## Plotting
```
cd pyncorr/scripts

python plot_data.py
```

Note that the input files are hardcoded. You can edit them in the script to look 
at different data/random files. 


## Correlation functions

Just as with the ```plot_data.py``` script, the input files are hardcoded. When you first check out this
repository, they should be edited to use datasets that take seconds to run. 

### Cartesian 2pcf
```
cd pyncorr/scripts

python cartesian_2pcf.py

```

### Angular 2pcf
```
cd pyncorr/scripts

python angular_2pcf.py

```

Note that these scripts automatically write out the summary files for the pair counts as

```
dd.dat
rr.dat
dr.dat
```

And these can be plotted (filenames are hardcoded in the script) on their own, if you don't want to rerun
all the calculations.

```
python plot_results.py
```

## Correlation functions with voxelized approach...

***Coming soon...***
