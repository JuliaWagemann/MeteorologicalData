'''
Created on Jan 10, 2014

@author: Julia
'''
###############################################################################
# Script 2_preparation_theo_profiles_samples
# Author: Julia Wagemann
# Date: January 2014
#
# This script retrieves all the necessary parameters in order to calculated
# theoretical Z profiles
###############################################################################
import numpy as np
import os
from os.path import basename
import glob
from datetime import datetime

# Path to height of cloud top data
pathCloudTop  = 'H:/Masterarbeit/2_Data/3_fog_time_series/dsd/cloudradar_cloudinfo/' 
# Path to temperature at cloud base height
pathCloudBaseTemp  = 'H:/Masterarbeit/2_Data/3_fog_time_series/dsd/campbell_Samples/' 
# Path to vertical z profiles
pathZVal  = 'H:/Masterarbeit/2_Data/3_fog_time_series/dsd/cloudradar_zSamples/'
# Path to calculated omega values
pathOmega = 'H:/Masterarbeit/2_Data/3_fog_time_series/dsd/'     


def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function that calculates the liquid water content with the aid of a given Omega
def calculateLWC(omega,Z):
    LWC = omega*Z
    return LWC

# Function getParamsInFile that puts all necessary parameters in an outputfile
def getParamsInFile(inputCloudTop,inputCloudBaseTemp,inputZ,inputOmega):
    arrayCloudTop = np.loadtxt(open(pathCloudTop+inputCloudTop,"rb"),delimiter =",",usecols=range(1,7),skiprows=1)
    arrayCloudBaseTemp = np.loadtxt(open(pathCloudBaseTemp+inputCloudBaseTemp,"rb"),delimiter =",",usecols=range(1,5),skiprows=1)
    arrayZVals = np.loadtxt(open(pathZVal+inputZ,"rb"),delimiter =",",usecols=range(1,512))
    arrayOmega = np.loadtxt(open(inputOmega,"rb"),delimiter =",",usecols=range(1,7),skiprows=1)
 
	inputFile = open(pathCloudTop+inputCloudTop,'r')
    outputfile1 = open(pathOmega+'params/'+inputZ[:-14]+'_paramsGround.csv','w')
    outputfile2 = open(pathOmega+'params/'+inputZ[:-14]+'_paramsProfile.csv','w')
    dateTimeList= []
    for line in inputFile:
        if line.startswith('dateTime'):
            continue
        columns = line.split(',')
        dateTime = datetime.strptime(columns[0],"%Y-%m-%d %H:%M")
        dateTimeFinal = dateTime.strftime("%Y-%m-%d %H:%M")
        dateTimeList.append(dateTimeFinal)
         
    omega1=arrayOmega[0,5].tolist()
    omega2=arrayOmega[1,5]
    cloudBase=0
    zInc = 1
    betaStatic = 0.3
    height = 2000.
    rangeGateHeight = height/512.
    
    outputfile1.write('dateTime, cloudTop, cloudBase, zInc, betaStatic, cloudBaseTemp, LWC, altitude, omega\n')
    outputfile2.write('dateTime, cloudTop, cloudBase, zInc, betaStatic, cloudBaseTemp, LWC, altitude, omega\n') 

    for j in range(len(arrayZVals)):
        cloudBaseTemp = arrayCloudBaseTemp[j,0].tolist()
        cloudTop = arrayCloudTop[j,1].tolist()
        dateTimeCur = dateTimeList[j]
        zVal = 0.
        for i in range(511):
            if zVal != 0.:
                break
            if arrayZVals[j,i]==-999.0:
                continue
            else:
                zVal = arrayZVals[j,i].tolist()              
                altitude = i*rangeGateHeight
                
        LWC1 = calculateLWC(omega1,zVal)
        LWC2 = calculateLWC(omega2,zVal)
       
        outputfile1.write(dateTimeCur+','+str(cloudTop)+','+str(cloudBase)+','+str(zInc)+','+str(betaStatic)+','+str(cloudBaseTemp)+','+str(LWC1)+','+str(altitude)+','+str(omega1)+'\n')
        outputfile2.write(dateTimeCur+','+str(cloudTop)+','+str(cloudBase)+','+str(zInc)+','+str(betaStatic)+','+str(cloudBaseTemp)+','+str(LWC2)+','+str(altitude)+','+str(omega2)+'\n')    
    outputfile1.close()
    outputfile2.close()       
    
###########################################################################
# Testing environment
###########################################################################
fileList1 = getFilesInList(pathCloudTop, '*_Samples.csv')    
fileList2 = getFilesInList(pathCloudBaseTemp, '*_Samples.csv')    
fileList3 = getFilesInList(pathZVal, '*_ZProfiles.csv')      
  
inputOmega =pathOmega+'dsd_mgvParam.csv'    

for i,j,k in zip(fileList1,fileList2,fileList3):
    print i,j,k
    getParamsInFile(i,j,k,inputOmega)


