# -*- coding: utf-8 -*-

# Berechnung MGV-Parameter a, alpha, b, gamma, rc und Omega
# Die Ergebnisse werden in eine Datei fogXX_1min_mgvParam.csv ausgeschrieben.

# Dabei werden folgende Schwankungsbereiche fÃ¼r die MGV-Parameter vorgegeben:
# a:         -
# rc:    0.5 - 50.0
# alpha: 1   - 10
# gamma: 0.0 - 10.0

from numpy import *
from scipy.optimize import leastsq
import os
from os.path import basename
from math import gamma, pi

inputfile  = open('H:/Masterarbeit/2_Data/3_fog_time_series/dsd/dsd.csv', 'r')                   # Hier die jeweilige Input-Datei angeben
outputfile = open( inputfile.name + '_mgvParam.csv', 'w')

#Array fÃ¼r die Tropfenanzahl der Bins von einem Spektrum (= in einer Zeile)
dropCounts = zeros(48)
# Array fÃ¼r die Mittleren Radii der Bins
binRadii   = zeros(48)

# Ausschreibe-Methode fÃ¼r jede Zeile:
def writeLineToOutputfile(UTC,rc,gamma,a,alpha,b,omega):
    outputfile.write(str(UTC) + ',' + str(rc) + ',' + str(gamma) + ',' + str(a) + ',' + str(alpha) + ',' + str(b) + ',' + str(omega) + '\n')
    return

# Omega (alpha, gamma und rc sind die jew. MGV-Parameterwerte)
# Eq. 25 angepasst (Faktor 1/48 ergibt sich durch Teilen von korrektem LWC durch korrektes Z (4/3 geteilt durch 64))
def calculateOmega(rc, gamma, alpha):
    try:
        b = alpha/(gamma * (rc**gamma))
        omega = 1./48. * math.pi * (math.gamma((alpha+4.)/gamma)/math.gamma((alpha+7.)/gamma)) * (b**(3./gamma)) * 10.**(6.)
    except Exception, e:
        omega = -999
    return omega

# Hilfsmethode die Ã¼berprÃ¼ft, ob die Parameter sich noch im erlaubten Schwankungsbereich befinden:
# a wird nicht Ã¼berprÃ¼ft, da es irrelevant ist und alpha wird spÃ¤ter Ã¼berprÃ¼ft, da es ein Integer
# sein muss (alpha muss integer sein, weil bei der GV dann bei der Ableitung mit FakultÃ¤t gerechnet wird, wobei natÃ¼rlich nur Integer erlaubt sind)
def within_bounds(p):
    rc, gamma, a = p
    if (rc>=0.5 and rc<=50):
        if(gamma>0 and gamma<=10):
            return True
        return False
    return False

# Theoretical model
def peval(x, p, alpha):
    rc, gamma, a = p
    return a*x**alpha*exp(-(alpha/gamma)*(x/rc)**gamma)

# Residuals: The function takes into account the statistical error on each bin = sqrt(N), therefore function is N/sqrt(N)=Sqrt(N)
def residuals(p, y, x, alpha):
    if within_bounds(p):
        return sqrt(y) - sqrt(peval(x,p,alpha))
    else:
        return 1E6

# Schreiben des Headers der Output-Datei
outputfile.write('UTC,rc,gamma,a,alpha,b,Omega\n')

for line in inputfile:            # Iterieren durch die Zeilen der Input-Datei
    columns = line.split(';')     # Aufteilen der Linie in die Felder --> werden in "columns" gespeichert
    
    if line.startswith('UTC'):    # Hier wird das binRadii-Array gefÃ¼llt
        for i in range(48):       # Kopieren und Umwandeln der Strings aus "columns" zu float-Werten in "binRadii"
            binRadii[i] = float(columns[i+1])
        continue                  # Hier soll der erste Schleifendurchlauf abgebrochen werden, da nur das binRadii-Array gefÃ¼llt werden sollte
    
    # falls die Zeile kein Spektrum enthÃ¤lt soll in die Output-Datei auch nur eine leere Zeile geschrieben werden:
    if columns[1] == '':
        outputfile.write(columns[0] + ',,,,,,,,\n')
        continue
    
    for i in range(48):           # Kopieren und Umwandeln der Strings aus "columns" zu float-Werten in "dropCounts"
        dropCounts[i] = float(columns[i+1])
    
    # Jetzt kÃ¶nnen die MGV-Parameter bestimmt werden:
    y_meas = zeros(48)
    
    for i in range(48):
        y_meas[i]=dropCounts[i]/0.5     #dropCounts[i] wird hier durch die Breite des Bins geteilt (Nach Durchmesser-Radius-Korrektur sind die Intervalle jetzt nur noch 0.5 ym breit)
    
    # Startvalues for fit (the result should not depend on this, if a minimum is found
    p0 = [ 1., 1., 1. ]
    
    # Initialization of result-Array for MGV-Parameters including sum of squared differences (as measure of best fit)
    # [0] = rc, [1] = gamma, [2] = a, [3] = alpha, [4] = sumOfSqDiffs
    bestFitParameters = zeros(5)
    bestFitParameters[4] = float('inf')            # Setting initial best fit to positive infinite (--> very bad fit)

    # Calling the fit-algorithm for each alpha between 1 and 10
    for alpha in range(10):
        try:
            plsqCur = leastsq(residuals, p0, args=(y_meas, binRadii, alpha+1), full_output=1)
            FitParameters = [ plsqCur[0][0], plsqCur[0][1], plsqCur[0][2], alpha+1, linalg.norm(plsqCur[2]['fvec']) ]
        
            # now it is checked if the new fit is better than any fit before in this iteration. If this is the case the new MGV-Parameters are stored in the bestFitParameters-Array
            if FitParameters[4] < bestFitParameters[4]:
                bestFitParameters = FitParameters
                
        except Exception, e:
            print columns[0] + '   A better fit could be reached when relaxing the bounds'
            
    # Extrahieren der Parameter:
    rc = bestFitParameters[0]
    gamma = bestFitParameters[1]
    a = bestFitParameters[2]
    alpha = bestFitParameters[3]
    
    # Berechnen des Omega-Wertes:
    omega = calculateOmega(rc,gamma,alpha)
    
    # Berechnen von b:
    b = alpha/(gamma*(rc**gamma))
    
    # write all results into output-file
    writeLineToOutputfile(columns[0],rc,gamma,a,alpha,b,omega)

inputfile.close()
outputfile.close()