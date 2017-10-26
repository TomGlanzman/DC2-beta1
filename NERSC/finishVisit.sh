#!/bin/bash
# setupVisit.sh - set up environment

## General task configuration (for all steps)
source ${DC2_CONFIGDIR}/config.sh


## Dump environment variables for posterity
echo "********************************************************************************"
echo
echo "Most Environment Variables:"
echo "-------------------------------------"
printenv | grep -v ^PE_ | grep -v ^CRAY | sort
echo
echo
date
echo "--------------------------------------------------------------------"
echo

## Final step: run task code
${DC2_CONFIGDIR}/finishVisit.py
exit $?
