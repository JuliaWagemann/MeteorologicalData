'''
Created on Jan 9, 2014

@author: Julia
'''
###############################################################################
# Script 6_cloudradar_cloudinfo_getZSamples
# Author: Julia Wagemann
# Date: January 2014
#
# This script lists cloudinfo information of selected vertical ZProfiles 
# based on a list of index numbers
# (index number means the selected time point of the fog event)
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# Path to cloudradar cloudinfo data
path = "H:/Masterarbeit/2_Data/3_fog_time_series/cloudradar/cloudinfo_5min/"
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
    for i in range(7):
        colStr = colStr + ',' + str(paras[i])
  
    outputfile.write(date + colStr +'\n')

# Function getZProfiles, that get cloudinfo information of selected vertical ZProfiles
def getZProfiles(inputfile1,ZSamples):
    arrayVals = np.loadtxt(open(inputfile1,"rb"),delimiter =",",usecols=range(1,8),skiprows=1)
    inputFile = open(inputfile1,'r')
    outputfile = open(inputfile1[:-30] + '_cloudinfo5min_Samples.csv', 'w')
    outputfile.write('dateTime, CloudbaseHeight_1, CloudtopHeight_1, Cloudthickness_1'+'\n') 
    zVals=[]
    
    dateTime = []
    for line in inputFile:
        if line.startswith('dateTime'):
            continue
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    
    for i in ZSamples:
        print int(i)-2
        zVals = arrayVals[int(i)-2]
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