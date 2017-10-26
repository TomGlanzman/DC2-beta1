## utils.py - utility functions for use in DC2 phoSim workflow scripts

import os,sys
import pickle


def dm2phosim(chipID):
    ## Convert dm to phosim style of LSST sensor ID
    ##
    ## dm format: R:n,m S:n,m (or S:n,m,A/B for corner rafts)
    ## phosim format: Rnm_Snm
    ## where n,m range from 0-4
    #print 'dm2phosim - chipID = ',chipID
    rRow = chipID.split()[0].split(':')[1].split(',')[0]
    rCol = chipID.split()[0].split(':')[1].split(',')[1]
    #print 'rRow = ',rRow,', rCol = ',rCol
    sRow = chipID.split()[1].split(':')[1].split(',')[0]
    sCol = chipID.split()[1].split(':')[1].split(',')[1]
    #print 'sRow = ',sRow,', sCol = ',sCol
    r = rRow+rCol
    s = sRow+sCol
    newID = 'R'+r+'_S'+s
    #print 'newID = ',newID
    ## Ignore corner rafts
    if r == '00' or r == '04' or r == '40' or r == '44':
        newID = None
        #print 'corner raft...ignore.'
        pass
    return newID


def getVisit(stream, visitFile):

    print 'Entering getVisit:\n   stream ',stream,'\n   visitFile ',visitFile

    data = pickle.load(open(visitFile,'rb'))
    obsHistIDs = data['obsHistID']
    chipNames = data['chipNames']


    numVisits = len(obsHistIDs)

    if len(obsHistIDs) != len(chipNames):
        print "%ERROR: #obsHistIDs =/= #chipNames"
        print 'len(obsHistIDs) = ',len(obsHistIDs)
        print 'len(chipNames) = ',len(chipNames)
        sys.exit(1)
        pass

    print 'Number of visits in visit file = ',numVisits
    if stream > numVisits-1:
        print "%ERROR: stream number too large"
        sys.exit(1)
        pass

    ## Select visit

    obsHistID = obsHistIDs[stream]
    chipList = chipNames[stream]

    print 'stream = ',stream
    print 'obsHistID = ',obsHistID
    #print 'chipList = ',chipList


    phoSimSensorList = []
    for chip in chipList:
        #print 'chip = ',chip
        numChips = len(chip)
        #print 'Number of chips to sim in this visit = ',numChips
        sensorID = dm2phosim(chip)
        #print 'sensorID = ',sensorID
        if sensorID != None: phoSimSensorList.append(sensorID)
        pass

    print 'Number of sensors to sim = ',len(phoSimSensorList)
    print 'List of sensors to simulate this visit:\n',phoSimSensorList
    return (obsHistID,phoSimSensorList)
