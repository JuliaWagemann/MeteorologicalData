'''
Created on Feb 21, 2014

@author: Julia
'''
###############################################################################
# Script 5_calc_LWP_ZIntegral
# Author: Julia Wagemann
# Date: February 2013
#
# This script takes the theoretical calculated profiles from a temporal subset 
# of a fog event and calculates the LWP and dBZIntegral and writes the values into
# an outputfile
###############################################################################
from numpy.core.numeric import arange
import os
import glob 
import numpy as np
import csv
import math
from scipy import integrate
import re
from operator import itemgetter,attrgetter

# Path to theoretical profiles calculated from Samples2 (temporal subset)
path = 'H:/Masterarbeit/2_Data/3_fog_time_series/dsd/LWP/'

def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList

def writeLineToOutput(outputfile,paras,date):
    colStr = ''
    for i in range(6):
        colStr = colStr + ',' + str(paras[i])
  
    outputfile.write(date + colStr +'\n')

# Function calculateLWP that calculates the Liquid Water Path
def calculateLWP(array,column):
    array_prep = array[array[:,column]>0]
    length=len(array_prep)
    if (length<2):
        Integral = 0.
    else:
        array_prep2 = array_prep[array_prep[:,0]<1000]
        Integral = integrate.trapz(array_prep2[:,column],array_prep2[:,0])
    return Integral

# Function calculateIntegralZ that calculated the integral from vertical Z profiles
def calculateIntegralZ(array,column):
    array_prep = array[array[:,column]>-999]
    length=len(array_prep)
    if(length<2):
        Integral = 0.
    else:
        array_prep2 = array_prep[array_prep[:,0]<1000]
        Integral = integrate.trapz(array_prep2[:,column]+100,array_prep2[:,0])
    return Integral

###########################################################################
# Testing environment
###########################################################################	
event = "20121020_20121021"
fileList1 = getFilesInList(path+event,'*_measured.csv')
fileList2 = getFilesInList(path+event,'*_theoProf_ground.csv')
fileList3 = getFilesInList(path+event,'*_theoProf_Profile.csv')
outputfile1 = open(path+event+'_Integrals.csv','wb')
outputfile1.write('dateTime, LWP_measured_ground, LWP_measured_profile, LWP_ground, LWP_profile, dBZIntegral_measured, dBZIntegral_ground, dBZIntegral_profile\n')
IntegralList = []
for i,j,k in zip(fileList1,fileList2,fileList3):
    with open(i,'r') as file1:
        firstLine = file1.readline()
    
    columns = firstLine.split(',')
    date = columns[4].rstrip('\n')
    print i

    array_measured = np.loadtxt(open(i,"rb"),delimiter=",",skiprows=1) 
    array_ground = np.loadtxt(open(j,"rb"),delimiter=",",skiprows=1)
    array_profile = np.loadtxt(open(k,"rb"),delimiter=",",skiprows=1)
    if array_measured.size==0:
        Integrals = date +','+'-999'+','+'-999'+','+'-999'+','+'-999'+','+'-999'+','+'-999'+','+'-999'+'\n'
        outputfile1.write(Integrals)
        continue
    else:    
        LWP_measured_ground = calculateLWP(array_measured,1)
        LWP_measured_profile = calculateLWP(array_measured,2)   
        LWP_ground = calculateLWP(array_ground,1)
        LWP_profile = calculateLWP(array_profile,1)
        
        dBZIntegral_measured = calculateIntegralZ(array_measured,3)
        dBZIntegral_ground = calculateIntegralZ(array_ground,3)
        dBZIntegral_profile = calculateIntegralZ(array_profile,3)     
    
        Integrals =','+str(LWP_measured_ground)+','+str(LWP_measured_profile)+','+str(LWP_ground)+','+str(LWP_profile)+','+str(dBZIntegral_measured)+','+str(dBZIntegral_ground)+','+str(dBZIntegral_profile)
        outputfile1.write(date+Integrals+'\n')
outputfile1.close()

    
    


