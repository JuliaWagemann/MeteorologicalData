'''
Created on Feb 18, 2014

@author: Julia
'''
###############################################################################
# Script 5_cloudradar_getZSamples2
# Author: Julia Wagemann
# Date: September 2013
#
# This script creates a subset of selected vertical ZProfiles based on the first
# and last index of a given list
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# Path to cloudradar Z Profiles
path = "H:/Masterarbeit/2_Data/3_fog_time_series/cloudradar/Z_5min/"
# Path to list of index number for each fog event
path2 = "H:/Masterarbeit/2_Data/3_fog_time_series/cloudradar/"
path = "H:/Masterarbeit/2_Data/3_fog_time_series/cloudradar/Z_5min/"
path2 = "H:/Masterarbeit/2_Data/3_fog_time_series/cloudradar/"

# Function getFilesInList to list all files in a folder
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList
# Function that writes the outputfile
def writeLineToOutput(outputfile,paras,date):
    colStr = ''
    for i in range(511):
        colStr = colStr + ',' + str(paras[i])
        
    outputfile.write(date + colStr +'\n')

# Function getZProfiles, that chooses a subset of selected vertical ZProfiles based on given ZSample numbers
def getZProfiles(inputfile1,ZSamples):
    arrayVals = np.loadtxt(open(inputfile1,"rb"),delimiter =",",usecols=range(1,512))
    inputFile = open(inputfile1,'r')
    outputfile = open(inputfile1[:-14] + '_ZProfiles2.csv', 'w')
    print ZSamples
    
    dateTime = []
    for line in inputFile:
        if line.startswith('TIME'):
            continue
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    # create subset of Z profiles
    subset = arrayVals[int(ZSamples[0]):int(ZSamples[1]),:]
    j=0
    for i in subset:
        writeLineToOutput(outputfile,i,dateTime[int(j)+int(ZSamples[0])-1])
        j += 1
    outputfile.close()
  
###########################################################################
# Testing environment
###########################################################################
fileList = getFilesInList(path,'*.csv')
ZProfiles = open(path2+"cloudradar_start_end_samples.csv", 'r')
samples = []
for row in ZProfiles:
    columns = row.split(';')
    samples.append(columns)

for i,j in zip(fileList,samples):
    getZProfiles(i,j)