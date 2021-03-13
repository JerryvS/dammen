import pygame
from .constanten import grijs, wit, blokgrootte, rijen, zwart, kolommen
from .schijven import Schijf
from copy import deepcopy


def print_bord(bord):
    for rijindex, rij in enumerate(bord):
        print(rijindex, end=' ')
        for kolomindex, kolom in enumerate(rij):
            if not kolom:
                print(' ', end='')
            else:
                kleur = 'b'
                if kolom.kleur == wit:
                    kleur = 'w'
                print(kleur, end='')
        print()
    print()

class Bord:
    def __init__(self):
        self.bord = []
        self.schijf_wit = 20
        self.schijf_zwart = 20
        self.dam_zwart = 0
        self.dam_wit = 0
        self.schijven_plaatsen()

    def vierkant(self, scherm):
        scherm.fill(grijs)
        for rij in range(rijen):
            for kolom in range(rij % 2, rijen, 2):
                pygame.draw.rect(scherm, wit, (rij * blokgrootte, kolom * blokgrootte, blokgrootte, blokgrootte))

    def schijven_plaatsen(self):
        for rij in range(rijen):
            self.bord.append([])
            for kolom in range(kolommen):
                if kolom % 2 == ((rij + 1) % 2):
                    if rij < 4:
                        self.bord[rij].append(Schijf(rij, kolom, zwart))
                    elif rij > 5:
                        self.bord[rij].append(Schijf(rij, kolom, wit))
                    else:
                        self.bord[rij].append(0)
                else:
                    self.bord[rij].append(0)

    def bord_schijven(self, scherm):
        self.vierkant(scherm)
        for rij in range(rijen):
            for kolom in range(kolommen):
                schijf = self.bord[rij][kolom]
                if schijf != 0:
                    schijf.tekenen(scherm)

    def zet(self, schijf, rij, kolom, bord=None):
        if bord == None:
            bord = self.bord
        bord[schijf.rij][schijf.kolom], bord[rij][kolom] = bord[rij][kolom], bord[schijf.rij][schijf.kolom]
        schijf.zet(rij, kolom)
        if rij == 0 and schijf.kleur == wit:
            schijf.dam_worden()
            self.dam_wit += 1
        if rij == rijen - 1 and schijf.kleur == zwart:
            schijf.dam_worden()
            self.dam_zwart += 1
        return bord

    def geef_mogelijke_zetten(self, schijf):
        zetten = {}
        _zetten = {}
        for y in range(rijen):
            for x in range(kolommen):
                _schijf = self.bord[y][x]
                if _schijf and _schijf.kleur == schijf.kleur:
                    _zetten.update(self.slaande_zetten(_schijf))
        if _zetten:
            max_lengte = 0
            for zet in _zetten:
                print(zet)
                if len(_zetten[zet]) > max_lengte:
                    max_lengte = len(_zetten[zet])
            for zet in self.slaande_zetten(schijf):
                if len(_zetten[zet]) == max_lengte:
                    zetten.update({zet: _zetten[zet]})
            return zetten
        if schijf:
            if schijf.kleur == wit:
                richting = [-1]
            else: 
                richting = [1]
            if schijf.dam:
                richting = [1, -1]
            for dy in richting:
                for dx in [1, -1]:
                    if schijf.kolom+dx < kolommen:
                        if not self.bord[schijf.rij+dy][schijf.kolom+dx]:
                            zetten[(schijf.rij+dy, schijf.kolom+dx)] = []
        return zetten

    def slaande_zetten(self, schijf, geslagen=[], bord=None):
        if bord == None:
            bord = self.bord
        rij = schijf.rij
        kolom = schijf.kolom
        zetten = {}
        for dy in [1, -1]:
            for dx in [1, -1]:
                desty, destx = rij+dy*2, kolom+dx*2
                if desty < rijen and desty >= 0 and destx < kolommen and destx >= 0:
                    schijf2 = bord[rij+dy][kolom+dx]
                    if schijf2 != 0 and (rij+dy, kolom+dx) not in geslagen:
                        if schijf2.kleur != schijf.kleur and bord[desty][destx] == 0:
                            tempbord = deepcopy(bord)
                            tempbord = self.zet(tempbord[rij][kolom], desty, destx, tempbord)
                            tempbord[rij+dy][kolom+dx] = 0
                            slaandezetten = self.slaande_zetten(tempbord[desty][destx], geslagen+[(rij+dy, kolom+dx)], tempbord)
                            zetten.update(slaandezetten)
                            if not slaandezetten:
                                zetten[(desty, destx)] = geslagen+[(rij+dy, kolom+dx)]
        return zetten

    def verwijder(self, schijf):
        if schijf != 0:
            self.bord[schijf.rij][schijf.kolom] = 0
            if schijf != 0:
                if schijf.kleur == wit:
                    self.schijf_wit -= 1
                else:
                    self.schijf_zwart -= 1

    def winnaar(self):
        if self.schijf_zwart <= 0:
            return wit
        elif self.schijf_wit <= 0:
            return zwart
        return False
