# -*- coding: utf-8 -*-
'''
Created on Nov 6, 2013

@author: sebastian
'''

import sys
from numpy import math, sqrt, cumsum, mean, arange
from numpy import polyfit
from breakpoint import breakpoint
import matplotlib.pyplot as plt

# Methode zum Ausschreiben auf Console:
def prnt(string):
    sys.stdout.write(string)
    sys.stdout.flush()

# Sign-Methode (s. Franks 2. Paper)
def sign_selfmade(x,y):
    if x-y >  0.: return  1.
    if x-y == 0.: return  0.
    if x-y <  0.: return -1.

# Methode um nach einem Bruchpunkt zu suchen:
# var ist dabei das Zeit-Array mit den Parameterwerten
# Returns: Id des ermittelten Bruchpunkts und dessen geschätzte Wahrscheinlichkeit
# Id bezieht sich dabei auf die Python-Array-ID (Erste ID = 0)
# Quelle: KLIWA (2002) Eq. 3.9
def findBreakPoint(var):
    U_list = []                         # Liste für alle berechneten U
    n    = len(var)                     # Gesamtlänge der Zeitreihe
    
    prnt('Suche Bruchpunkt...\n')

    for k in range(0,n):                  # Laufender Zeitindex
        
        # Statusausgabe auf Console
        prnt('\r' + str(k+1) + '/' + str(n))
        
        U = 0.                            # Summe der Vorzeichen
        for i in range(0,k):
            for j in range(k+1,n):
                U += sign_selfmade(var[i],var[j])
        U_list.append(abs(U))
    prnt('\n\n')
    
    # Ergebnis-"Array" [0]: id von Kn, [1]: Geschätzte Wahrscheinlichkeit von Kn
    Kn = max(U_list)
    Kn_id = U_list.index(Kn)
    P = estimateP(n,Kn)
    res = [Kn_id,P]
    return res

# Diese Methode berechnet die geschätzte Wahrscheinlichkeit für den Bruchpunkt K_n (= Wert bei max|U_k,n|)
# Returns: P
# Quelle: KLIWA (2002) Eq. 3.10
def estimateP(n,Kn):
    P = 1 - math.exp((-6 * Kn**2)/(n**3 + n**2))
    return P

# Methode fürs Ausschreiben der Ergebnisse von calcXBreakpoints(var,x):
def printResults(bps):
    prnt('BP\tID\tP\tt\tFund-Reihenfolge\n')
    for i in range(len(bps)):
        prnt(str(i+1) + '\t' + str(bps[i].ID) + '\t' + str(bps[i].P)[:3] + '\t' + str(bps[i].t) + '\t' + str(bps[i].z) + '\n')
        
# Methode fürs Ausschreiben der Ergebnisse von calcXBreakpoints(var,x) in eine Outputdatei:
def printResultsToFile(bps,outputfilePath):
    outputfile = open(outputfilePath,'w')
    outputfile.write('BP,ID,P,t,Fund-Reihenfolge\n')
    for i in range(len(bps)):
        outputfile.write(str(i+1) + ',' + str(bps[i].ID) + ',' + str(bps[i].P)[:3] + ',' + str(bps[i].t) + ',' + str(bps[i].z) + '\n')
    outputfile.close()

# Methode für den Mann-Test
# (nur der klassische Mann-Test - Kendall prüft zusätzlich auf Ties)
# Input: Zu untersuchende Zeitreihe
# Returns: true, falls 0-Hypothese verworfen werden kann (--> Es gibt einen homogenen Trend) 
#          false, falls 0-Hypothese nicht verworfen werden kann (--> kein homogener Trend!)
# Signifikanzniveau = 0.05
# Quelle: Schönwiese (2006) Eq. 14.21
def mannTest(var):
    n = len(var)
    S = 0.
    for i in range(n-1):
        for j in range(i+1,n):
            S += sign_selfmade(var[j],var[i])
    # Varianz:
    v2 = (n*(n-1.)*(2.*n+5.))/18.
    # Q:
    Q = S/sqrt(v2)
    if abs(Q) > 1.96:
        return True
    else:
        return False
    
# Diese Zelle führt die 2-seitigen t-tests auf die Geradensteigungen der Summenlinien der Subzeitreihen durch
# (Testet, ob die beiden Steigungen tatsächlich unterschiedlich sind)
# FRANKS GLEICHUNG


