'''
Created on Dec 8, 2013

@author: Julia
'''
###############################################################################
# Script 4_cl31_aggregateBS
# Author: Julia Wagemann
# Date: December 2013
#
# This script provides functions to aggregated smoothed cl31 backscatter data
###############################################################################
import numpy as np
from numpy import *
import os
from os.path import basename
import glob
import csv
from datetime import datetime, timedelta


# path to smoothed cl31 backscatter data
path = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/cl31/Backscatter/ma_TimeHeight_log"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function to write outputfile
def writeLineToOutputTime(outputfile,paras,date):
    colStr = ''
    for i in range(760):
        colStr = colStr + ',' + str(paras[i])
        
    outputfile.write(date + colStr +'\n')

# Fucntion averageTime to aggregated row values based on given timeSteps value
def averageTime(inputfile,timeSteps):
    arrayVals = np.loadtxt(open(inputfile,"rb"),delimiter =",",usecols=range(1,761))
    inputFile = open(inputfile,'r')
    ofile = open(inputFile.name[:-13]+'maTime_5min.csv','w')
    dateTime = []
    for line in inputFile:
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    print len(dateTime)
    j = 0
    for i in range(len(dateTime)/5):
        print j
        timeStepEnd = timeSteps +j
        subset = arrayVals[j:timeStepEnd]
        subsetSum = map(sum,zip(*subset))
        result = [x/timeSteps for x in subsetSum]
        print dateTime[j]
        print dateTime[i]
        writeLineToOutputTime(ofile,result,dateTime[j])
        j = timeStepEnd
    ofile.close()
    

###############################################################################
# Test environment
############################################################################### 
fileList = getFilesInList(path,"*__averaged.csv")
print fileList
for files in fileList:
    averageTime(files,5)

