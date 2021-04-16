[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)
[![docker based CI](https://github.com/Shimwell/remove_dagmc_tags/actions/workflows/docker_ci.yml/badge.svg)](https://github.com/Shimwell/remove_dagmc_tags/actions/workflows/docker_ci.yml)
[![PyPI](https://img.shields.io/pypi/v/remove-dagmc-tags?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/remove-dagmc-tags/)
[![codecov](https://codecov.io/gh/shimwell/remove_dagmc_tags/branch/main/graph/badge.svg)](https://codecov.io/gh/shimwell/remove_dagmc_tags)

This is a minimal Python package that provides both **command line** and **API** interfaces for removing **multiple** tags from a DAGMC h5m file.

This is useful for preparing the h5m file for visulisation where it is desirable to remove reflecting surfaces, vacuum materials and the graveyard(s) region
from the geometry before viewing the vtk file.


# Command line usage

Perhaps the most common use of this program is to remove a DAGMC graveyard.
```bash
remove-dagmc-tags -i dagmc.h5m -o dagmc_no_graveyard.h5m -t graveyard
```

- the ```-i``` or ```--input``` argument specifies the input h5m file
- the ```-o``` or ```--output``` argument specifies the output h5m or vtk filename
- the ```-t``` or ```--tags``` argument specifies the tags to remove.
- the ```-v``` or ```--verbose``` argument enables (true) or disables (false) the printing of additional details

Multiple tags can also be removed and vtk files can be generated. This example
removes three tags from the dagmc.h5m file and saves the result as a vtk file.

```bash
remove-dagmc-tags -i dagmc.h5m -o output.vtk -t mat:graveyard mat:vacuum reflective
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

Removing two tags called ```mat:graveyard``` and ```reflective``` from the
dagmc.h5m file and saves the result as a vtk file and h5m file.

```python
from remove_dagmc_tags import remove_tags

remove_tags(
    input='dagmc.h5m',
    output=['output.vtk', 'output.h5m'],
    tags=['reflective', 'mat:graveyard']
)
```

# Installation

The recommended method of installing is via conda install as this is able to
install all the dependencies including PyMoab.
```bash
conda install -c conda-forge remove_dagmc_tags
```

However the package is available via the PyPi package manager. In this case you
will have to seperatly install PyMoab.

```bash
pip install remove_dagmc_tags
```

Some Python dependencies (such as Numpy) are installed during the ```pip install remove_dagmc_tags process```, however [PyMoab](https://bitbucket.org/fathomteam/moab/src/master/) needs to be installed seperatly to make full use of this package.


One method of installing ```pymoab``` is to install MOAB via Conda which
includes PyMoab.

```bash
conda install -c conda-forge moab
```

Another method of installing ```pymoab``` is to compile MOAB with pymoab enabled.

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
