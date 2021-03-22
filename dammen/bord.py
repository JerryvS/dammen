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

    def is_op_bord(self, y, x):
        return y < rijen and y >= 0 and x < kolommen and x >= 0

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
        # Check voor elke schijf van dezelfde kleur of hij iets kan slaan en voeg die zetten toe aan '_zetten'
        for y in range(rijen):
            for x in range(kolommen):
                _schijf = self.bord[y][x]
                if _schijf and _schijf.kleur == schijf.kleur:
                    _zetten.update(self.slaande_zetten(_schijf))
        # Als er slaande zetten zijn, voeg dan alleen de zetten die de meeste andere stukken pakken toe aan 'zetten'
        if _zetten:
            max_lengte = 0
            for zet in _zetten:
                if len(_zetten[zet]) > max_lengte:
                    max_lengte = len(_zetten[zet])
            schijfzetten = self.slaande_zetten(schijf)
            for zet in schijfzetten:
                if len(schijfzetten[zet]) == max_lengte:
                    zetten.update({zet: schijfzetten[zet]})
            return zetten
        # Als er geen slaande zetten zijn, voeg dan de normale diagonale zetten toe
        if schijf.kleur == wit:
            richting = [-1]
        else: 
            richting = [1]
        if schijf.dam:
            richting = [1, -1]
        for dy in richting:
            for dx in [1, -1]:
                desty, destx = schijf.rij+dy, schijf.kolom+dx
                if self.is_op_bord(desty, destx) and not self.bord[desty][destx]:
                    zetten[(desty, destx)] = []
                if schijf.dam:
                    while (self.is_op_bord(desty, destx) and not self.bord[desty][destx]):
                        zetten[(desty, destx)] = []
                        desty, destx = desty+dy, destx+dx

        return zetten

    def slaande_zetten(self, schijf, geslagen=[], bord=None, useddy=None, useddx=None):
        if bord == None:
            bord = self.bord
        rij = schijf.rij
        kolom = schijf.kolom
        zetten = {}
        # Voor elke richting:
        for dy in [1, -1]:
            for dx in [1, -1]:
                if True:
                #if -dy != useddy and -dx != useddx:
                    # hity en hitx zijn de coordinaten van het eventueel geslagen stuk
                    hity, hitx = rij+dy, kolom+dx
                    while (self.is_op_bord(hity, hitx)):
                        hit = bord[hity][hitx]
                        # Check of de hitschijf van de tegenstander is en niet al geslagen is
                        if hit != 0 and hit.kleur != schijf.kleur and (hity, hitx) not in geslagen:
                            # desty en destx zijn de coordinaten van de slaande schijf na zijn zet
                            desty, destx = hity+dy, hitx+dx
                            # Als de coordinaten (desty, destx) nog vrij zijn op het bord:
                            while(self.is_op_bord(desty, destx) and not bord[desty][destx]):
                                # Voeg de zet toe
                                zetten[(desty, destx)] = geslagen+[(hity, hitx)]
                                # Maak een kopie van het bord en doe de zet
                                tempbord = deepcopy(bord)
                                tempbord = self.zet(tempbord[rij][kolom], desty, destx, tempbord)
                                tempbord[hity][hitx] = 0
                                # Als er nog slaande zetten zijn nadat de zet is gedaan, voeg die dan ook toe (later worden de zetten die de minste stukken slaan eruit gefilterd)
                                zetten.update(self.slaande_zetten(tempbord[desty][destx], geslagen+[(hity, hitx)], tempbord, dy, dx))
                                # Als de schijf een dam is, herhaal de stappen dan op het volgende coordinaat
                                if not schijf.dam:
                                    break
                                desty, destx = desty+dy, destx+dx
                        # Als de schijf een dam is, herhaal de stappen dan op het volgende coordinaat
                        if not schijf.dam:
                            break
                        hity, hitx = hity+dy, hitx+dx
        return zetten

    def verwijder(self, schijf):
        if schijf != 0:
            self.bord[schijf.rij][schijf.kolom] = 0
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
