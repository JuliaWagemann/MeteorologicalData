'''
Created on Sep 2, 2013

@author: Julia
'''
###############################################################################
# Script 1_cl31_preprocess
# Author: Julia Wagemann
# Date: September 2013
#
# This script provides functions to preprocess cl31 data
###############################################################################
import glob
import csv
import os
from numpy import *

# path to cl31 raw data
path = "H:/Masterarbeit/2_Data/cl31/"

# list files in fileList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# function that reads cl31 raw data and splits cloud height data from
# Backscatter values
def readInWriteOutData (inputFile): 
    data = csv.reader(open(inputFile), delimiter = ",")
    data.next()
    ofile1 = open(inputFile[:13]+'.csv', "wb")
    ofile2 = open(inputFile[:14]+'BS.csv', "wb")
    writer1 = csv.writer(ofile1, delimiter=",")
    writer2 = csv.writer(ofile2, delimiter=",")
    col_indices = range(33,804)
    line2 = []
    for row in data:
        line1 = ([row[0],row[6],row[7],row[8],row[9]])
        replaceNaNs(line1,'    -5555', '      NaN')
        writer1.writerow(line1)
        line2.extend([row[0]])
        for i in col_indices:
            line2.extend([row[i]])           
        writer2.writerow(line2) 
        line2 = []                   
    ofile1.close()
    ofile2.close()

# help function that replaces the old value with the new value
def replaceNaNs(inputList,old,new):
    for index,item in enumerate(inputList):
        if item==old:
            inputList[index]=new

# function that checks if vertical visibility was measured
# if vertVis was measured (!= nan), then the cloud base height is 0.0
def checkVertVis(input):
    data = csv.reader(open(input), delimiter = ",")
    ofile1 = open(input[:-4]+'_processed.csv', "wb")
    writer1 = csv.writer(ofile1, delimiter=",") 
    ofile1.write('datetime, lowCb, 2nd.Cb, high.Cb, vertVis\n')
    data.next()
    for line in data:
        print line[0]
        if line[4] != 'nan':
            line[1] = '0.0'
        line1 = (line[0], line[1], line[2], line[3], line[4])
        writer1.writerow(line1)
    
    ofile1.close()
    
    
   
# Methode fuer das Ausschreiben einer Zeile in die Output-Datei
def writeLineToOutput(outputfile,paras, date):
    colStr = ''
    for i in range(4):
        colStr = colStr + ',' + str(paras[i])
        
    outputfile.write(date + colStr +'\n')

# Function that averages the cl31 cloud height data to 1 minute aggregated values
def preprocessData(inputfileName):
    print inputfileName
    # Inputfile
    inputfile = open(inputfileName, 'r')
    # Festlegen einer Outputfile
    outputfile = open( inputfile.name[:-4] + '_1min.csv', 'w')
    
    # Jetzt wird Zeile fuerr Zeile eingelesen und zu 1-Minuten-Mittelwerten zusammengefasst
    zaehler = 0.
    counts = [0]*4
    curParas = zeros(4)          # Array fuers Aufsummieren im mom. Aggregationsbereich
    time = ''
    date = ''
#    ersteZeile = False

    outputfile.write('datetime, lowCb, 2nd.Cb, high.Cb, vertVis\n')
    for line in inputfile:        
        columns = line.split(',')    # Aufteilen der akt. Zeile in columns
        # Wenn ein Minutenblock zu Ende ist, soll gemittelt werden
        if time != columns[0][11:16]:
            if time == '':
                time = columns[0][11:16]
                print time
                date = columns[0][0:10]
                print date
            else:
                for i in range(4):
                    if counts[i] < 2 and zaehler > 1:
                        curParas[i] = curParas[i]/float(zaehler-counts[i])
                        counts[i]=0.
                    else:
                        curParas[i] = 'NaN'

                zaehler = 0.
                writeLineToOutput(outputfile,curParas,date + ' ' + time)
                for i in range(4):
                    curParas[i] = 0
                    counts[i]=0
                time = columns[0][11:16]
                date = columns[0][0:10]

        # Aufsummieren der Parameterwerte
        for i in range(4):
            if math.isnan(float(columns[i+1])):
                counts[i] +=1.
                curParas[i] = curParas[i]
            else:
                curParas[i] = curParas[i] + float(columns[i+1])        
            
        zaehler += 1.

    # Die letzte Minute muss explizit ausgeschrieben werden:
    for i in range(4):
        if counts[i] < 2:
            curParas[i] = curParas[i]/float(zaehler-counts[i])
        else:
            curParas[i] = 'NaN'
    writeLineToOutput(outputfile,curParas,date + ' ' + time)

    # Schliessen der Files:
    inputfile.close()
    outputfile.close()
    return


################################################################################################
# Test environment
################################################################################################
fileList = getFilesInList(path, ".csv")

for files in fileList:
    print files
    readInWriteOutData(files)
    preprocessData(files)
#    checkVertVis(files)
