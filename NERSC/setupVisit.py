#!/usr/bin/env python
## setupVisit.py - bookkeeping for initiating a phoSim run in DC2-phoSim task
##

import os,sys,shutil,gzip

print '\n\nWelcome to setupVisit.py\n========================\n'
rc = 0

## Setup logging, python style
import logging as log
log.basicConfig(stream=sys.stdout, format='%(asctime)s %(levelname)s in %(filename)s line %(lineno)s: %(message)s', level=log.INFO)

## Insert task config area for python modules (insert as 2nd element in sys.path)
sys.path.insert(1,os.getenv('DC2_CONFIGDIR'))
#from config import *
from utils import *

## Say hello
sstream = os.getenv('DC2_SIXDIGSTREAM')
log.info("Starting stream %s",sstream)
## Preserve 6-digit top-level stream number
cmd = 'pipelineSet DC2_TOPLEVEL6 '+sstream
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable")
    sys.exit(99)
    pass



## Create Persistent data store directory structure for this invocation of phoSim
##   This area is in the LSST "project" storage space

### Check if project directory already exists from previous execution and, if not, create it.
## Directory structure: $DC2_ROOT/<output>/<stream>/{work,output}
filePermissions = int(os.getenv("filePermissions"),8) ## Octal file permissions
archivesDirName = 'archives'
outDir = os.path.join(os.environ['DC2_OUTPUT'],os.environ['DC2_SIXDIGSTREAM'])

print 'filePermissions = ',filePermissions,' (or ',oct(filePermissions), ' octal)'

log.info('PhoSim output directory = \n\t%s',outDir)

### Is there a previous instance of this job step that requires archiving?

if not os.access(outDir,os.F_OK):                          ## NO
    log.info('Creating output directory: \n\t%s',outDir)
    os.makedirs(outDir,filePermissions)  ## Note that filePermissions is ignored on cori
#    os.chmod(outDir,filePermissions)
    os.system('chmod -R 0755 '+outDir)  ## may be obsolete now we are using ACLs
    pass
else:                                                      ## YES
    ## Create appropriate archive directory, 'archive-N'
    archiveRoot = os.path.join(outDir,archivesDirName)
    if not os.access(archiveRoot,os.F_OK):
        log.info('Creating archives directory: \n\t%s',archiveRoot)
        os.makedirs(archiveRoot,filePermissions)
#        os.chmod(archiveRoot,filePermissions)
        os.system('chmod -R 0755 '+archiveRoot)
        pass
    archiveDirList = os.listdir(archiveRoot)
    if len(archiveDirList) == 0:
        newArchiveName = 'archive-1'
    else:
        oldNumList = []
        for oldArc in archiveDirList:
            if oldArc.startswith('archive'):oldNumList.append(int(oldArc.split('-')[-1]))
            pass
        if len(oldNumList) > 0:
            oldNumList.sort()
            #print 'oldNumList = ',oldNumList
            newArchiveName = 'archive-'+str(oldNumList[-1]+1)
        else:
            log.error('Unexpected content in archives directory: \n\t%s\n\t %s',archiveRoot,archiveDirList)
            sys.exit(99)
            pass
        pass
    archiveDir = os.path.join(archiveRoot,newArchiveName)
    log.info("Creating new archive directory: \n\t%s",archiveDir)
    os.makedirs(archiveDir,filePermissions)
#    os.chmod(archiveDir,filePermissions)
    os.system('chmod -R 0755 '+archiveDir)
    
### And then squirrel away the old output in the new archive directory
    outDirList = os.listdir(outDir)
    log.info("Moving old files to archive")
    for item in outDirList:
        if not item == archivesDirName:
            sitem = os.path.join(outDir,item)
            ditem = os.path.join(archiveDir,item)
            #print 'shutil.move(',sitem,',',ditem,')'
            shutil.move(sitem,ditem)
            pass
        pass
    

## Pass along the path to the output directory
cmd = 'pipelineSet DC2_PHOSIMOUT '+outDir
print cmd
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable \n $%s",cmd)
    sys.exit(99)
    pass


