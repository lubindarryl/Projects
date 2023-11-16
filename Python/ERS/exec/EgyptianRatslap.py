import os, pygame, sys
from functions import *
import pygame.display as display
import random

os.chdir('images')

pygame.init()
pygame.mixer.init()

size = width, height = 800, 600

screen = display.set_mode(size)
display.set_caption("Egyptian Ratslap", "Egytpian Ratslap")
bg = pygame.image.load("woodbg.jpg")
bg = pygame.transform.scale(bg, (800, 600))
color = (100, 200, 100)
empty = (0, 0, 0, 0)

# Instatiating Card Objects for deck
H1 = Card(screen, "H1", "H", 1, "H1.png")
H2 = Card(screen, "H2", "H", 2, "H2.png")
H3 = Card(screen, "H3", "H", 3, "H3.png")
H4 = Card(screen, "H4", "H", 4, "H4.png")
H5 = Card(screen, "H5", "H", 5, "H5.png")
H6 = Card(screen, "H6", "H", 6, "H6.png")
H7 = Card(screen, "H7", "H", 7, "H7.png")
H8 = Card(screen, "H8", "H", 8, "H8.png")
H9 = Card(screen, "H9", "H", 9, "H9.png")
H10 = Card(screen, "H10", "H", 10, "H10.png")
H11 = Card(screen, "H11", "H", 11, "H11.png")
H12 = Card(screen, "H12", "H", 12, "H12.png")
H13 = Card(screen, "H13", "H", 13, "H13.png")

D1 = Card(screen, "D1", "D", 1, "D1.png")
D2 = Card(screen, "D2", "D", 2, "D2.png")
D3 = Card(screen, "D3", "D", 3, "D3.png")
D4 = Card(screen, "D4", "D", 4, "D4.png")
D5 = Card(screen, "D5", "D", 5, "D5.png")
D6 = Card(screen, "D6", "D", 6, "D6.png")
D7 = Card(screen, "D7", "D", 7, "D7.png")
D8 = Card(screen, "D8", "D", 8, "D8.png")
D9 = Card(screen, "D9", "D", 9, "D9.png")
D10 = Card(screen, "D10", "D", 10, "D10.png")
D11 = Card(screen, "D11", "D", 11, "D11.png")
D12 = Card(screen, "D12", "D", 12, "D12.png")
D13 = Card(screen, "D13", "D", 13, "D13.png")

S1 = Card(screen, "S1", "S", 1, "S1.png")
S2 = Card(screen, "S2", "S", 2, "S2.png")
S3 = Card(screen, "S3", "S", 3, "S3.png")
S4 = Card(screen, "S4", "S", 4, "S4.png")
S5 = Card(screen, "S5", "S", 5, "S5.png")
S6 = Card(screen, "S6", "S", 6, "S6.png")
S7 = Card(screen, "S7", "S", 7, "S7.png")
S8 = Card(screen, "S8", "S", 8, "S8.png")
S9 = Card(screen, "S9", "S", 9, "S9.png")
S10 = Card(screen, "S10", "S", 10, "S10.png")
S11 = Card(screen, "S11", "S", 11, "S11.png")
S12 = Card(screen, "S12", "S", 12, "S12.png")
S13 = Card(screen, "S13", "S", 13, "S13.png")

C1 = Card(screen, "C1", "C", 1, "C1.png")
C2 = Card(screen, "C2", "C", 2, "C2.png")
C3 = Card(screen, "C3", "C", 3, "C3.png")
C4 = Card(screen, "C4", "C", 4, "C4.png")
C5 = Card(screen, "C5", "C", 5, "C5.png")
C6 = Card(screen, "C6", "C", 6, "C6.png")
C7 = Card(screen, "C7", "C", 7, "C7.png")
C8 = Card(screen, "C8", "C", 8, "C8.png")
C9 = Card(screen, "C9", "C", 9, "C9.png")
C10 = Card(screen, "C10", "C", 10, "C10.png")
C11 = Card(screen, "C11", "C", 11, "C11.png")
C12 = Card(screen, "C12", "C", 12, "C12.png")
C13 = Card(screen, "C13", "C", 13, "C13.png")

