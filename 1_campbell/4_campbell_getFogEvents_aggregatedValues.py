'''
Created on Jan 9, 2014

@author: Julia
'''

###############################################################################
# Script 4_campbell_getFogEvents_aggregatedValues
# Author: Julia Wagemann
# Date: January 2014
#
# This script adds campbell files aggregated to 5min values based on fog start and end values
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# path of the campbell 5min aggregated files
path1 = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/campbell/campbell_5min/"
# path of files with fog start and end times
path2 = "H:/Masterarbeit/2_Data/Fog/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# function getFogEvents that creates a new files for the timeframe of
# the given fog events
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
        
        if line1.startswith('dateTime') or line2.startswith('dateTime'):
            continue
  
        dateTime11 = columns1[0][:-3]
        dateTime1 = datetime.strptime(dateTime11,"%Y-%m-%d %H:%M")
        dateTime22 = columns2[0][:-3]
        dateTime2 = datetime.strptime(dateTime22,"%Y-%m-%d %H:%M")
             
        test1 = datetime.strptime('2012-12-19', "%Y-%m-%d").date()
        colStr1 = ""
        colStr2 = ""
        colStr3 = ""
        if dateTime1.date() == test1:
            if dateTime1.time() >= fogStart1.time() and dateTime1.time() <= fogEnd1.time():
                date3 = dateTime1.strftime("%Y-%m-%d %H:%M")
                colStr3=date3+','
                for i in range(3):
                    colStr3+=columns1[i+1]+','
                colStr3+=columns1[4]
                outList3.append(colStr3)
        if len(outList3)!=0:
            ofile = open(inputfile1[:8] + '_' + inputfile1[:8] + '_campbell_5min.csv', 'w')
            ofile.write('dateTime,T1_2m_Avg,T2_10m_Avg,rH_2m,rH_10m\n')
            for item in outList3:               
                ofile.write(item)
            ofile.close()
        if dateTime1.time() >= fogStart1.time() and dateTime1.date() == fogStart1.date():
            date1 = dateTime1.strftime("%Y-%m-%d %H:%M")
            colStr1 = date1+','
            for i in range(3):
                colStr1+=columns1[i+1]+','
            colStr1+=columns1[4]
            outList1.append(colStr1)
        if dateTime2.time() <= fogEnd1.time() and dateTime2.date() == fogEnd1.date(): 
            date2 = dateTime2.strftime("%Y-%m-%d %H:%M")
            colStr2 = date2 +','
            for i in range(3):
                colStr2+=columns2[i+1]+','
            colStr2+=columns2[4]
            outList2.append(colStr2)
    if len(outList1)!=0:
        ofile = open(inputfile1[:8] + '_' + inputfile2[:8] + '_campbell_5min.csv', 'w')
        ofile.write('dateTime,T1_2m_Avg,T2_10m_Avg,rH_2m,rH_10m\n')
        for item in outList1:
            ofile.write(item)
        for item in outList2:
            ofile.write(item)

        ofile.close()

################################################################################################
# Test environment
################################################################################################
fileList = getFilesInList(path1,'*.csv')
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