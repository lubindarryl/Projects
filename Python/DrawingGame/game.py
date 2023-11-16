import pygame, os, sys

from functions import *

pygame.init()

os.chdir('images')

screen_size = width, height = 1000, 800

screen = pygame.display.set_mode(screen_size)
bg = pygame.image.load('bg.jpg')
bg = pygame.transform.scale(bg, (1000, 800))

clock = pygame.time.Clock()

PLAY = pygame.USEREVENT
MENU = pygame.USEREVENT + 1
OPTIONS = pygame.USEREVENT + 2
MUSIC = pygame.USEREVENT + 3
DRAW = pygame.USEREVENT + 4
CLEAR = pygame.USEREVENT + 5
INCRSIZE = pygame.USEREVENT + 6
DECSIZE = pygame.USEREVENT + 7
UNDO = pygame.USEREVENT + 8
REDO = pygame.USEREVENT + 9

objects = []

game = Game(screen, bg, objects)

game.menu()

while True:

    ev = pygame.event.get()

    game.checkInput(ev)

    for event in ev:
        if event.type == pygame.QUIT: sys.exit()

    game.update(ev)