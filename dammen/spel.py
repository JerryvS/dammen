import pygame
from .constanten import zwart, wit, lichtgrijs, blokgrootte, breedte, hoogte, zwart_winnaar, wit_winnaar
from .bord import Bord

class Spel:
    def __init__(self, scherm):
        self._start()
        self.scherm = scherm

    def _start(self):
        self.gekozen = None
        self.bord = Bord()
        self.beurt = wit
        self.mogelijke_zetten = {}
    
    def update(self):
        self.bord.bord_schijven(self.scherm)
        self.teken_mogelijke_zetten(self.mogelijke_zetten)
        if self.bord.winnaar() == zwart:
            self.scherm.blit(zwart_winnaar, (breedte // 2 - zwart_winnaar.get_width() // 2, hoogte // 2 - zwart_winnaar.get_height() // 2))
        elif self.bord.winnaar() == wit:
            self.scherm.blit(wit_winnaar , (breedte // 2 - wit_winnaar.get_width() // 2, hoogte // 2 - wit_winnaar.get_height() // 2))
        pygame.display.update()

    def reset(self):
        self._start()

    def beurtverandering(self):
        self.mogelijke_zetten = {}
        if self.beurt == wit:
            self.beurt = zwart
        else:
            self.beurt = wit
    
    def kiezen(self, rij, kolom):
        if self.gekozen:
            resultaat = self._zet(rij, kolom)
            if not resultaat:
                self.gekozen = None
                self.mogelijke_zetten = {}
                self.kiezen(rij, kolom)
        
        schijf = self.bord.bord[rij][kolom]
        if schijf != 0 and schijf.kleur == self.beurt:
            self.gekozen = schijf
            self.mogelijke_zetten = self.bord.geef_mogelijke_zetten(schijf)
            return True
        return False

    def _zet(self, rij, kolom):
        if self.gekozen and not self.bord.bord[rij][kolom] and (rij, kolom) in self.mogelijke_zetten:
            self.bord.zet(self.gekozen, rij, kolom)
            overgeslagen = self.mogelijke_zetten[(rij, kolom)]
            for coords in overgeslagen:
                self.bord.verwijder(self.bord.bord[coords[0]][coords[1]])
            if not overgeslagen or self.bord.slaande_zetten(self.bord.bord[rij][kolom]) == {}:
                self.beurtverandering()
        else:
            return False
        return True
    
    def teken_mogelijke_zetten(self, zetten):
        for zet in zetten:
            rij, kolom = zet
            pygame.draw.circle(self.scherm, lichtgrijs, (kolom * blokgrootte + blokgrootte//2, rij * blokgrootte + blokgrootte//2), 15)

