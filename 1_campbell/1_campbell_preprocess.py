#!/usr/bin/python

'''
Created on Aug 19, 2013

@author: Julia
'''
###############################################################################
# Script 1_campbell_preprocess
# Author: Julia Wagemann
# Date: August 2013
#
# This script provides several functions that help to preprocess data from the
# Campbell data logger
###############################################################################
import os
import csv
import glob


# Identify path to raw Campbell data
path = "H:/Masterarbeit/2_Data/1_Ausgangsdaten/campbell/campbell/"

# function that adds all .csv files into a list
def getFilesInList (path):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob("*.csv")
    return fileList

# function that helps to combine campbell data in two seperate files
# (if radiation data are stored in a separate file, e.g. 30.10 - 20.12)
# The combined data are written to a new .csv file
# Header of the oututfile is as follows:
# Tair_Avg, VIS_Up_Avg, Vis_down_avg, IR_Up_avg, IR_Down_Avg, IR_Up_T_Avg, IR_Down_T_Avg, Rs_net_Avg, RI_net_Avg, Rn_Avg, 
# Tdry_Avg, Twet_Avg, VP_Avg, VP_sat_Avg, rH_psy_Avg, HMP45_T1_Avg, HMP45_T2, HMP45_rH1, HMP45_rH2
def mergeCsvs (fileList):
    for i,j in zip(fileList, fileList[1:])[::2]:
        print "i = " + i
        print "j = " + j
        csv1 = csv.reader(open(i), delimiter = ",")
        csv2 = csv.reader(open(j), delimiter = ",")
        ofile = open(i[:8]+'.csv', "wb")
        writer = csv.writer(ofile, delimiter=",")
        for a in csv2:
            dataLineA = a[2:len(a)]  
            for b in csv1:
                if(b[0] == a[0]):
                    dataLineB = b
                    dataLineB.extend(dataLineA)
                    break
                else:
                    continue
            print dataLineB
            writer.writerow(dataLineB)
        ofile.close()

# function that reads in files of a fileList and restructures the columns of
# the input file.
# Header of the oututfile is as follows:
# Tair_Avg, VIS_Up_Avg, Vis_down_avg, IR_Up_avg, IR_Down_Avg, IR_Up_T_Avg, IR_Down_T_Avg, Rs_net_Avg, RI_net_Avg, Rn_Avg, 
# Tdry_Avg, Twet_Avg, VP_Avg, VP_sat_Avg, rH_psy_Avg, HMP45_T1_Avg, HMP45_T2, HMP45_rH1, HMP45_rH2
def readInWriteOutData (fileList):  
    for i in fileList[:1]:      
        data = csv.reader(open(i), delimiter = ",")
        ofile = open(i[:8]+'.csv', "wb")
        print ofile
        writer = csv.writer(ofile, delimiter=",")
        for row in data:
            line = ([row[0],row[1],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[2],row[3],row[4],row[5],row[6],row[18],row[19],row[20],row[21]]) 
            writer.writerow(line)
        ofile.close()


################################################################################################
# Test environment
################################################################################################
fileList = getFilesInList(path)
mergeCsvs(fileList)