deck = [H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13,
        D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, 
        S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, 
        C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13]

# Start Button
start_text = pygame.font.SysFont('Serif', 35)
start_button = Button(screen, "Start", 'small_banner.png', (125, 50), start_text, (400, 200))

# Play Button
play_text = pygame.font.SysFont('Serif', 20)
play_button = Button(screen, "Play", 'play_button.png', (100, 50), play_text, (150, 500))

# Slap Button
slap_text = pygame.font.SysFont('Serif', 20)
slap_button = Button(screen, "Slap", 'slap_button.png', (100, 50), slap_text, (650, 500))

# Options
options_text = pygame.font.SysFont('Serif', 30)
options_button = Button(screen, "Options", 'small_banner.png', (150, 50), options_text, (400, 300))

options_text = pygame.font.SysFont('Verdana', 20)
options_volume = Textbox(screen, "Options Volume", (475, 30), options_text, 'center', (width* 1/3, height/2))
options_volume.change_text('Background Volume:', "white")

options_volume_slider = Textbox(screen, "Options Volume Slider", (130, 26), options_text, 'center', (0, 0), 'slider_bar.png')
options_volume_slider.change_text('', "black")
options_volume_slider.rect.left = options_volume.rect.right + 50
options_volume_slider.place(options_volume_slider.rect.centerx, options_volume.rect.centery)

options_volume_button = Button(screen, "Options Volume Button", 'gold_button.png', (30, 26), options_text, (0, 0))
options_volume_button.change_text('', "black")
options_volume_button.place(options_volume_slider.rect.left + pygame.mixer.music.get_volume()*options_volume_slider.rect.width, options_volume_slider.rect.centery)

# Instructions Button
instruct_text = pygame.font.SysFont('Serif', 30)
instruct_button = Button(screen, "Instructions", 'small_banner.png', (200, 50), instruct_text, (400, 400))

# Back Button
back_text = pygame.font.SysFont('Serif', 30)
back_button = Button(screen, "Back", 'small_banner.png', (100, 50), back_text, (75, 50))

# Quit Button
quit_text = pygame.font.SysFont('Serif', 30)
quit_button = Button(screen, "Quit", 'small_banner.png', (125, 50), quit_text, (400, 500))

# Exit Button
exit_text = pygame.font.SysFont('Serif', 30)
exit_button = Button(screen, "Exit", 'small_banner.png', (100, 50), exit_text, (700, 50))

# Title Box
title_text = pygame.font.SysFont('Copperplate Gothic', 40)
title_textbox = Textbox(screen, "Title", (600, 100), title_text, 'topcenter', (400, 75), 'banner.png')
title_textbox.change_text("Egyptian Ratslap", "black")

# Win Box
win_text = pygame.font.SysFont('Copperplate Gothic', 40)
win_textbox = Textbox(screen, "Win", (400, 75), win_text, 'center', (400, 50))

os.chdir('..')
os.chdir('sounds')
card_move_sound = pygame.mixer.Sound('cardSlide5.wav')
card_move_sound.set_volume(0.5)
plr_move_sound = pygame.mixer.Sound('cardPlace1.wav')
com1_move_sound = pygame.mixer.Sound('cardPlace2.wav')
com2_move_sound = pygame.mixer.Sound('cardPlace3.wav')
com3_move_sound = pygame.mixer.Sound('cardPlace4.wav')
slap_sound = pygame.mixer.Sound('slap.mp3')
win_sound = pygame.mixer.Sound('cardShove4.wav')
click_sound = pygame.mixer.Sound('knock.mp3')
click_sound.set_volume(0.5)
songs = ['song1.mp3', 'song2.mp3', 'song3.mp3', 'song4.mp3', 'song5.mp3', 'song6.mp3', 'song7.mp3']
os.chdir('..')
os.chdir('images')

