## phosimSetup.sh - establish cori environment to run phoSim (and DMTCP)

## Select phoSim version
version=v3.7.1   # Nov 2017

## Select compiler used to build phoSim
#compiler=gcc
compiler=intel

## Determine if running on knl, or haswell node, and whether batch or
## interactive
node=haswell
mode=batch
if [[ ! -z "$SLURM_JOB_PARTITION" ]]; then
#    if echo "$SLURM_JOB_PARTITION" | grep -q "knl"; then
    if [[ "$SLURM_JOB_PARTITION" =~ "knl" ]]; then
	node=knl
    fi
else
    mode=interactive
fi


## Code pointers
arch=cori-${node}-${compiler}
export PHOSIM_ROOT=/global/common/software/lsst/${arch}/phosim/${version}
export DMTCP_ROOT=/global/common/cori/contrib/lsst/dmtcp/2.4.5


## Add dummy condor_submit_dag
export PATH=${DC2_ROOT}/bin:$PATH

## Add DMTCP to (MAN)PATH
export PATH=$DMTCP_ROOT/bin:$PATH
export MANPATH=$DMTCP_ROOT/share/man:$MANPATH

## Module shenanigans on cori to run phoSim and DMTCP (checkpointing)
if [ $compiler == 'gcc' ]; then
    module swap PrgEnv-intel PrgEnv-gnu
    module swap gcc gcc/5.2.0
    module rm craype-network-aries
    module rm cray-libsci
    module unload craype
    export CC=gcc
fi

module load python/2.7-anaconda

