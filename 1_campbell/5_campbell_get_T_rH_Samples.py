'''
Created on Jan 9, 2014

@author: Julia
'''
###############################################################################
# Script 5_campbell_getSamples
# Author: Julia Wagemann
# Date: January 2014
#
# This script writes Temperature and relative humidity based on individual samples
# to a .csv file
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# path to campbell data
path = "H:/Masterarbeit/2_Data/3_fog_time_series/campbell/campbell_5min/"
# path to file with samples of z profiles
path2 = "H:/Masterarbeit/2_Data/3_fog_time_series/cloudradar/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# function to write to output file
def writeLineToOutput(outputfile,paras,date):
    colStr = ''
    for i in range(4):
        colStr = colStr + ',' + str(paras[i])
  
    outputfile.write(date + colStr +'\n')


# function that extracts temperature and rH for each Sample
def getZProfiles(inputfile1,ZSamples):
    arrayVals = np.loadtxt(open(inputfile1,"rb"),delimiter =",",usecols=range(1,5),skiprows=1)
    inputFile = open(inputfile1,'r')
    outputfile = open(inputfile1[:-9] + '_Samples.csv', 'w')
    outputfile.write('dateTime,T1_2m_Avg,T2_10m_Avg,rH_2m,rH_10m\n')
    zVals=[]
    print ZSamples
    
    dateTime = []
    for line in inputFile:
        if line.startswith('dateTime'):
            continue
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    
    for i in ZSamples:
        print int(i)-1
        zVals = arrayVals[int(i)-2]
        writeLineToOutput(outputfile,zVals,dateTime[int(i)-2])
    outputfile.close()

    

################################################################################################
# Test environment
################################################################################################
fileList = getFilesInList(path,'*.csv')
print fileList

ZProfiles = open(path2+"zProfilesSample.csv", 'r')
samples = []
for row in ZProfiles:
    columns = row.split(';')
    samples.append(columns)

for i,j in zip(fileList,samples):
    getZProfiles(i,j)