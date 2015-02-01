'''
Created on Oct 7, 2013

@author: Julia
'''
###############################################################################
# Script 6_cl31_getFogEvents_BS
# Author: Julia Wagemann
# Date: October 2013
#
# This script writes cl31 BS information based on individual fog events
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# path to cl31 backscatter data
path1 = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/cl31/Backscatter/ma_TimeHeight_log/"
# path to start and end times of fog events
path2 = "H:/Masterarbeit/2_Data/Fog/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function getFogEvents that creates a new outpufile for the time frame of the
# fog event given
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

        if line1.startswith('TIME') or line2.startswith('TIME'):
            continue
        dateTime1 = datetime.strptime(columns1[0],"%Y-%m-%d %H:%M")
        dateTime2 = datetime.strptime(columns2[0],"%Y-%m-%d %H:%M")
        test1 = datetime.strptime('2012-12-19', "%Y-%m-%d").date()

        colStr1 = ""
        colStr2 = ""
        colStr3 = ""
        if dateTime1.date() == test1:
            if dateTime1.time() >= fogStart1.time() and dateTime1.time() <= fogEnd1.time():
                date3 = dateTime1.strftime("%Y-%m-%d %H:%M")
                colStr3=date3+','
                for i in range(759):
                    colStr3+=columns1[i+1]+','
                colStr3+=columns1[760]
                outList3.append(colStr3)
        if len(outList3)!=0:
            ofile = open(inputfile1[:8] + '_' + inputfile1[:8] + '_cl31_BS_5min.csv', 'w')
            header = 'TIME,'
            for i in range(761):
                header = header + str(i+1) + ','
            ofile.write(header+'\n')
            for item in outList3:               
                ofile.write(item)
            ofile.close()
        if dateTime1.time() >= fogStart1.time() and dateTime1.date() == fogStart1.date():
            date1 = dateTime1.strftime("%Y-%m-%d %H:%M")
            colStr1 = date1+','
            for i in range(759):
                colStr1+=columns1[i+1]+','
            colStr1+=columns1[760]
            outList1.append(colStr1)
        if dateTime2.time() <= fogEnd1.time() and dateTime2.date() == fogEnd1.date():
            date2 = dateTime2.strftime("%Y-%m-%d %H:%M")
            colStr2 = date2 +','
            for i in range(759):
                colStr2+=columns2[i+1]+','
            colStr2+=columns2[760]
            outList2.append(colStr2)
    if len(outList1)!=0:
        ofile = open(inputfile1[:8] + '_' + inputfile2[:8] + '_cl31_BS_5min.csv', 'w')
        header = 'TIME,' 
        for i in range(760):
            header = header + str(i+1) + ','
        ofile.write(header+'\n')        
        for item in outList1:
            ofile.write(item)
        for item in outList2:
            ofile.write(item)

        ofile.close()

###############################################################################
# Test environment
############################################################################### 
fileList = getFilesInList(path1,'*_5min.csv')
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