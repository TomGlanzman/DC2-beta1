#!/bin/bash
## generateDc1InstCat.sh - setup and generate DC2 phoSim instance catalog

opts=$@
shift $#
# (one must empty the $@ var or it is sent to the setup script...)

echo 'sourcing instanceCatalog generation setup'
source /global/common/cori/contrib/lsst/lsstDM/setupStack-dc1.sh

echo 'generate ic'
echo python ${DC2_CONFIGDIR}/generateDc1InstCat.py ${opts}
python ${DC2_CONFIGDIR}/generateDc1InstCat.py ${opts}

rc=$?
echo 'Return from generateDc1InstCat.py, rc ='$rc

exit $rc