## Check that SCRATCH (staging) area is clean
scrDir = os.path.join(os.getenv('PHOSIM_SCR_ROOT'),os.getenv('DC2_SIXDIGSTREAM'))
log.info('Checking phoSim scratch/staging space: '+scrDir)
if os.access(scrDir,os.F_OK):
    log.info('phoSim scratch/staging directory already exists.  Cleaning up...')
    shutil.rmtree(scrDir)
    pass


## Create staging area (work and output directories) in SCRATCH
log.info('Creating phoSim work and output directories in $SCRATCH')
scr_work=os.path.join(scrDir,'work')
scr_output=os.path.join(scrDir,'output')
os.makedirs(scr_work,filePermissions)
os.makedirs(scr_output,filePermissions)

cmd = 'pipelineSet DC2_SCR_PHOSIMOUT '+scrDir
print cmd
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable \n $%s",cmd)
    sys.exit(99)
    pass


##
## Determine visit number (obsHistID) and list of sensors to simulate
##
stream = int(os.getenv('PIPELINE_STREAM'))
log.info('Extract visit data.')

################################################################################
########## <DEVELOPMENT ONLY> ##################################################
################################################################################

#visitFile = os.getenv('DC2_VISIT_DB')
#(visitID,sensorList) = getVisit(stream,visitFile)

################################################################################
############  R E M O V E   P R I O R   T O   P R O D U C T I O N  #############
################################################################################

## We do not yet know how the list of visitIDs will be presented for DC2
## Also, will only the dithered subset of the focal plane be simulated?

## For now, allow only *four* pre-packaged visits to be used
print "\n\n\n\n\n   ********* DEVELOPMENT TEST **************\n"

if stream == 0:
    visitID=40336
    sensorList=['R01_S02']   # <--- initial single-sensor test

#    sensorList=['R01_S02', 'R02_S00', 'R02_S01', 'R02_S02', 'R03_S01', 'R03_S11', 'R03_S12', 'R03_S21', 'R03_S22', 'R13_S02', 'R13_S12', 'R14_S00', 'R14_S01', 'R14_S10', 'R14_S11', 'R14_S12', 'R14_S21', 'R14_S22', 'R24_S02']

elif stream == 1:
    visitID=40337
    sensorList=['R01_S00', 'R01_S01', 'R01_S02', 'R01_S10', 'R01_S11', 'R01_S12', 'R01_S20', 'R01_S21', 'R01_S22', 'R02_S00', 'R02_S01', 'R02_S02', 'R02_S10', 'R02_S11', 'R02_S12', 'R02_S20', 'R02_S21', 'R02_S22', 'R03_S00', 'R03_S01', 'R03_S10', 'R03_S11', 'R03_S12', 'R03_S20', 'R03_S21', 'R03_S22', 'R10_S01', 'R10_S02', 'R10_S10', 'R10_S11', 'R10_S12', 'R10_S20', 'R10_S21', 'R10_S22', 'R11_S00', 'R11_S01', 'R11_S02', 'R11_S10', 'R11_S11', 'R11_S12', 'R11_S20', 'R11_S21', 'R11_S22', 'R12_S00', 'R12_S01', 'R12_S02', 'R12_S10', 'R12_S11', 'R12_S12', 'R12_S20', 'R12_S21', 'R12_S22', 'R13_S00', 'R13_S01', 'R13_S02', 'R13_S10', 'R13_S11', 'R13_S12', 'R13_S20', 'R13_S21', 'R13_S22', 'R14_S00', 'R14_S01', 'R14_S10', 'R14_S11', 'R14_S12', 'R14_S20', 'R14_S21', 'R14_S22', 'R20_S00', 'R20_S01', 'R20_S02', 'R20_S10', 'R20_S11', 'R20_S12', 'R20_S20', 'R20_S21', 'R20_S22', 'R21_S00', 'R21_S01', 'R21_S02', 'R21_S10', 'R21_S11', 'R21_S12', 'R21_S20', 'R21_S21', 'R21_S22', 'R22_S00', 'R22_S01', 'R22_S02', 'R22_S10', 'R22_S11', 'R22_S12', 'R22_S20', 'R22_S21', 'R22_S22', 'R23_S00', 'R23_S01', 'R23_S02', 'R23_S10', 'R23_S11', 'R23_S12', 'R23_S20', 'R23_S21', 'R23_S22', 'R24_S00', 'R24_S01', 'R24_S02', 'R24_S10', 'R24_S11', 'R24_S12', 'R24_S20', 'R24_S21', 'R24_S22', 'R30_S00', 'R30_S01', 'R30_S02', 'R30_S10', 'R30_S11', 'R30_S12', 'R30_S21', 'R30_S22', 'R31_S00', 'R31_S01', 'R31_S02', 'R31_S10', 'R31_S11', 'R31_S12', 'R31_S20', 'R31_S21', 'R31_S22', 'R32_S00', 'R32_S01', 'R32_S02', 'R32_S10', 'R32_S11', 'R32_S12', 'R32_S20', 'R32_S21', 'R32_S22', 'R33_S00', 'R33_S01', 'R33_S02', 'R33_S10', 'R33_S11', 'R33_S12', 'R33_S20', 'R33_S21', 'R33_S22', 'R34_S00', 'R34_S01', 'R34_S02', 'R34_S10', 'R34_S11', 'R34_S12', 'R34_S20', 'R34_S21', 'R41_S00', 'R41_S01', 'R41_S02', 'R41_S10', 'R41_S11', 'R41_S12', 'R41_S21', 'R41_S22', 'R42_S00', 'R42_S01', 'R42_S02', 'R42_S10', 'R42_S11', 'R42_S12', 'R42_S20', 'R42_S21', 'R42_S22', 'R43_S00', 'R43_S01', 'R43_S02', 'R43_S10', 'R43_S11', 'R43_S12', 'R43_S20', 'R43_S21']

