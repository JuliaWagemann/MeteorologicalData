'''
Created on Feb 18, 2014

@author: Julia
'''
###############################################################################
# Script 5_campbell_getTemporalSubset
# Author: Julia Wagemann
# Date: February 2014
#
# This script creates a temporal subset of temperature and relative humidity 
# based on start and end indices of cloudradar samples
###############################################################################

import glob
import csv
import os
import numpy as np
from datetime import datetime

# path to campbell data
path = "H:/Masterarbeit/2_Data/3_fog_time_series/campbell/campbell_5min/"
# path to start and end indices of cloudradar samples
path2 = "H:/Masterarbeit/2_Data/3_fog_time_series/cloudradar/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# function to write output
def writeLineToOutput(outputfile,paras,date):
    colStr = ''
    for i in range(4):
        colStr = colStr + ',' + str(paras[i])
  
    outputfile.write(date + colStr +'\n')

# function getZprofiles that creates a temporal subset based on ZSamples
def getZProfiles(inputfile1,ZSamples):
    arrayVals = np.loadtxt(open(inputfile1,"rb"),delimiter =",",usecols=range(1,5),skiprows=1)
    inputFile = open(inputfile1,'r')
    outputfile = open(inputfile1[:-9] + '_Samples2.csv', 'w')
    outputfile.write('dateTime,T1_2m_Avg,T2_10m_Avg,rH_2m,rH_10m\n')
    print ZSamples
    
    dateTime = []
    for line in inputFile:
        if line.startswith('dateTime'):
            continue
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    
    subset = arrayVals[int(ZSamples[0])-1:int(ZSamples[1])-1,:]
    j=0
    for i in subset:
        print dateTime[int(j)+int(ZSamples[0])-1]
        print i
        writeLineToOutput(outputfile,i,dateTime[int(j)+int(ZSamples[0])-1])
        j += 1
    outputfile.close()
    

################################################################################################
# Test environment
################################################################################################
fileList = getFilesInList(path,'*.csv')
print fileList

ZProfiles = open(path2+"cloudradar_start_end_samples.csv", 'r')
samples = []
for row in ZProfiles:
    columns = row.split(';')
    samples.append(columns)

for i,j in zip(fileList,samples):
    getZProfiles(i,j)
    