# Hill's approx. inverse t-dist.: Comm. of A.C.M Vol.13 No.10 1970 pg 620.
# Calculates t given df and two-tail probability.
# Gefunden auf: http://eswf.uni-koeln.de/glossar/surfstat/t.htm (Seiten-Quelltext)
def calcTvalue(p, df):
    t = None
    if (df == 1):
        t = math.cos(p*math.pi/2.)/math.sin(p*math.pi/2.)
    elif (df == 2):
        t = math.sqrt(2./(p*(2. - p)) - 2.)
    else:
        a = 1./(df - 0.5)
        b = 48./(a*a)
        c = ((20700.*a/b - 98.)*a - 16.)*a + 96.36
        d = ((94.5/(b + c) - 3.)/b + 1.)*math.sqrt(a*math.pi*0.5)*df
        x = d*p
        y = pow(x, 2./df)
        if (y > 0.05 + a):
            x = Norm_z(0.5*(1. - p))
            y = x*x
            if (df < 5.): 
                c = c + 0.3*(df - 4.5)*(x + 0.6)
            c = (((0.05*d*x - 5.)*x - 7.)*x - 2.)*x + b + c
            y = (((((0.4*y + 6.3)*y + 36.)*y + 94.5)/c - y - 3.)/b + 1.)*x
            y = a*y*y
            if (y > 0.002): 
                y = math.exp(y) - 1.
            else:
                y = 0.5*y*y + y
            t = sqrt(df*y)
        else:
            y = ((1./(((df + 6.)/(df*y) - 0.089*d - 0.822)*(df + 2.)*3.) + 0.5/(df + 4.))*y - 1.)*(df + 1.)/(df + 2.) + 1./y;
            t = math.sqrt(df*y)
    return t

# Returns z given a half-middle tail type p
# Gefunden auf: http://eswf.uni-koeln.de/glossar/surfstat/t.htm (Seiten-Quelltext)
def Norm_z(p):
    a0,a1,a2,a3  = 2.5066282,  -18.6150006, 41.3911977,  -25.4410605
    b1,b2,b3,b4  = -8.4735109, 23.0833674,  -21.0622410, 3.1308291
    c0,c1,c2,c3  = -2.7871893, -2.2979648,  4.8501413,   2.3212128
    d1,d2,r,z    = 3.5438892,  1.6370678,   None,        None
    if (p>0.42):
        r=math.sqrt(-math.log(0.5-p));
        z=(((c3*r+c2)*r+c1)*r+c0)/((d2*r+d1)*r+1)
    else:
        r=p*p
        z=p*(((a3*r+a2)*r+a1)*r+a0)/((((b4*r+b3)*r+b2)*r+b1)*r+1)
    return z

# Diese Funktion berechnet den Wert t_dach (entspr. Franks Gleichung aus Programm.f90 - KLIWA (2002) Eq. 3-11 oder verändert nach Schönwiese (2006): 11-93)
# und vergleicht das Ergebnis mit dem t-Wert, der bei den gegebenen Freiheitsgraden gerade noch signifikant ist (Signifikanzniveau: 0.01)
# Input: 2 Teilzeitreihen (nur die ursprünglichen Parameterwerte. Doppelsummen werden intern gebildet)
# Returns: True, falls t_dach im Signifikanzbereich liegt (--> Geradensteigungen unterscheiden sich)
#          False, falls t_dach NICHT im Signifikanzbereich liegt (--> Geradensteigungen unterscheiden sich NICHT)
def tTestOnSlope(timeseries1,timeseries2):
    # Berechnung der summierten Parameterwerte (Entspricht y1, y2 in Kliwa (2002) Eq. 3.11):
    x1            = cumsum(timeseries1)
    x2            = cumsum(timeseries2)

    # Anlegen der Zeit-Arrays
    times1        = range(1,len(timeseries1)+1)
    times2        = range(1,len(timeseries2)+1)

    # Berechnung der summierten Zeiten (Entspricht x1, x2 in Kliwa (2002) Eq. 3.11):
    t1            = cumsum(times1) 
    t2            = cumsum(times2)

    # Berechnung der linearen Regressionsgleichungen für die beiden Subzeitreihen:
    b1, a1 = polyfit(t1,x1,1)
    b2, a2 = polyfit(t2,x2,1)

    # Berechnung der Covarianzen
    #sx1t1  = cov(t1,x1)[0][1]
    #sx2t2  = cov(t2,x2)[0][1]
    
    # Berechnung der Länge der Zeitreihen
    n1     = len(x1)
    n2     = len(x2)
    
    # Berechnung von Qt1 und Qt2 (KLIWA (2002) - Eq. 3.13)
    Qt1    = sum((t1-mean(t1))**2)
    Qt2    = sum((t2-mean(t2))**2)

    # Berechnung der Schätzwerte x1_dach und x2_dach (Schönwiese, 2006: 11-9)
    x1_dach = a1+b1*t1
    x2_dach = a2+b2*t2

    # Berechung der Restvarianz (Schönwiese, 2006: 11-20)
    x1_RestVAR = sum((x1-x1_dach)**2)/(len(x1)-2)
    x2_RestVAR = sum((x2-x2_dach)**2)/(len(x2)-2) 

    # Berechnung der Freiheitsgrade:
    m = n1 + n2 - 4
    
    # Berechnung von t_dach (entspr. Franks Gleichung aus Programm.f90 - KLIWA (2002) Eq. 3-11 oder verändert nach Schönwiese (2006): 11-93)
    t_dach = (abs(b1-b2))/(sqrt(((x1_RestVAR*((len(x1)-2))+x2_RestVAR*((len(x2)-2)))/m)*((1/Qt1)+ 1/Qt2)))

    # Berechnung des t-Wertes für das Signifikanzniveau von 0.01 bei den gegebenen Freiheitsgraden:
    t = calcTvalue(0.01,m)
    if t_dach > t:
        return True   # t-Wert übersteigt 0.01-Signifikanzniveau  (--> Geradensteigungen sind unterschiedlich)
    else:
        return False  # t-Wert liegt unter 0.01-Signifikanzniveau (--> Geradensteigungen sind NICHT unterschiedlich)
    
