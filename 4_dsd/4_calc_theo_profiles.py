# -*- coding: utf-8 -*-
# Umsetzung von Jan Cermaks Methode zur Berechnung eines theoretischen LWC-Profils
# Dabei orientiere ich mich an den Formeln und Beschreibungen aus seiner Diss.
from numpy.core.numeric import arange
import os
import glob 
import numpy as np
import csv
import math
from scipy import integrate

# Path to parameters needed for theoretical profiles
path1 = 'H:/Masterarbeit/2_Data/3_fog_time_series/dsd/params/'
# Path to vertical Z Profiles
path2 = 'H:/Masterarbeit/2_Data/3_fog_time_series/dsd/cloudradar_zSamples2/'

def getFilesInList (path, fileEnding):
    os.chdir(path)
    print "New directory is:" + os.getcwd()
    fileList = glob.glob(fileEnding)
    return fileList


# Literatur:
# (1) Cermak, J. (2006). SOFOS - A new Satellite-based Operational Fog Observation Scheme. Philipps-University of Marburg.
# (2) Brenguier, J.-L., Pawlowska, H., Schüller, L., Preusker, R., Fischer, J., & Fouquart, Y. (2000). 
#     Radiative Properties of Boundary Layer Clouds: Droplet Effective Radius versus Number Concentration. 
#     Journal of the Atmospheric Sciences, 57(6), 803–821. doi:10.1175/1520-0469(2000)057<0803:RPOBLC>2.0.CO;2

# Methode zum Berechnen des adiabatischen LWC-Gehalts in Nebel
# Quelle: Cermak 2006 (Eq. 4.39) / Brenguier 2000
# Input:  Höhe z in [m] über cloudBase
#         cloudbasetemp in Grad C
def adiabaticLWC(z,cloudbasetemp):
    # Laut Cermak: At sea level, it ranges from 1 * 10−3 to 2.5 * 10−3 for temperatures from 0 to 40°C.
    # Annahme: Diese range verläuft linear (so ergibt sich der Faktor von 3.75E-5 (rate = 2.5 bei 40°C))
    rate = 1.0E-3 + 3.75E-5 * cloudbasetemp
    return z * rate

# Methode zur Berechnung des theoretischen Profils von Jan Cermak:
# Quelle: Cermak 2006
# cloudTop:          Höhe der Wolken-/Nebelobergrenze
# cloudBase:         Höhe der Wolken-/Nebeluntergrenze (sollte bei Nebel immer = 0 sein)
# zInc:              Inkrement für Höhenintervalle (in Meter) (= 1)
# betaStatic:        Mixing parameter (Laut Cermak (2006) = 0.3)
# cloudBaseTemp:     Temperatur in °C and der Wolkenuntergrenze (= Temperatur die an der Station gemessen wurde)
# lowestMeasuredLWC: LWC-Wert an der tiefsten Stelle des gemessenen Profils. Von diesem aus wird dann auf den LWC-Wert bei 0m Höhe geschlossen.
# lowestMeasuredAlt: Höhe auf der der lowestMeasuredLWC gemessen wurde
# outputpath:        Pfad für Outputdatei
# outputf:           Name der Outputdatei
#
# @ Julia:
# lowestMeasuredLWC müsste bei dir der LWC-Wert sein, den du vorher aus dem untersten Z-Wert mit Hilfe des mittleren Tropfenspektrums berechnet hast
# lowestMeasuredAlt müsste bei dir dann immer ~30m sein (höhe des untersten range-gates über dem Nahfeld)
# 
def calcTheoreticalLWCProfile(cloudTop,cloudBase,zInc,betaStatic,cloudBaseTemp,lowestMeasuredLWC,lowestMeasuredAlt,omega):    
    LWCs = []
    alts = []
    Zs = []
    logZs = []
    deltaZ = cloudTop - cloudBase       # Absolute Wolkendicke
    
    # Ermittelung der Grenzschichten zwischen den 3 Layern:
    boundary1 = 0.   # Höhe der Grenze zwischen Layer1 und Layer2 (untere und mittlere Schicht)
    boundary2 = 0.   # Höhe der Grenze zwischen Layer2 und Layer3 (mittlere und obere Schicht)
    
    if deltaZ >= 166.67: boundary1 = deltaZ * 0.3 + cloudBase  # boundary1 entspricht 30% der Nebeldicke
    else: boundary1 = 50. + cloudBase                          # boundary1 entspricht 50m über Nebeluntergrenze
    
    if deltaZ >= 500.00: boundary2 = cloudTop - 75.  # boundary2 entspricht 75m unter Nebelobergrenze
    else: boundary2 = cloudTop - deltaZ * 0.15       # boundary2 entspricht 15% von der Gesamtdicke unter Nebelobergrenze = 85% der Nebeldicke
    
    # Anpassung von beta (Eq. 4.44):
    beta = betaStatic * cloudTop / 1000.
    
    # Bestimmung des LWC-Wertes bei 0m Höhe
    # Annahme: Zwischen Boden und niedrigstem LWC-Messpunkt ist der LWC-Gradient subadiabatisch mit beta = betaStatic
    l_LWC_adiab = adiabaticLWC(-lowestMeasuredAlt,cloudBaseTemp)
    l_LWC = (1-beta) * l_LWC_adiab + lowestMeasuredLWC
    
    # Inkrementieren durch das Profil:
    for alt in arange(cloudBase,cloudTop+zInc,zInc):
        # Festlegen von Variablen (u.a. betaCurrent) je nach Schicht:
        betaCurrent = 0.
        
        # Wenn wir uns im unteren Layer befinden:
        if alt <= boundary1:
            betaCurrent = beta * ((alt - cloudBase) / (boundary1 - cloudBase))
            LWC_adiab = adiabaticLWC(alt-cloudBase,cloudBaseTemp)
            LWC = (1-betaCurrent) * LWC_adiab + l_LWC # Eq. 4.43 (ohne Weg über mixing ratio), + l_LWC für Rechtsverschiebung
            
        # Wenn wir uns im mittleren Layer befinden:
        if (alt <= boundary2) and (alt > boundary1):
            betaCurrent = beta
            LWC_adiab = adiabaticLWC(alt-cloudBase,cloudBaseTemp)
            LWC = (1-betaCurrent) * LWC_adiab + l_LWC  # Eq. 4.43 (ohne Weg über mixing ratio), + l_LWC für Rechtsverschiebung
            
        # Wenn wir uns im oberen Layer befinden:
        if alt > boundary2:
            # Hier soll der LWC einfach nur linear abnehmen. D.h. es wird eine Gerade gebildet zwischen
            # 0 (Obergrenze) und LWC-Wert @ boundary2 und für die jeweilige Höhe der entsprechende Wert berechnet:
            LWC = (alt-cloudTop) / ((boundary2 - cloudTop) / ((1-beta) * adiabaticLWC(boundary2-cloudBase,cloudBaseTemp) + l_LWC)) # + l_LWC für Rechtsverschiebung
        
        Z = LWC/omega
        if Z>0:
            logZ = 10*(math.log10(Z))
        else:
            logZ = -999.
        LWCs.append(LWC)
        Zs.append(Z)
        alts.append(alt)
        logZs.append(logZ)

    finalList = zip(alts,LWCs,Zs,logZs)  
    return finalList

