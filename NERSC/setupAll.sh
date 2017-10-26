### Combined setup for phoSim and dmtcp
## from /global/common/cori/contrib/lsst/phosim/setupPhosim.sh
## and  /global/common/cori/contrib/lsst/dmtcp/setupDMTCP.sh
module swap PrgEnv-intel PrgEnv-gnu
module swap gcc gcc/5.2.0
module rm craype-network-aries
module rm cray-libsci
module unload craype
module load python/2.7-anaconda
export CC=gcc

export PHOSIM_ROOT=/global/common/cori/contrib/lsst/phosim/v3.6
export DMTCP_ROOT=/global/common/cori/contrib/lsst/dmtcp/2.4.5

export PATH=$DMTCP_ROOT/bin:$PATH
export MANPATH=$DMTCP_ROOT/share/man:$MANPATH

#export DMTCP_CHECKPOINT_DIR=$SCRATCH/dmtcp/checkpointDir
#export DMTCP_TMPDIR=$SCRATCH/dmtcp/tmp
#export DMTCP_CHECKPOINT_INTERVAL=300