# Diese Methode berechnet X Bruchpunkte für eine Zeitreihe (var)
# Dabei wird die gesamte Zeitreihe zuerst an einem ersten Bruchpunkt zweigeteilt.
# Für die längere Subzeitreihe wird anschließend ein zweiter Bruchpunkt gesucht.
# Damit hat man 3 Subzeitreihen (geteilt an den beiden bereits gefundenen Bruchpunkten)
# Dann wird aus diesen 3 Subzeitreihen die längste gesucht und für diese wieder ein BP gesucht
# usw...
# Returns: Die X Bruchpunkte und deren jeweilige geschätzte Wahrscheinlichkeit
def calcXBreakpoints(var,x):
    totalLength = len(var)
    # Array für Bruchpunkte:
    bps = []
    
    # Schleife für die x Bruchpunkte:
    for i in range(x):
        prnt(str(i+1) + '. Bruchpunkt:\n')
        
        # Finden der aktuell längsten Sub-Zeitreihe:
        # Durchgehen der bereits ermittelten Bruchpunkte
        TsLength = 0
        start = 0
        stop = len(var)
        
        for j in arange(len(bps)+1):
            # Anfang:
            if len(bps) == 0:
                continue
                
            if j == 0:
                curTsLength = bps[j].ID
                # Falls die aktuelle die längste bisherige Subzeitreihe ist
                # sollen Start- und End-ID dieser Zeitreihe übergeben werden:
                if curTsLength > TsLength:
                    TsLength = curTsLength
                    start = 0
                    stop  = bps[j].ID
            
            elif j == len(bps):
                curTsLength = (totalLength-1) - bps[j-1].ID
                if curTsLength > TsLength:
                    TsLength = curTsLength
                    start = bps[j-1].ID
                    stop  = totalLength - 1
            
            else:
                curTsLength = bps[j].ID - bps[j-1].ID
                if curTsLength > TsLength:
                    TsLength = curTsLength
                    start = bps[j-1].ID
                    stop  = bps[j].ID
        
        prnt('Untersuchung der Subzeitreihe von ' + str(start) + ' bis ' + str(stop) + '\n')
        longestSubTimeSeries = var[start:stop]
        # Hier wird noch auf Mindestlänge der Subzeitreihe getestet (min. n >= 40 (??))
        # Falls die längste Subzeitreihe kürzer ist, als 40 wird abgebrochen
        if len(longestSubTimeSeries) < 40:
            break
        
        # Suche BP zur längsten Subzeitreihe:
        curBP = findBreakPoint(longestSubTimeSeries)

        # Splitten der longestSubTimeSeries am gefundenen BP:
        subTimeSeries1 = longestSubTimeSeries[:curBP[0]]
        subTimeSeries2 = longestSubTimeSeries[curBP[0]:]
        
        # TODO: Hier Nur wenn True: Weitermachen
        t = tTestOnSlope(subTimeSeries1,subTimeSeries2)
        
        # Speichern des gefundenen Bruchpunkts als breakpoint-Objekt
        # Dabei wird die ID des Bruchpunkts bezogen auf die komplette Zeitreihe angepasst (+start)
        curBP = breakpoint(curBP[0] + start,curBP[1],t,i)
        # An BP-Array anhängen
        bps.append(curBP)
        # Sortieren des Arrays nach der ID (Ist in breakpoint-Klasse in der compare-Methode so definiert:
        list.sort(bps)
    return bps

# Diese Methode erzeugt einen Plot der untersuchten Zeitreihe zusammen mit den übergebenen Bruchpunkten
# Input: var = Zeitreihe, bps = Liste von Bruchpunkten
def makePlotWithBps(var,bps):
    plt.figure()
    plt.plot(var)
    ylim = plt.ylim()
    for k in bps:
        bpid = k.ID
        plt.vlines(bpid,ymin=ylim[0],ymax=ylim[1],linestyles='-',colors='r')
    plt.show()
