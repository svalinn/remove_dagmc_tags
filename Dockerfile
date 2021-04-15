# This Dockerfile creates an enviroment for testing the python package
# remove_dagmc_tags

FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y

# RUN apt-get install -y libgl1-mesa-glx libgl1-mesa-dev libglu1-mesa-dev \
#                        freeglut3-dev libosmesa6 libosmesa6-dev \
#                        libgles2-mesa-dev curl && \
#                        apt-get clean


# # Install neutronics dependencies from Debian package manager
# RUN if [ "$include_neutronics" = "true" ] ; \
#     then echo installing with include_neutronics=true ; \
#          apt-get install -y \
#             wget git gfortran g++ cmake \
#             mpich libmpich-dev libhdf5-serial-dev libhdf5-mpich-dev \
#             imagemagick ; \
#     fi

# # install addition packages required for MOAB
RUN apt-get --yes install libeigen3-dev && \
    apt-get --yes install libblas-dev && \
    apt-get --yes install liblapack-dev && \
    apt-get --yes install libnetcdf-dev && \
    apt-get --yes install libtbb-dev && \
    apt-get --yes install libglfw3-dev

# Clone and install MOAB

RUN pip install --upgrade numpy cython && \
    mkdir MOAB && \
    cd MOAB && \
    mkdir build && \
    git clone  --single-branch --branch 5.2.1 --depth 1 https://bitbucket.org/fathomteam/moab.git && \
    cd build && \
    cmake ../moab -DENABLE_HDF5=ON \
                  -DENABLE_NETCDF=ON \
                  -DENABLE_FORTRAN=OFF \
                  -DENABLE_BLASLAPACK=OFF \
                  -DBUILD_SHARED_LIBS=OFF \
                  -DCMAKE_INSTALL_PREFIX=/MOAB && \
    make 2 && \
    make 2 install && \
    rm -rf * && \
    cmake ../moab -DENABLE_HDF5=ON \
                  -DENABLE_PYMOAB=ON \
                  -DENABLE_FORTRAN=OFF \
                  -DBUILD_SHARED_LIBS=ON \
                  -DENABLE_BLASLAPACK=OFF \
                  -DCMAKE_INSTALL_PREFIX=/MOAB && \
    make 2 && \
    make 2 install
    
    # cd pymoab && \
    # bash install.sh && \
    # python setup.py install
