import pygame

kroon = pygame.transform.scale(pygame.image.load('dammen/plaatje/kroon.png'), (40, 30))
zwart_winnaar = pygame.transform.scale(pygame.image.load('dammen/plaatje/zwartwin.png'), (214, 172))
wit_winnaar = pygame.transform.scale(pygame.image.load('dammen/plaatje/witwint.png'), (217, 174))

framerate = 10
kolommen = 10
rijen = 10
breedte = 800
hoogte = 800
blokgrootte = breedte // kolommen

grijs = (80,80,80)
wit = (255,255,255)
zwart = (0,0,0)
lichtgrijs = (180,180,180)