# Helper function calculateLWCfromZ that calculates Liquid water content from Z values based on a given Omega
def calculateLWCfromZ(zArray,omega):
    zArray_prep = []
    for i in zArray:
        if (i==-999):
            zArray_prep.append(i)
        else:
            zArray_prep.append(i*omega)
    return zArray_prep

# Helper function convertZtodBZ that converts a given zArray to dBZ values
def convertZtodBZ(zArray):
    zArray_prep = []
    for i in zArray:
        if(i==-999):
            zArray_prep.append(i)
        else:
            zArray_prep.append(10*(math.log10(i)))
    return zArray_prep


###########################################################################
# Testing environment
###########################################################################
fileList1 = getFilesInList(path1,'*_paramsGround_2.csv')
fileList2 = getFilesInList(path1,'*_paramsProfile_2.csv')
fileList3 = getFilesInList(path2,'*.csv')

for i,j,k in zip(fileList1,fileList2,fileList3):
    os.chdir(path1)
    with open(i, 'r') as file1:
        lines1 = file1.readlines()[1:]
    with open(j, 'r') as file2:
        lines2 = file2.readlines()[1:]
    file3 = open(path2+k,'r')
    t=000
    os.makedirs(path1+i[:17])
    os.chdir(path1+i[:17])

    radarAlt = []
    t=000
    for line1,line2,line3 in zip(lines1,lines2,file3):
        if line1.startswith('dateTime'):
            continue
        if line2.startswith('dateTime'):
            continue
        t+=1
        columns1 = line1.split(',')
        columns2 = line2.split(',')
        columns3 = line3.split(',')     
		# two output files - two different theoretical profiles and   
        ofile1 = open(columns1[0][:10]+'_'+str(t)+'_theoProf_Ground.csv', "wb")
        ofile2 = open(columns2[0][:10]+'_'+str(t)+'_theoProf_Profile.csv', "wb")
 
        writer1 = csv.writer(ofile1, delimiter=",")
        writer1.writerow(("alt","LWC","Z","logZ",columns1[0]))
 
        writer2 = csv.writer(ofile2, delimiter=",")
        writer2.writerow(("alt","LWC","Z","logZ",columns1[0]))
		
		# another outputfile that converts the measured Z values to LWC values
        ofile3 = open(columns3[0][:10]+'_'+str(t)+'_measured.csv', "wb")  
           
        writer3 = csv.writer(ofile3, delimiter=",")
        writer3.writerow(("alt","LWC_ground","LWC_profile","dBZ",columns3[0]))              
        
        if math.isnan(float(columns1[1])) or math.isnan(float(columns2[1])):
            continue
        else:           
            arrayGround = calcTheoreticalLWCProfile(float(columns1[1]),float(columns1[2]),float(columns1[3]),float(columns1[4]),float(columns1[5]),float(columns1[6]),float(columns1[7]),float(columns1[8]))
            arrayProfile = calcTheoreticalLWCProfile(float(columns2[1]),float(columns2[2]),float(columns2[3]),float(columns2[4]),float(columns2[5]),float(columns2[6]),float(columns2[7]),float(columns2[8]))  
                            
            for row in arrayGround:
                writer1.writerow(row)
    
            for row in arrayProfile:
                writer2.writerow(row)
        
        ofile1.close()
        ofile2.close()
    
        ZProfile = np.array(map(float,columns3[1:len(columns3)-1]))
        m = 1
        radarAlt.append(0.)
        for i in ZProfile:
            alt = 2000./512*(m)
            radarAlt.append(alt)
            m=m+1        
                   
        LWC_measured_ground = calculateLWCfromZ(ZProfile,float(columns1[8]))
        LWC_measured_profile = calculateLWCfromZ(ZProfile,float(columns2[8]))       
        dBZ_measured = convertZtodBZ(ZProfile)
    
        measuredValues = zip(radarAlt,LWC_measured_ground, LWC_measured_profile, dBZ_measured)                 
        for row in measuredValues:
            writer3.writerow(row)
        
        ofile3.close()
        radarAlt = []        