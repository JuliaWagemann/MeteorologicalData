'''
Created on Sep 27, 2013

@author: Julia
'''
###############################################################################
# Script 2_cloudradar_dbz_getFogEvents
# Author: Julia Wagemann
# Date: September 2013
#
# This script creates a temporal subset of cloudradar dbz data, based 
# on given fog start and end time points.
###############################################################################
import glob
import csv
import os
import numpy as np
from datetime import datetime

path1 = "H:/Masterarbeit/2_Data/2_Daten_gemittelt/cloudradar/dbz/"
path2 = "H:/Masterarbeit/2_Data/Fog/"

# Function getFileInList
def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

# Function getFogEvents that create temporal subsets of a file list based on given fog start and end times
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
                for i in range(510):
                    colStr3+=columns1[i+1]+','
                colStr3+=columns1[511]+'\n'
                outList3.append(colStr3)
        if len(outList3)!=0:
            ofile = open(inputfile1[:8] + '_' + inputfile1[:8] + '_dbz1min_fog.csv', 'w')
            ofile.write('TIME,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511\n')
            for item in outList3:               
                ofile.write(item)
            ofile.close()
		# First all the entries during the fog event from first day are stored in a list
        if dateTime1.time() >= fogStart1.time() and dateTime1.date() == fogStart1.date():
            date1 = dateTime1.strftime("%Y-%m-%d %H:%M")
            colStr1 = date1+','
            for i in range(510):
                colStr1+=columns1[i+1]+','
            colStr1+=columns1[511]+'\n'
            outList1.append(colStr1)
		# in a seperate list all the entries from the second day are stored			
        if dateTime2.time() <= fogEnd1.time() and dateTime2.date() == fogEnd1.date(): 
            date2 = dateTime2.strftime("%Y-%m-%d %H:%M")
            colStr2 = date2 +','
            for i in range(510):
                colStr2+=columns2[i+1]+','
            colStr2+=columns2[511]+'\n'
            outList2.append(colStr2)
	# both lists are combined and written to a text file
    if len(outList1)!=0:
        ofile = open(inputfile1[:8] + '_' + inputfile2[:8] + '_dbz1min_fog.csv', 'w')
        ofile.write('TIME,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511\n')
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