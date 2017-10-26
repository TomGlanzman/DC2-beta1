#!/bin/bash
# runE2ADC.sh - set up environment

## General task configuration (for all steps)
source ${DC2_CONFIGDIR}/config.sh

## Setup to run phoSim and DMTCP (checkpointing)
source ${DC2_CONFIGDIR}/phosimSetup.sh

## Special step-specific configs
#export DMTCP_CHECKPOINT_DIR=$SCRATCH/dmtcp/checkpointDir
#export DMTCP_TMPDIR=$SCRATCH/dmtcp/tmp
#export DMTCP_CHECKPOINT_INTERVAL=300

## Dump environment variables for posterity
echo
echo "Most Environment Variables:"
printenv | grep -v ^PE_ | grep -v ^CRAY | sort
echo
echo
date
echo "--------------------------------------------------------------------"
echo

## Final step: run task code
${DC2_CONFIGDIR}/runE2ADC.py
exit $?
