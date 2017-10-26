#!/usr/bin/env python
## finishVisit.py - final bookkeeping and cleanup for a single visit
##

import os,sys,shutil

print '\n\nWelcome to finishVisit.py\n========================\n'
rc = 0

## Setup logging, python style
import logging as log
log.basicConfig(stream=sys.stdout, format='%(asctime)s %(levelname)s in %(filename)s line %(lineno)s: %(message)s', level=log.INFO)

## Insert task config area for python modules (insert as 2nd element in sys.path)
sys.path.insert(1,os.getenv('DC2_CONFIGDIR'))


## The primary task of this jobstep is to clean up the $SCRATCH area
## for user 'desc' for this particular visit.  $SCRATCH accumulates
## instance catalogs and bits of same, job submission files, parameter
## files, etc.  It all adds up to several GB

if os.getenv('PHOSIM_SCR_CLEANUP') == '1':
    scrDir = os.path.join(os.getenv('PHOSIM_SCR_ROOT'),os.getenv('DC2_SIXDIGSTREAM'))
    log.info('Cleaning up $SCRATCH: '+scrDir)
    shutil.rmtree(scrDir)
    pass

## Done.
log.info('All done.')
sys.exit(rc)
