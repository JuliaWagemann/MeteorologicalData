'''
Created on Oct 5, 2013

@author: Julia
'''
###############################################################################
# Script 3_cl31_smoothBS
# Author: Julia Wagemann
# Date: October 2013
#
# This script provides functions to smooth cl31 backscatter data
###############################################################################
import numpy as np
from numpy import *
import os
from os.path import basename
import glob
import csv
from datetime import datetime, timedelta


# path to cl31 backscatter data, aggregated to 1 min
path = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/cl31/Backscatter/ma_Time"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function to write outputfile, after smoothed over height (columns)
def writeLineToOutputHeight(outputfile,paras,date):
    colStr = ''
    for i in range(760):
        colStr = colStr + ',' + str(paras[i])
        
    outputfile.write(date + colStr +'\n')

# Function write outpufile, after smoothed over time (rows)
def writeLineToOutputTime(outputfile,paras,date):
    colStr = ''
    for i in range(771):
        colStr = colStr + ',' + str(paras[i])
        
    outputfile.write(date + colStr +'\n')

# Function averageTime, that aggregated row values based on the given timeStep values
# recommended after Muenkel: 20 minutes
def averageTime(inputfile,timeSteps):
    arrayVals = np.loadtxt(open(inputfile,"rb"),delimiter =",",usecols=range(1,772))
    inputFile = open(inputfile,'r')
    ofile = open(inputFile.name[:-8]+'_maTime.csv','w')
    dateTime = []
    for line in inputFile:
        if line.startswith('TIME'):
            continue
        columns = line.split(',')
        a = columns[0]
        dateTime.append(a)
    print len(dateTime)
    for i in range(len(dateTime)-timeSteps):
        timeStepEnd = timeSteps+i
        subset = arrayVals[i:timeStepEnd]
        subsetSum = map(sum,zip(*subset))
        result = [x/timeSteps for x in subsetSum]
        writeLineToOutputTime(ofile,result,dateTime[i])
    ofile.close()
    
# function averageHeight, that aggregates column values
def averageHeight(inputfile):
    inputFile = open(inputfile,'r')
    ofile = open(inputFile.name[:-10]+'_averaged.csv','w')      
    curValues = zeros(760)
    for line in inputFile:
        columns = line.split(',')
        dateTime = columns[0]
        sumVal = 0
        # different aggregation values depending on the height are recommended
        # compare .pdf of Master thesis
        for i in range(760):
            if i == 0:
                curValues[i]=columns[i+1]
                if(curValues[i]> 0):
                    curValues[i]=math.log10(curValues[i])
            if i > 0 and i<6:
                subset1 = columns[1:i*2+2]
                for item in subset1:
                    sumVal = sumVal + float(item)
                curValues[i] = sumVal/(len(subset1))
                if(curValues[i]> 0):
                    curValues[i] = math.log10(curValues[i])
                sumVal = 0
            if i > 5 and i< 51:
                subset2 = columns[i-5:i+8]
                for item in subset2:
                    sumVal = sumVal + float(item)
                curValues[i] = sumVal/13
                if(curValues[i]> 0):    
                    curValues[i] = math.log10(curValues[i])
                sumVal = 0
            if i > 50 and i< 201:
                subset3 = columns[i-7:i+10]
                for item in subset3:
                    sumVal = sumVal + float(item)
                curValues[i] = sumVal/17
                if(curValues[i]> 0):
                    curValues[i] = math.log10(curValues[i])
                sumVal = 0
            if i > 200 and i< 761:
                subset4 = columns[i-9:i+11]
                for item in subset4:
                    sumVal = sumVal + float(item)
                curValues[i] = sumVal/21
                if(curValues[i]> 0):
                    curValues[i] = math.log10(curValues[i])
                sumVal = 0
        writeLineToOutputHeight(ofile,curValues,dateTime)
    ofile.close()
    inputFile.close()

# Function appendTimeRows, which appends the 20 minutes of the subsequent day to each file,
# for averaging over time (rows)
def appendTimeRows (inputfile1, inputfile2):
    csv1 = csv.reader(open(inputfile1),delimiter=",")
    csv2 = csv.reader(open(inputfile2),delimiter=",")
    ofile = open(inputfile1[:-4]+'_neu.csv','wb')
    writer = csv.writer(ofile,delimiter=",")

    for row1 in csv1:
        if row1[0]=="TIME":
            continue     
        dataLine1 = row1
        writer.writerow(dataLine1)
    for row2 in csv2:
        if row2[0]=="TIME":
            continue    
        dateTime = datetime.strptime(row2[0], "%Y-%m-%d %H:%M")
        timeFinal = datetime.strptime(inputfile2[0:4]+'-'+inputfile2[4:6]+'-'+inputfile2[6:8]+" 00:20", "%Y-%m-%d %H:%M")
        if dateTime < timeFinal:
            dataLine2 = row2
            writer.writerow(dataLine2)
        else:
            break  
    ofile.close()

###############################################################################
# Test environment
############################################################################### 

fileList = getFilesInList(path,"*maTime.csv")
print fileList

# first step before average over time --> append time rows to each file
for file1,file2 in zip(fileList,fileList[1:]):
    first = open(file1,'r')
    second = open(file2,'r')
    for row1,row2 in zip(first,second):
        columns1 = row1.split(',')
        columns2 = row2.split(',')
        
        if row1.startswith('TIME') or row2.startswith('TIME'):
            continue        
        dateTime1 = datetime.strptime(columns1[0],"%Y-%m-%d %H:%M")
        dateTime2 = datetime.strptime(columns2[0],"%Y-%m-%d %H:%M")
        break
    dateTime3 = dateTime1.date()+timedelta(days=1)
    if dateTime2.date() == dateTime3:
        appendTimeRows(file1,file2)

# second step, average first over time and then over height
for files in fileList:
    print files
    averageTime(files,20)
    averageHeight(files)

