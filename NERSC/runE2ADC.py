#!/usr/bin/env python
## runE2ADC.py - phoSim catalog step to create electronics readout files (one per amplifier)
##                         NOTE: this step is optional depending on command line options

import os,sys,shutil,gzip

print '\n\nWelcome to runE2ADC.py\n========================\n'
rc = 0

## Setup logging, python style
import logging as log
log.basicConfig(stream=sys.stdout, format='%(asctime)s %(levelname)s in %(filename)s line %(lineno)s: %(message)s', level=log.INFO)
log.info("Start")


## Insert task config area for python modules (as 2nd element) in sys.path
sys.path.insert(1,os.getenv('DC2_CONFIGDIR'))
#from config import *


## Step 1: Loop over exposures (snaps) for this visit
log.info('Step 1')
nsnaps = os.getenv('DC2_NSNAP')
log.info('There are '+nsnaps+' exposures for this visit')
for snap in range(0,int(nsnaps)):
    log.info('Start exposure '+str(snap))

    
## Step 2: Construct full .submit file name(s) for this job
    log.info('Step 2')
    exposure = "%03d" % snap
    print 'exposure = ',exposure,', type = ',type(exposure)
    subFileName = 'e2adc_'+os.getenv('DC2_OBSHISTID')+'_'+os.getenv('DC2_SENSORID')+'_'+'E'+exposure+'.submit'
    print 'subFileName = ', subFileName
    
    sixdigits = "%06d" % int(os.getenv('DC2_TOPLEVEL6'))
    workDir = os.path.join(os.getenv('PHOSIM_SCR_ROOT'),sixdigits,'work')
    print 'workDir = ',workDir

    sf = os.path.join(workDir,subFileName)
    print 'submitFile = ',sf

    if not os.access(sf,os.R_OK):
        log.error('Cannot access .submit file for this trim job: '+sf)
        sys.exit(1)
        pass


## Step 3: Extract data from .submit file
##                   NOTE: continuation lines are neither needed nor
##                   supported in the .submit file parsing
    log.info('Step 3')
    jobParms = {}
    nlines = 0
    with open(sf,'r') as sfp:
        for line in sfp:
            nlines += 1
            if line.find('=') != -1:
                print line.strip()
                foo = line.split('=')
                jobParms[foo[0].strip()] = foo[1].strip()
            pass
        pass
    print '----------------------------------------\n# useful lines in submit file = ',nlines
    print 'jobParms = ',jobParms

## Step 4: construct command to run e2adc and execute
    log.info('Step 4')
    cmd = 'cat '+jobParms['Input']+' | '+jobParms['executable']
    cmd = jobParms['executable']+' < '+jobParms['Input']
    print 'cmd = ',cmd
    os.chdir(jobParms['initialdir'])

    sys.stdout.flush()
    rc = os.system(cmd)
    sys.stdout.flush()
    log.info('Return from e2adc, rc = '+str(rc))
    if rc != 0:
        log.error('Abort')
        sys.exit(rc)
        pass

    pass ## end of loop over exposures

log.info("All done")
sys.exit(rc)
