
This is a minimal Python package that provides both **command line** and **API** interfaces for removing **multiple** tags from a DAGMC h5m file.

This is useful for preparing the h5m file for visulisation where it is desirable to remove reflecting surfaces, vacuum materials and the graveyard(s) region.


# Command line usage

Perhaps the most common use of this program is to remove a DAGMC graveyard.
```bash
remove-dagmc-tags -i dagmc.h5m -o dagmc_no_graveyard.h5m -t graveyard
```

- the ```-i``` or ```--input``` argument specifies the input h5m file
- the ```-o``` or ```--output``` argument specifies the output h5m file
- the ```-t``` or ```--tags``` argument specifies the tags to remove.
- the ```-v``` or ```--verbose``` argument enables (true) or disables (false) the printing of additional details

Multiple tags can also be removed. This example removes three tags from the dagmc.h5m file

```bash
remove-dagmc-tags -i dagmc.h5m -o dagmc_output.h5m -t mat:graveyard mat:vacuum reflective
```

# Python API usage

Removing a single tag called ```mat:graveyard``` from the dagmc.h5m file.
```python
from remove_dagmc_tags import remove_tags

remove_tags(
    input='dagmc.h5m',
    output='output.h5m',
    tags='mat:graveyard'
)
```

Removing two tags called ```mat:graveyard``` and ```reflective``` from the dagmc.h5m file.
```python
from remove_dagmc_tags import remove_tags

remove_tags(
    input='dagmc.h5m',
    output='output.h5m',
    tags='reflective'
)
```

# Installation

```bash
pip install remove_dagmc_tags
```

Some Python dependencies (such as Numpy) are installed during the ```pip install remove_dagmc_tags process```, however [PyMoab](https://bitbucket.org/fathomteam/moab/src/master/) needs to be installed seperatly to make full use of this package.

One method of installing ```pymoab``` is to compile MOAB with pymoab enabled.

```bash
mkdir MOAB
cd MOAB ; \
mkdir build ; \
git clone  --single-branch --branch develop https://bitbucket.org/fathomteam/moab.git
cd build
cmake ../moab -DENABLE_HDF5=ON \
              -DENABLE_NETCDF=ON \
              -DENABLE_FORTRAN=OFF \
              -DENABLE_BLASLAPACK=OFF \
              -DBUILD_SHARED_LIBS=OFF \
              -DCMAKE_INSTALL_PREFIX=/MOAB
make -j"$compile_cores"
make -j"$compile_cores" install
cmake ../moab -DENABLE_HDF5=ON \
              -DENABLE_PYMOAB=ON \
              -DENABLE_FORTRAN=OFF \
              -DBUILD_SHARED_LIBS=ON \
              -DENABLE_BLASLAPACK=OFF \
              -DCMAKE_INSTALL_PREFIX=/MOAB
make -j"$compile_cores"
make -j"$compile_cores" install
cd pymoab
bash install.sh
python setup.py install
```


# Achknowledgments

The package is largely inspired by the DAGMC-viz(https://github.com/svalinn/DAGMC-viz) repository. 
