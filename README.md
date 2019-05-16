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

```
cd pyncorr/scripts

python plot_data.py
```

Note that the input files are hardcoded. You can edit them in the script to look 
at different data/random files. 