plr_hand = Hand(400, 400, "plr") # Bottom
com1_hand = Hand(300, 300, "com1") # Left
com2_hand = Hand(400, 200, "com2") # Top
com3_hand = Hand(500, 300, "com3") # Right

pile = Pile(screen, 400, 300)
burn_pile = Pile(screen, 500, 400)

plr = Player("plr", plr_hand, plr_move_sound)
plr_counter = Counter(screen, "bottom")
com1 = Player("com1", com1_hand, com1_move_sound)
com1_counter = Counter(screen, "left")
com2 = Player("com2", com2_hand, com2_move_sound)
com2_counter = Counter(screen, "top")
com3 = Player("com3", com3_hand, com3_move_sound)
com3_counter = Counter(screen, "right")
plrs = [plr, com1, com2, com3]
counters = [plr_counter, com1_counter, com2_counter, com3_counter]

objects = [start_button, play_button, options_button, options_volume, options_volume_slider, options_volume_button, instruct_button, back_button, slap_button, quit_button, exit_button, title_textbox, win_textbox, plr_counter, com1_counter, com2_counter, com3_counter]

TIMER = pygame.USEREVENT + 1
SLAPTIMER = pygame.USEREVENT + 2
COM1TIMER = pygame.USEREVENT + 3
COM2TIMER = pygame.USEREVENT + 4
COM3TIMER = pygame.USEREVENT + 5

DEAL = pygame.USEREVENT + 6

MUSIC = pygame.USEREVENT + 7

game_time = 1700
com_slap_time = 1500
slap_time = 2500

slap_timer = Timer()
timer = Timer()

stop_timers = False
stop_slap_timers = False

game = Game(timer, plrs, counters, screen, deck, pile, burn_pile, objects, win_sound, songs)

game.menu()
game.jukebox.play()

randomlist = []
deal_direction = "right"

