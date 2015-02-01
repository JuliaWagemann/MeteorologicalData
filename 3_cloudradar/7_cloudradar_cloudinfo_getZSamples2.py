'''
Created on Feb 18, 2014

@author: Julia
'''
###############################################################################
# Script 7_cloudradar_cloudinfo_getZSamples2
# Author: Julia Wagemann
# Date: February 2014
#
# This script lists cloudinfo information of a subset of selected vertical ZProfiles 
# based on a list of index numbers
# (index number means the selected time point of the fog event)
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# Path to cloudinfo data
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
    for i in range(3):
        colStr = colStr + ',' + str(paras[i])
    outputfile.write(date + colStr +'\n')

# Function getZProfiles, that gets a subset of cloudinfo information of selected vertical ZProfiles	
def getZProfiles(inputfile1,ZSamples):
    arrayVals = np.loadtxt(open(inputfile1,"rb"),delimiter =",",usecols=range(1,8),skiprows=1)
    inputFile = open(inputfile1,'r')
    outputfile = open(inputfile1[:-30] + '_cloudinfo_5min_Samples2.csv', 'w')
    outputfile.write('dateTime, CloudbaseHeight_1, CloudtopHeight_1, Cloudthickness_1'+'\n') 
    zVals=[]
    
    dateTime = []
    zValues = []
    for line in inputFile:
        if line.startswith('dateTime'):
            continue
        columns = line.split(',')
        print len(columns)
        z = columns[1:len(columns)]
        a = columns[0]
        dateTime.append(a)
    subset = arrayVals[int(ZSamples[0])-1:int(ZSamples[1])-1,0:3]
    j=0
    for i in subset:
        print dateTime[int(j)+int(ZSamples[0])-1]
        print i
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