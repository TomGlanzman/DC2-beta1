# coriSetup.sh - cori-specific configs for phoSim and DMTCP
module swap PrgEnv-intel PrgEnv-gnu
module swap gcc gcc/5.2.0
module rm craype-network-aries
module rm cray-libsci
module unload craype
module load python/2.7-anaconda
export CC=gcc