elif stream == 2:
    visitID=40338
    sensorList=['R12_S21', 'R12_S22', 'R13_S20', 'R20_S22', 'R21_S01', 'R21_S02', 'R21_S10', 'R21_S11', 'R21_S12', 'R21_S20', 'R21_S21', 'R21_S22', 'R22_S00', 'R22_S01', 'R22_S02', 'R22_S10', 'R22_S11', 'R22_S12', 'R22_S20', 'R22_S21', 'R22_S22', 'R23_S00', 'R23_S01', 'R23_S02', 'R23_S10', 'R23_S11', 'R23_S12', 'R23_S20', 'R23_S21', 'R23_S22', 'R24_S00', 'R24_S10', 'R24_S11', 'R24_S20', 'R24_S21', 'R24_S22', 'R30_S01', 'R30_S02', 'R30_S11', 'R30_S12', 'R30_S21', 'R30_S22', 'R31_S00', 'R31_S01', 'R31_S02', 'R31_S10', 'R31_S11', 'R31_S12', 'R31_S20', 'R31_S21', 'R31_S22', 'R32_S00', 'R32_S01', 'R32_S02', 'R32_S10', 'R32_S11', 'R32_S12', 'R32_S20', 'R32_S21', 'R32_S22', 'R33_S00', 'R33_S01', 'R33_S02', 'R33_S10', 'R33_S11', 'R33_S12', 'R33_S20', 'R33_S21', 'R33_S22', 'R34_S00', 'R34_S01', 'R34_S02', 'R34_S10', 'R34_S11', 'R34_S12', 'R34_S20', 'R34_S21', 'R41_S00', 'R41_S01', 'R41_S02', 'R41_S10', 'R41_S11', 'R41_S12', 'R41_S21', 'R41_S22', 'R42_S00', 'R42_S01', 'R42_S02', 'R42_S10', 'R42_S11', 'R42_S12', 'R42_S20', 'R42_S21', 'R42_S22', 'R43_S00', 'R43_S01', 'R43_S02', 'R43_S10', 'R43_S11', 'R43_S12', 'R43_S20', 'R43_S21']

elif stream == 3:
    visitID=1668469
    sensorList=["R01_S00","R01_S10","R10_S00"]   # <-- known to require a long execution time (>5d @SLAC)

else:
    print "Stream ",stream," has no catalog!  Exiting..."
    sys.exit(1)

################################################################################
########## </DEVELOPMENT ONLY> #################################################
################################################################################

