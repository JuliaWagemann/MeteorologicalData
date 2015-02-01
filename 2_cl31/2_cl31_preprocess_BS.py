'''
Created on Oct 4, 2013

@author: Julia
'''
###############################################################################
# Script 2_cl31_preprocess_BS
# Author: Julia Wagemann
# Date: October 2013
#
# This script provides functions to preprocess cl31 backscatter data
###############################################################################
from numpy import *
import math
import os
from os.path import basename
import glob

# Path to cl31 backscatter data
path = "C:/Users/Julia/Desktop/Wagemann_Linden_Daten/cl31_backscatter/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function to write outputfile
def writeLineToOutput(outputfile,paras, date):
    colStr = ''
    for i in range(771):
        colStr = colStr + ',' + str(paras[i])
        
    outputfile.write(date + colStr +'\n')

# Function to aggregate cl31 backscatter data to 1 min aggregated values
def preprocessData(inputFile):
    inputfile = open(inputFile,'r')
# Outputfile
    outputfile = open( inputfile.name[:-4] + '_1min.csv', 'w')

    zaehler = 0
    curZvalues = zeros(771)          # Array fuers Aufsummieren
    time = ''
    date = ''
    
    # Anlegen des Headers
    header = 'TIME,'
    for i in range(771):
        header = header + str(i) + ','
    outputfile.write(header+'\n')
    
    # Jetzt wird Zeile fuer Zeile eingelesen und gemittelt
    for line in inputfile:     
        # Aufteilen der akt. Zeile in columns
        columns = line.split(',')      
        
        if time != columns[0][11:16]:
            if time == '':
                time = columns[0][11:16]
                date = columns[0][0:10]
            else:
                for i in range(771):
                    curZvalues[i] = curZvalues[i]/float(zaehler)
                    if(curZvalues[i]>0):
                        curZvalues[i] = math.log10(curZvalues[i])
                zaehler = 0
                writeLineToOutput(outputfile, curZvalues,date+' '+time)
                for i in range(771):
                    curZvalues[i] = 0
                time = columns[0][11:16]
                date = columns[0][0:10]
        for i in range(771):        # Jetzt wird aufaddiert...
            curZvalues[i] = curZvalues[i] + float(columns[i+1])
                
        zaehler = zaehler + 1
        continue
    
    # Der letzte Block muss auch extra prozessiert und ausgeschrieben werden
    for i in range(771):
        curZvalues[i] = curZvalues[i]/float(zaehler)
        if(curZvalues[i]>0):
            curZvalues[i] = math.log10(curZvalues[i])
    zaehler = 0
                
    writeLineToOutput(outputfile,curZvalues,date+' '+time)
    
    outputfile.close()
    inputfile.close()


###############################################################################
# Test environment
###############################################################################
fileList = getFilesInList(path, '*_BS.csv')
for files in fileList:
    preprocessData(files)