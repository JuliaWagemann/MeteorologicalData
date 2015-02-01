# -*- coding: utf-8 -*-
'''
Created on Jan 7, 2014

@author: Julia
'''
###############################################################################
# Script 4_cloudradar_getZSamples
# Author: Julia Wagemann
# Date: September 2013
#
# This script lists selected vertical ZProfiles based on a list of index numbers
# (index number means the selected time point of the fog event)
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

# Function getZProfiles, that chooses selected vertical ZProfiles based on given ZSample numbers
def getZProfiles(inputfile1,ZSamples):
    arrayVals = np.loadtxt(open(inputfile1,"rb"),delimiter =",",usecols=range(1,512))
    inputFile = open(inputfile1,'r')
    outputfile = open(inputfile1[:-14] + '_ZProfiles.csv', 'w')
    zVals=0.
    
    dateTime = []
    for line in inputFile:
        if line.startswith('TIME'):
            continue
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    
    for i in ZSamples:
        zVals = arrayVals[int(i)-1,:]
        writeLineToOutput(outputfile,zVals,dateTime[int(i)-2])
    outputfile.close()
    
###########################################################################
# Testing environment
###########################################################################
fileList = getFilesInList(path,'*.csv')
ZProfiles = open(path2+"zProfilesSample.csv", 'r')
samples = []
for row in ZProfiles:
    columns = row.split(';')
    samples.append(columns)

for i,j in zip(fileList,samples):
    getZProfiles(i,j)