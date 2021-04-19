# This Dockerfile creates an enviroment for testing the python package
# remove_dagmc_tags

FROM continuumio/miniconda3:4.9.2

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y

# install addition packages required for MOAB
RUN apt-get --yes install libeigen3-dev && \
    apt-get --yes install libblas-dev && \
    apt-get --yes install liblapack-dev && \
    apt-get --yes install libnetcdf-dev && \
    apt-get --yes install libtbb-dev && \
    apt-get --yes install libglfw3-dev && \
    apt-get --yes install cmake && \
    apt-get --yes install g++ && \
    apt-get --yes install git

# Clone and install MOAB
RUN pip install --upgrade numpy cython
RUN mkdir MOAB && \
    cd MOAB && \
    git clone  --single-branch --branch 5.2.1 --depth 1 https://bitbucket.org/fathomteam/moab.git

RUN cd MOAB && \
    mkdir build && \
    cd build && \
    cmake ../moab -DENABLE_HDF5=ON \
                  -DENABLE_NETCDF=ON \
                  -DENABLE_FORTRAN=OFF \
                  -DENABLE_BLASLAPACK=OFF \
                  -DBUILD_SHARED_LIBS=OFF \
                  -DCMAKE_INSTALL_PREFIX=/MOAB && \
    make &&  \
    make install && \
    cmake ../moab -DENABLE_HDF5=ON \
                  -DENABLE_PYMOAB=ON \
                  -DENABLE_FORTRAN=OFF \
                  -DBUILD_SHARED_LIBS=ON \
                  -DENABLE_BLASLAPACK=OFF \
                  -DCMAKE_INSTALL_PREFIX=/MOAB && \
    make install && \
    cd pymoab && \
    # not quite sure why these two lines are needed but it appears that pymoab
    # is not available as "import pymoab" without them
    bash install.sh && \
    python setup.py install

RUN pip install pytest-cov

COPY setup.py setup.py
COPY remove_dagmc_tags remove_dagmc_tags/
COPY tests tests/
COPY README.md README.md

RUN python setup.py develop

CMD pytest tests -v --cov=remove_dagmc_tags --cov-report term --cov-report xml ; mv coverage.xml /share/coverage.xml
