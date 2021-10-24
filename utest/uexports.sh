#! /bin/sh


export C_INCLUDE_PATH=/home/slab/src/testu1/include:${C_INCLUDE_PATH}
export LD_LIBRARY_PATH=/home/slab/src/testu1/lib64:${LD_LIBRARY_PATH}
export LIBRARY_PATH=/home/slab/src/testu1/lib64:${LIBRARY_PATH}
sudo ldconfig
