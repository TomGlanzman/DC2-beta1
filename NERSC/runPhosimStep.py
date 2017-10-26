#!/usr/bin/env python
## runPhosimStep.py - Run a part of phoSim
##

import os,sys,shutil,gzip,subprocess,shlex
import logging as log

def runPhosimStep(step,snap=0):

    steps = ['trim','raytrace','e2adc']
    if step not in steps:
        log.error('Unrecognized phoSim step ',step)
        return 1

    log.info('Begin phoSim step '+step+', snap '+str(snap))

    ## Construct full .submit file name(s) for this job
    log.info('Construct submit filename')
    exposure = "%03d" % snap

    if step == 'trim':
        subFileName = step+'_'+os.getenv('DC2_OBSHISTID')+'_'+os.getenv('PIPELINE_STREAM')
    else:
        ckpt = '0'   ## internal phoSim checkpointing is NOT supported
        subFileName = step+'_'+os.getenv('DC2_OBSHISTID')+'_'+os.getenv('DC2_SENSORID')+'_'+'E'+exposure

        if step == 'raytrace': subFileName += '_'+ckpt
        pass
    
    parFileName = subFileName+'.pars'
    print 'parFileName = ',parFileName
        
    subFileName += '.submit'
    print 'subFileName = ', subFileName
    
    sixdigits = "%06d" % int(os.getenv('DC2_TOPLEVEL6'))
    workDir = os.path.join(os.getenv('PHOSIM_SCR_ROOT'),sixdigits,'work')
    print 'workDir = ',workDir

    sf = os.path.join(workDir,subFileName)
    print 'submitFile = ',sf

    if not os.access(sf,os.R_OK):
        log.error('Cannot access .submit file for this trim job: '+sf)
        return 1
        pass


   ## Extract data from .submit file
   ##                   NOTE: continuation lines are neither needed nor
   ##                   supported in the .submit file parsing
    log.info('Extract data from submit file')
    jobParms = {}
    nlines = 0
    with open(sf,'r') as sfp:
        for line in sfp:
            if line.find('=') != -1:
                nlines += 1
                print line.strip()
                foo = line.split('=')
                jobParms[foo[0].strip()] = foo[1].strip()
            pass
        pass
    print '----------------------------------------\n# useful lines in submit file = ',nlines
    print 'jobParms = ',jobParms

## Switch to phoSim work directory for remaining steps
    os.chdir(jobParms['initialdir'])

## append trimcatalog for this sensor to the end of the raytrace .pars file (but only once)
    if step=='raytrace':
        trimcatFileName = 'trimcatalog_'+os.getenv('DC2_OBSHISTID')+'_'+os.getenv('DC2_SENSORID')+'.pars'
        print 'trimcatFileName = ',trimcatFileName

        ## Check if trimmed catalog already appended to raytrace .pars file
        trimmed = False
        with open(parFileName,'r') as sfp:
            for line in sfp:
                if line.startswith('object'):
                    trimmed = True
                    break
                pass
            pass
        log.info('raytrace.pars file trimmed: '+str(trimmed))
        if not trimmed:
            log.info('Append trimcatalog to end of raytrace .pars file')
            cmd = 'cat '+trimcatFileName+' >> '+parFileName
            print cmd
            rc = os.system(cmd)
            if rc <> 0:
                log.error('Failure to concatenate trimcat to raytrace .pars file')
                sys.exit(1)
                pass
            pass
        pass

   ## Construct phoSim command and execute
    log.info('Construct command and execute')
    #cmd = 'cat '+jobParms['Input']+' | '+jobParms['executable']
    cmd = jobParms['executable']+' < '+jobParms['Input']
    print 'cmd = ',cmd

    sys.stdout.flush()
    rc = os.system(cmd)
    sys.stdout.flush()
    log.info('Return from '+step+', rc = '+str(rc))
    return rc