visitID = str(visitID)
print 'visitID = ',visitID,', type(visitID) = ',type(visitID)
print 'sensorList = ',sensorList

## Package up the sensorList into variables of <990 characters each (email limitation)
### Figure 8 characters/sensor, e.g. R01_S12 plus a comma
### 189 sensors would then be 1511 characters long
if len(sensorList) <= 100:
    foo = ','.join(sensorList)
    bar = ''
else:
    foo = ','.join(sensorList[:100])
    bar = ','.join(sensorList[100:])
    pass
print 'foo = ',foo
print 'bar = ',bar
cmd = 'pipelineSet DC2_SENSORLIST_1 '+foo
rc1 = os.system(cmd)
cmd = 'pipelineSet DC2_SENSORLIST_2 '+bar
rc2 = os.system(cmd)
cmd = 'pipelineSet DC2_NUM_SENSORS '+str(len(sensorList))
rc3 = os.system(cmd)
if rc1 <> 0 or rc2 <> 0 or rc3 <> 0:
    log.error("Unable to set pipeline variable")
    sys.exit(99)
    pass


##  Set up phoSim instanceCatalog

if os.getenv('PHOSIM_IC_GEN') == 'STATIC':
    print 'Using statically generated instance catalog'
    icDir = os.getenv('PHOSIM_CATALOGS')+'/'+visitID
    print 'icDir = ',icDir
    icName = 'phosim_cat_'+visitID+'.txt'
    print 'icName = ',icName
    icSelect = os.path.join(icDir,icName)
    print 'icSelect = ',icSelect
    
elif os.getenv('PHOSIM_IC_GEN') == 'DYNAMIC':
    print 'Using dymanically generated instance catalog'

    cmd = os.path.join(os.getenv('DC2_CONFIGDIR'),'generateDc1InstCat.sh')
    print 'cmd = ',cmd
    icDir = os.path.join(scrDir,'instCat')
    print 'icDir = ',icDir
    icName = 'phosim_cat_'+visitID+'.txt'
    print 'icName = ',icName
    icSelect = os.path.join(icDir,icName)
    print 'icSelect = ',icSelect
    minMag = os.getenv('DC2_MINMAG')
    print 'minMag = ',minMag
    opts = ' --db '+os.getenv('DC2_OPSIM_DB')+' --out '+icDir+' --id '+visitID+' --min_mag '+minMag
    cmd += opts
    log.info('Generate instanceCatalog.')
    print cmd

    sys.stdout.flush()
    rc = os.system(cmd)
    sys.stdout.flush()
    log.info('Return from generateDc1InstCat, rc= '+str(rc))
    if rc <> 0:
        log.error('Failed to generate instance catalog.')
        sys.exit(1)
        pass
    pass



## Preserve the instance catalog info for subsequent processing steps
cmd = 'pipelineSet DC2_INSTANCE_CATALOG '+icSelect
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable")
    sys.exit(99)
    pass




## Copy instanceCatalog to scratch and uncompress
###  Assume if ic compressed, then filename.txt.gz

# old way: pre-made instanceCatalog copied from repository to $SCRATCH
#log.info('Copy/create uncompressed instanceCatalog in $SCRATCH')
#icScratch = os.path.join(scrDir,os.path.basename(icSelect))
#shutil.copyfile(icSelect,icScratch)

# new way: instanceCatalog is generated in place on $SCRATCH
icScratch = icSelect


if icScratch.endswith('.gz'):
    icNew = os.path.splitext(icScratch)[0]
    print 'icNew = ',icNew
    print 'icScratch = ',icScratch
    inF = gzip.open(icScratch,'rb')
    outF = open(icNew,'wb')
    outF.write(inF.read())
    inF.close()
    outF.close()
    os.remove(icScratch)
    icScratch = icNew
    pass


