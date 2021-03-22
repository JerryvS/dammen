import pygame
from dammen.constanten import breedte, hoogte, framerate, blokgrootte, wit
from dammen.bord import Bord
from dammen.spel import Spel

scherm = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption('Dammen')

def main():
    run = True
    klok = pygame.time.Clock()
    bord = Bord()
    spel = Spel(scherm)
    
    while run:
        klok.tick(framerate)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                positie = pygame.mouse.get_pos()
                rij, kolom = muispositie(positie)
                spel.kiezen(rij, kolom)   


        spel.update()

    pygame.quit()

def muispositie(positie):
    x, y = positie
    kolom = x // blokgrootte
    rij = y // blokgrootte
    return rij, kolom

main()