#!/usr/bin/env python
## runTrim.py - phoSim catalog trim step
##

import os,sys,shutil,gzip

print '\n\nWelcome to runTrim.py\n========================\n'
rc = 0

## Setup logging, python style
import logging as log
log.basicConfig(stream=sys.stdout, format='%(asctime)s %(levelname)s in %(filename)s line %(lineno)s: %(message)s', level=log.INFO)

## Insert task config area for python modules (insert as 2nd element in sys.path)
sys.path.insert(1,os.getenv('DC2_CONFIGDIR'))
#from config import *
import runPhosimStep


## Run Trim
log.info('Run Trim')
rc = runPhosimStep.runPhosimStep('trim',0)
if rc != 0:
    log.error('Failure in trim step, aborting...')
    sys.exit(1)


## Extract Sensor coordinates and pass back to workflow engine
log.info('Extract sensorIDs from .par file')
parFileName = 'trim_'+os.getenv('DC2_OBSHISTID')+'_'+os.getenv('PIPELINE_STREAM')+'.pars'
print 'parFileName = ',parFileName

sixdigits = "%06d" % int(os.getenv('DC2_TOPLEVEL6'))
workDir = os.path.join(os.getenv('PHOSIM_SCR_ROOT'),sixdigits,'work')
print 'workDir = ',workDir

pf = os.path.join(workDir,parFileName)
print 'parFile = ',pf
sensors = []
with open(pf,'r') as pfp:
    for line in pfp:
        if line.startswith('chipid'):sensors.append(line.split()[2].strip())
        pass
    pass
print 'sensors = ',sensors
sList = ','.join(sensors)
print 'sList = ',sList

cmd = 'pipelineSet DC2_SENSORLIST '+sList
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable")
    sys.exit(1)
    pass



log.info("All done")
sys.exit(0)