while True:
    objects = [start_button, play_button, options_button, options_volume, options_volume_slider, options_volume_button, instruct_button, back_button, slap_button, quit_button, exit_button, title_textbox, win_textbox, plr_counter, com1_counter, com2_counter, com3_counter]

    ev = pygame.event.get()
    
    for event in ev:
        if event.type == TIMER:
            timer.finish()
        elif event.type == SLAPTIMER:
            slap_timer.finish()
        elif event.type == DEAL:
            card_move_sound.play()
            current_card = deck[randomlist.pop()]
            if deal_direction == "right":
                card_pos = (com3_hand.x, com3_hand.y)
                deal_direction = "down"
                com3_hand.addCard(current_card)
            elif deal_direction == "left":
                card_pos = (com1_hand.x, com1_hand.y)
                deal_direction = "up"
                com1_hand.addCard(current_card)
            elif deal_direction == "up":
                card_pos = (com2_hand.x, com2_hand.y)
                deal_direction = "right"
                com2_hand.addCard(current_card)
            elif deal_direction == "down":
                card_pos = (plr_hand.x, plr_hand.y)
                deal_direction = "left"
                plr_hand.addCard(current_card)
            current_card.dragTo(card_pos, 1)
            print(f'{current_card.name} is going to {card_pos} from {current_card.pos}')
            if not randomlist:
                timer.finish()
        elif event.type == MUSIC:
            game.jukebox.next()

    mouse = pygame.mouse

    if start_button.checkMouse(mouse):
        start_button.change_text_color("gold")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                game.start()
                game.makeTurn(plr)
                randomlist = random.sample(range(0, 52), 52)
                pygame.time.set_timer(DEAL, 100, 52)
    else:
        start_button.change_text_color("black")

    if back_button.checkMouse(mouse):
        back_button.change_text_color("gold")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                game.menu()
    else:
        back_button.change_text_color("black")

    if options_button.checkMouse(mouse):
        options_button.change_text_color("gold")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                game.options()
    else:
        options_button.change_text_color("black")
    
    if options_volume_slider.checkMouse(mouse):
        if mouse.get_pressed()[0]:
            ratio = (mouse.get_pos()[0] - options_volume_slider.rect.left)/options_volume_slider.rect.width
            options_volume_button.place(mouse.get_pos()[0], options_volume_button.rect.centery)
            pygame.mixer.music.set_volume(ratio)

    if instruct_button.checkMouse(mouse):
        instruct_button.change_text_color("gold")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                game.instructions()
    else:
        instruct_button.change_text_color("black")

    if quit_button.checkMouse(mouse):
        quit_button.change_text_color("gold")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
    else:
        quit_button.change_text_color("black")

    if play_button.checkMouse(mouse) and game.current_player == plr and timer.done:
        play_button.change_text_color("white")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.set_timer(TIMER, 0)
                pygame.event.clear(TIMER)
                game.takeTurn()
                timer.start()
                pygame.time.set_timer(TIMER, game_time, 1)
                pygame.time.set_timer(COM1TIMER, com_slap_time, 1)
                pygame.time.set_timer(COM2TIMER, com_slap_time, 1)
                pygame.time.set_timer(COM3TIMER, com_slap_time, 1)
                break
    else:
        play_button.change_text_color("black")
    

    if slap_button.checkMouse(mouse) and len(pile) >= 2 and not plr.out and slap_timer.done:
        slap_button.change_text_color("white")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                slap_sound.play()
                slap_timer.start()
                pygame.time.set_timer(SLAPTIMER, slap_time, 1)
                if pile.checkSlap():
                    print("Player win slap!")
                    stop_timers = True
                    plr.out = False
                    game.win(plr)
                    game.makeTurn(plr)
                    game.win_state = False
                else:
                    print("Player lost slap!")
                    game.burn_card()
                break           
    else:
        slap_button.change_text_color("black")
    
    if exit_button.checkMouse(mouse):
        exit_button.change_text_color("gold")
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                exit_button.place(650, 50)
                game.over()
                pygame.time.set_timer(DEAL, 0)
                break
    else:
        exit_button.change_text_color("black")

    for event in ev:
        if event.type == COM1TIMER and (stop_timers or stop_slap_timers):
            pygame.event.clear(COM1TIMER)
        if event.type == COM1TIMER and game.started and pile.checkSlap('Double'):
            slap_sound.play()
            pygame.event.clear(COM1TIMER)
            game.win(com1)
            game.makeTurn(com1)
            game.win_state = False
            stop_slap_timers = True

    for event in ev:
        if event.type == COM3TIMER and (stop_timers or stop_slap_timers):
            pygame.event.clear(COM2TIMER)
        if event.type == COM2TIMER and game.started and pile.checkSlap('Sandwhich'):
            slap_sound.play()
            pygame.event.clear(COM2TIMER)
            game.win(com2)
            game.makeTurn(com2)
            game.win_state = False
            stop_slap_timers = True

    for event in ev:
        if event.type == COM3TIMER and (stop_timers or stop_slap_timers):
            pygame.event.clear(COM3TIMER)
        if event.type == COM3TIMER and game.started and pile.checkSlap('Super Sandwhich'):
            slap_sound.play()
            pygame.event.clear(COM3TIMER)
            game.win(com3)
            game.makeTurn(com3)
            game.win_state = False
            stop_slap_timers = True

    for event in ev:
        if stop_timers and event.type == TIMER:
            pygame.event.clear(TIMER)
            stop_timers = False
        elif game.started and event.type == TIMER and game.check():
            pygame.time.set_timer(TIMER, 0)
            pygame.event.clear(TIMER)
            game.takeTurn()
            game.updateGame()
            timer.start()
            pygame.time.set_timer(TIMER, game_time, 1)
            pygame.time.set_timer(COM1TIMER, com_slap_time, 1)
            pygame.time.set_timer(COM2TIMER, com_slap_time, 1)
            pygame.time.set_timer(COM3TIMER, com_slap_time, 1)
            stop_slap_timers = False

    for event in ev:
        if event.type == pygame.QUIT: sys.exit()

    if game.started:
        game.updateGame()
    else:
        refresh(screen, bg, game.objects, deck)
    display.flip()