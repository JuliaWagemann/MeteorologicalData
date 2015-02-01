'''
Created on Jan 9, 2014

@author: Julia
'''
###############################################################################
# Script 1_campbell_preprocess
# Author: Julia Wagemann
# Date: August 2013
#
# This script aggregates Campbell data based on a given timeStep value
###############################################################################
import numpy as np
from numpy import *
import os
from os.path import basename
import glob
import csv
from datetime import datetime, timedelta
import math

# path of campbell data that shall be aggregated
path = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/campbell/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# function that writes the outputfile
def writeLineToOutputTime(outputfile,paras,date):
    colStr = ''
    for i in range(4):
        colStr = colStr + ',' + str(paras[i])
        
    outputfile.write(date + colStr +'\n')

# function that takes an inputfile and a given timeStep to aggregate
# the values of the inputfile
def averageTime(inputfile,timeSteps): 
    arrayVals = np.loadtxt(open(inputfile,"rb"),delimiter =",",usecols=range(18,22),skiprows=1)
    inputFile = open(inputfile,'r')
    ofile = open(inputFile.name[:-4]+'_5minMean.csv','w')
    dateTime = []
    for line in inputFile:
        if line.startswith('dateTime'):
            continue
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    print len(dateTime)
    j = 1
    for i in range(len(dateTime)/timeSteps):
        timeStepEnd = timeSteps+j
        subset = arrayVals[j:timeStepEnd]
        subsetSum = map(sum,zip(*subset))
        result = [x/timeSteps for x in subsetSum]          
        writeLineToOutputTime(ofile,result,dateTime[j-1])
        j = timeStepEnd
    ofile.close()


################################################################################################
# Test environment
################################################################################################
fileList = getFilesInList(path,"*.csv")
print fileList

for files in fileList:
    print files
    averageTime(files,5)