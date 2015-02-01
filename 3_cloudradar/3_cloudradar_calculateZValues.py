'''
Created on Jan 10, 2014

@author: Julia
'''
###############################################################################
# Script 3_cloudradar_calculateZValues
# Author: Julia Wagemann
# Date: September 2013
#
# This script transforms cloudradar dBZ values to Z values - see Master thesis
# for formula
###############################################################################
import glob
import csv
import os
import numpy as np
from numpy import *
from datetime import datetime
import math

# provide path to cloudradar dbz values
path = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/cloudradar/dbz_5min/"

# Function getFilesInList to list all files in a folder
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function to write the outputfile
def writeLineToOutput(outputfile,paras,date):
    colStr = ''
    for i in range(511):
        colStr = colStr + ',' + str(paras[i])
  
    outputfile.write(date + colStr +'\n')

# Function calculateZVals that transforms all the dBZ values to Z values
def calculateZVals(inputFile):
    inputfile = open(inputFile,'r')
    outputfile = open(inputfile.name[:-17] + 'zVals.csv', 'w')

    colStr = ""
    for line in inputfile:
        outList = zeros(511)
        columns = line.split(',')
        if line.startswith('TIME'):
            continue    
        dateTime = datetime.strptime(columns[0],"%Y-%m-%d %H:%M")
        dateTimeFinal = dateTime.strftime("%Y-%m-%d %H:%M")   
        for i in range(511):
            print i
            if columns[i+1]=='-999':
                outList[i] = -999
            else:
                outList[i] =10**(float(columns[i+1])/10)
        writeLineToOutput(outputfile,outList,dateTimeFinal)
    outputfile.close()
 
fileList = getFilesInList(path,'*_5minMean.csv')
for i in fileList:
    calculateZVals(i)