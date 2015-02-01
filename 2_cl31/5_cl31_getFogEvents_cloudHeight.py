'''
Created on Sep 21, 2013

@author: Julia
'''
###############################################################################
# Script 5_cl31_getFogEvents_cloudHeight
# Author: Julia Wagemann
# Date: September 2013
#
# This script write cl31 cloudHeight information based on individual fog events
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# path to cl31 cloud height information data
path1 = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/cl31/Cloud/"
# path to start and end times of fog events
path2 = "H:/Masterarbeit/2_Data/Fog/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function getFogEvents that creates a new outputfile for the time period
# of the given fog event
def getFogEvents(inputfile1,inputfile2,fogStart,fogEnd):
    file1 = open(inputfile1, 'r')
    file2 = open(inputfile2, 'r')
    outList1 = []
    outList2 = []
    outList3 = []
    
    for line1, line2 in zip(file1,file2):
        columns1 = line1.split(',')
        columns2 = line2.split(',')

        fogStart1 = datetime.strptime(fogStart,"%Y-%m-%d %H:%M")
        fogEnd1 = datetime.strptime(fogEnd,"%Y-%m-%d %H:%M")
        
        if line1.startswith('datetime') or line2.startswith('datetime'):
            continue
        dateTime1 = datetime.strptime(columns1[0],"%Y-%m-%d %H:%M")
        dateTime2 = datetime.strptime(columns2[0],"%Y-%m-%d %H:%M")
        test1 = datetime.strptime('2012-12-19', "%Y-%m-%d").date()
        if dateTime1.date() == test1:
            if dateTime1.time() >= fogStart1.time() and dateTime1.time() <= fogEnd1.time():
                date3 = dateTime1.strftime("%Y-%m-%d %H:%M")
                colStr3 = date3 + ',' + columns1[1] + ',' + columns1[2] + ',' + columns1[3] + ',' + columns1[4]
                outList3.append(colStr3)
        if len(outList3)!=0:
            ofile = open(inputfile1[:9] +  inputfile1[:9] + 'cl31.csv', 'w')
            ofile.write('datetime, lowCb, 2nd.Cb, high.Cb, vertVis\n')
            for item in outList3:               
                ofile.write(item)
            ofile.close()
        if dateTime1.time() >= fogStart1.time() and dateTime1.date() == fogStart1.date():
            date1 = dateTime1.strftime("%Y-%m-%d %H:%M")
            colStr1 = date1 + ',' + columns1[1] + ',' + columns1[2] + ',' + columns1[3] + ',' + columns1[4]
            outList1.append(colStr1)
        if dateTime2.time() <= fogEnd1.time() and dateTime2.date() == fogEnd1.date(): 
            date2 = dateTime2.strftime("%Y-%m-%d %H:%M")
            colStr2 = date2 + ',' + columns2[1] + ',' + columns2[2] + ',' + columns2[3] + ',' + columns2[4]
            outList2.append(colStr2)
    if len(outList1)!=0:
        ofile = open(inputfile1[:9] + inputfile2[:9] + 'cl31.csv', 'w')
        ofile.write('datetime, lowCb, 2nd.Cb, high.Cb, vertVis\n')
        for item in outList1:
            ofile.write(item)
        for item in outList2:
            ofile.write(item)

        ofile.close()

###############################################################################
# Test environment
############################################################################### 
fileList = getFilesInList(path1,'*_processed.csv')
fogStart = open(path2 + '2012_fogEvents_start.csv', 'r')
start = []
end = []
for row in fogStart:
    columns = row.split('\n')
    start.append(columns[0])

fogEnd = open(path2 + '2012_fogEvents_end.csv', 'r')
for row in fogEnd:
    columns = row.split('\n')
    end.append(columns[0])

for i,j in zip(fileList,fileList[1:]):
    print i,j
    for x,y in zip(start,end):
        getFogEvents(i,j,x,y)