## Parse the first part of the instanceCatalog and extract a few items
ic = {}
nic = 0
visit = None
nsnap = None
cfilter = None
log.info('Configuration part of instanceCatalog:')
with open(icScratch,'r') as fp:
    for line in fp:
        if line.startswith('object'): break
        if len(line) == 0 or line.startswith('#'):continue
        entry=line.strip().split()
        ic[entry[0]] = entry[1]
        if entry[0] == 'obshistid':visit = entry[1]
        if entry[0] == 'nsnap':nsnap = entry[1]
        if entry[0] == 'filter':cfilter = entry[1]
        print entry[0],' ',entry[1]
        nic =+ 1
        pass
    pass

print '\n============================='
print 'visit (obshistid) = ',visit
print 'nsnap = ',nsnap
print 'filter = ',cfilter
print '=============================\n'

## Pass filter, nsnap and obshistid to workflow engine for subsequent steps
cmd = 'pipelineSet DC2_NSNAP '+nsnap
print cmd
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable \n $%s",cmd)
    sys.exit(99)
    pass
cmd = 'pipelineSet DC2_OBSHISTID '+visit
print cmd
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable \n $%s",cmd)
    sys.exit(99)
    pass
cmd = 'pipelineSet DC2_FILTER '+cfilter
print cmd
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable \n $%s",cmd)
    sys.exit(99)
    pass




## Copy command file to scratch
log.info('Copy command file to $SCRATCH')
cfScratch = os.path.join(scrDir,os.path.basename(os.getenv('PHOSIM_COMMANDS')))
shutil.copyfile(os.getenv('PHOSIM_COMMANDS'),cfScratch)
log.info('Contents of phoSim command file:')
sys.stdout.flush()

## Parse command/override file
cf = {}
with open(cfScratch,'r') as fp:
    for line in fp:
        print line
        if len(line.strip()) == 0 or line.startswith('#'):continue
        entry=line.strip().split()
        cf[entry[0]] = None
        if len(entry) > 1: cf[entry[0]] = ' '.join(entry[1:])
        pass
    pass
print '==========================================\n\n\n'

## Check if a centroid file is requested
centroidfile = '0'
if 'centroidfile' in cf:
    if cf['centroidfile'] == '1':
        centroidfile = '1'
        pass
    pass

cmd = 'pipelineSet DC2_CENTROIDFILE '+centroidfile
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable \n $%s",cmd)
    sys.exit(99)
    pass


## (First) Change file permissions in phoSim /work tree from default (0750) to
## something reasonable (0755)
os.system('chmod -R 0755 '+scrDir)


## Run first part of phoSim, preparation for downstream trim/raytrace/e2adc
log.info('Run phoSim (part I)')
cmd = os.path.join(os.getenv('PHOSIM_ROOT'),'phosim.py')

## Global phoSim options
##   -g condor causes batch files to be created for trim/raytrace/e2adc steps
opts = ' -g condor -o '+scr_output+' -w '+scr_work+' -c '+cfScratch+' --checkpoint=0 '
#opts += ' --sed='+os.getenv('PHOSIM_SEDS')+' '

if os.getenv('PHOSIM_E2ADC') == 0:
    opts += ' -e 0 '
if 'NTHREADS' in os.environ:
    opts += ' -t '+os.getenv('NTHREADS')
    pass
cmd += ' '+icScratch+opts
print 'phoSim command:\n',cmd
print
sys.stdout.flush()

rc = os.system(cmd)

sys.stdout.flush()
log.info('Return from phoSim, rc = '+str(rc))


## (Second) Change file permissions in phoSim /work tree from default (0750) to
## something reasonable (0755)
os.system('chmod -R 0755 '+scrDir)


## Determine the number of catalog trim jobs to perform
dirList = os.listdir(scr_work)
ntrim = 0
for filex in dirList:
    if filex.startswith('trim') and filex.endswith('.pars'):ntrim+=1
    pass
log.info('There are '+str(ntrim)+ ' trim jobs to perform.')


## Pass ntrim to workflow engine for subsequent step
cmd = 'pipelineSet DC2_NTRIMS '+str(ntrim)
rc = os.system(cmd)
if rc <> 0 :
    log.error("Unable to set pipeline variable \n $%s",cmd)
    sys.exit(99)
    pass


## All done.
if rc >= 255:rc=17
log.info ('BYE!  rc='+str(rc)+'\n\n\n*****\n')
log.shutdown()

sys.exit(rc)
