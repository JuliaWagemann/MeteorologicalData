'''
Created on Sep 27, 2013

@author: Julia
'''
###############################################################################
# Script 1_cloudradar_cloudheight_getFogEvents
# Author: Julia Wagemann
# Date: September 2013
#
# This script creates a temporal subset of cloudradar cloudheight data, based 
# on given fog start and end time points.
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

# Provide path to cloudradar cloudheight data and to a .csv with fog start and end times
path1 = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/cloudradar/cloudheight/"
path2 = "H:/Masterarbeit/2_Data/Fog/"

# Function getFileInList to list all files in the folder
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function getFogEvents that takes a fileList as well as fog start and end times and generates
# new files for the specific time period of the fog event
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
        # Check if first line is header
        if line1.startswith('TIME') or line2.startswith('TIME'):
            continue
       
        dateTime1 = datetime.strptime(columns1[0],"%Y-%m-%d %H:%M")
        dateTime2 = datetime.strptime(columns2[0],"%Y-%m-%d %H:%M")
        test1 = datetime.strptime('2012-12-19', "%Y-%m-%d").date()
        colStr1 = ""
        colStr2 = ""
        colStr3 = ""
		# Check if data of 19th December are processed - only fog event during day time
        if dateTime1.date() == test1:
            if dateTime1.time() >= fogStart1.time() and dateTime1.time() <= fogEnd1.time():
                date3 = dateTime1.strftime("%Y-%m-%d %H:%M")
                colStr3=date3+','
                for i in range(7):
                    colStr3+=columns1[i+1]+','
                colStr3+=columns1[8]
                outList3.append(colStr3)
        if len(outList3)!=0:
            ofile = open(inputfile1[:8] + '_' + inputfile1[:8] + '_cloudradar_cloudinfo_5min.csv', 'w')
            ofile.write('dateTime, CloudbaseHeight_1, CloudtopHeight_1, Cloudthickness_1, CloudbaseHeight_2, CloudtopHeight_2, Cloudthickness_2, CloudbaseHeight_3, CloudtopHeight_3, Cloudthickness_3\n')
            for item in outList3:               
                ofile.write(item)
            ofile.close()
		# First all the entries during the fog event from first day are stored in a list
        if dateTime1.time() >= fogStart1.time() and dateTime1.date() == fogStart1.date():
            date1 = dateTime1.strftime("%Y-%m-%d %H:%M")
            colStr1 = date1+','
            for i in range(7):
                colStr1+=columns1[i+1]+','
            colStr1+=columns1[8]
            outList1.append(colStr1)
		# in a seperate list all the entries from the second day are stored
        if dateTime2.time() <= fogEnd1.time() and dateTime2.date() == fogEnd1.date(): 
            date2 = dateTime2.strftime("%Y-%m-%d %H:%M")
            colStr2 = date2 +','
            for i in range(7):
                colStr2+=columns2[i+1]+','
            colStr2+=columns2[8]
            outList2.append(colStr2)
	# both lists are combined and written to a text file
	if len(outList1)!=0:
        ofile = open(inputfile1[:8] + '_' + inputfile2[:8] + '_cloudradar_cloudinfo_5min.csv', 'w')
        ofile.write('dateTime, CloudbaseHeight_1, CloudtopHeight_1, Cloudthickness_1, CloudbaseHeight_2, CloudtopHeight_2, Cloudthickness_2, CloudbaseHeight_3, CloudtopHeight_3, Cloudthickness_3\n')
        for item in outList1:
            ofile.write(item)
        for item in outList2:
            ofile.write(item)
        ofile.close()

# List cloudradar cloudheight data
fileList = getFilesInList(path1,'*.csv')

# Put fog start and end times into Python lists
fogStart = open(path2 + '2012_fogEvents_start.csv', 'r')
start = []
for row in fogStart:
    columns = row.split('\n')
    start.append(columns[0])

end = []
fogEnd = open(path2 + '2012_fogEvents_end.csv', 'r')
for row in fogEnd:
    columns = row.split('\n')
    end.append(columns[0])

# Iterate through fileList
for i,j in zip(fileList,fileList[1:]):
    print i,j
    for x,y in zip(start,end):
        getFogEvents(i,j,x,y)