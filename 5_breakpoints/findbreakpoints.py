# -*- coding: utf-8 -*-
'''
Created on Nov 6, 2013

@author: sebastian
'''
import getopt
from matplotlib.mlab import csv2rec
import sys

from breakpoint_utils import calcXBreakpoints, printResults, makePlotWithBps, \
    printResultsToFile

def usage():
    print '\n\nObligatorische Parameter:'
    print '-i --input:    Pfad der Inputdatei.'
    print '-v --variable: Name der zu untersuchenden Variable wie sie in der Inputfile im Header steht. Wichtig: Nur Kleinbuchstaben!'
    print '\nOptionale Parameter:'
    print '-b --bpcount:  Anzahl der zu suchenden Bruchpunkte. Standard ist auf 2 festgelegt.'
    print '-h --help:     Gibt diese Hilfe aus.'
    print '-p --plot:     Erzeugt einen Plot der untersuchten Zeitreihe zusammen mit den gefundenen Bruchpunkten.'
    print '-o --output:   Pfad der Outtdatei. In diese werden die zusammengefassten Informationen zu den gefundenen Bruchpunkten geschrieben.'
    print '\n'
    return

def main(argv):
    # Boolean-Werte als Schalter für (nicht) vorhandene Übergabe-Parameter vom User
    inputfileSpecified = False
    outputfileSpecified = False
    variableSpecified = False
    makeplot = False
    
    # Weitere nötige Felder:
    inputfilePath = ''
    outputfilePath = ''
    breakpointCount = 2
    variableName = ''   

    try:
        opts, args = getopt.getopt(argv, "hpb:i:v:o:", ["help","plot","bpcount=","input=","variable=","output="])
    except getopt.GetoptError:
        sys.exit(2)
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ('-p', "--plot"):
            makeplot = True
        elif opt in ('-b', "--bpcount"):
            breakpointCount = int(arg)
        elif opt in ("-i", "--input"):
            inputfileSpecified = True
            inputfilePath = arg
        elif opt in ("-v", "--variable"):
            variableSpecified = True
            variableName = arg
        elif opt in ("-o", "--output"):
            outputfileSpecified = True
            outputfilePath = arg
            
    if inputfileSpecified and variableSpecified:
        data = csv2rec(inputfilePath)
        try:
            var = data[variableName]
        except ValueError:
            print 'Der angegebene Variablenname konnte nicht gefunden werden. Bitte überprüfen Sie die Angabe auf korrekte Schreibweise und achten Sie darauf, dass der Variablenname nur Kleinbuchstaben enthalten darf'
            sys.exit(2)
    else:
        print 'Inputdatei und/oder Variablenname nicht angegeben! --help für weitere Informationen...'
        sys.exit(2)
    
    bps = calcXBreakpoints(var,breakpointCount)
    printResults(bps)

    if makeplot:
        makePlotWithBps(var,bps)
        
    if outputfileSpecified:
        print '\nSchreibe Bruchpunkt-Infos in ' + outputfilePath
        printResultsToFile(bps,outputfilePath)
       
    print 'Done...'
    
if __name__ == "__main__":
    main(sys.argv[1:])
