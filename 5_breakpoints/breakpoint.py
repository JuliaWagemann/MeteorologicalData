# -*- coding: utf-8 -*-
'''
Created on Nov 6, 2013

@author: sebastian
'''

# Klasse für Bruchpunktinformation
class breakpoint:
    ID = None        # ID des Bruchpunkts bezogen auf die Gesamt-Zeitreihe
    P  = None        # Geschätzte Wahrscheinlichkeit für den BP
    t  = None        # t-Test-Ergebnis auf Steigung der Teilzeitreihen (True: BP ist gültig)
    z  = None        # Platz auf der Gefunden-Reihenfolge (Erster gefundener BP: 0, zweiter ..: 1, usw)
    
    def __init__(self, ID, P, t, z):
        self.ID = ID
        self.P  = P
        self.t  = t
        self.z  = z
    
    def __cmp__(self, other):
        if self.ID < other.ID: return -1
        if self.ID > other.ID: return 1
        else: return 0