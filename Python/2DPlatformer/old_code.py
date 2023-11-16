import pygame, os
import pygame.display as display

from functions import *

os.chdir('images')

pygame.init()

size = 1000, 600

screen = display.set_mode(size)
width, height = screen.get_width(), screen.get_height()
bg = pygame.image.load("background.png")
bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
center = screen.get_width()/2, screen.get_height()/2
clock = pygame.time.Clock()
gravityvel = 10
gravityaccel = 1

# Background Objects
sky = BackgroundObj(screen, "sky", 'sky.jpg', 1, (width/2, height/2), (width, height)) # Background sky
sun = BackgroundObj(screen, "sun", 'sun.png', 1, (15, 15)) # Sun
cloud1 = BackgroundObj(screen, "cloud1", 'cloud1.png', 0.4, (125, 150), None, 1) # Normal cloud 
cloud2 = BackgroundObj(screen, "cloud2", 'cloud2.png', 0.4, (250, 50), None, 1) # Semi-Big cloud 
cloud3 = BackgroundObj(screen, "cloud3", 'cloud3.png', 0.4, (500, 50), None, 1) # Long cloud
cloud4 = BackgroundObj(screen, "cloud4", 'cloud4.png', 0.4, (375, 150), None, 1) # Short cloud
cloud5 = BackgroundObj(screen, "cloud5", 'cloud1.png', 0.4, (625, 150), None, 1) # Normal cloud 

clouds = [cloud1, cloud2, cloud3, cloud4, cloud5]

heart_box = BackgroundObj(screen, "box", 'blank.png', 1, (width/2, 50), (100, 75))
heart_box.rect.top = 0
heart_box.rect.right = width - 20
heart1 = BackgroundObj(screen, "heart1", 'heart.png', 1, (heart_box.rect.left + 15, heart_box.rect.centery), (35, 35))
heart2 = BackgroundObj(screen, "heart2", 'heart.png', 1, (heart_box.rect.centerx, heart_box.rect.centery), (35, 35))
heart3 = BackgroundObj(screen, "heart3", 'heart.png', 1, (heart_box.rect.right - 15, heart_box.rect.centery), (35, 35))

background_objs = [sky, sun, cloud1, cloud2, cloud3, cloud4, cloud5, heart1, heart2, heart3]

# Textbox objects
title_text = pygame.font.SysFont('Verdana', 60, True)
title = Textbox(screen, "title", (300, 50), title_text, 'center', (width/2, 105))

level_text = pygame.font.SysFont('Verdana', 30, True)
level = Textbox(screen, "level", (100, 20), level_text, 'center', (width/2, height-30))

textbox_objs = [title, level]

# Button objects
play_text = pygame.font.SysFont('Verdana', 30, True)
play = Button(screen, "Play", 'button.png', (125, 50), play_text, (width/2, height/2))

resume_text = pygame.font.SysFont('Verdana', 30, True)
resume = Button(screen, "Resume", 'button.png', (175, 50), resume_text, (width/2, height/2))

mainmenu_text = pygame.font.SysFont('Verdana', 30, True)
mainmenu = Button(screen, "Main Menu", 'button.png', (225, 50), mainmenu_text, (width/2, height * 2/3))

options_objs = [resume, mainmenu]

button_objs = [play]

# Foreground Objects
grass = ForegroundObj(screen, 'grass', 'grass.png', 1, (width/2, height-25), (width, 75))

platform = ForegroundObj(screen, 'platform', 'platform.png', 2, (-10000, -10000))
chest_platform = ForegroundObj(screen, 'chest_platform', 'platform.png', 2, (width/2, height/5))
enemy_platform = ForegroundObj(screen, 'enemy_platform', 'platform.png', 2, (100, height/2))

wall = ForegroundObj(screen, "wall", 'wall.png', 2, (-1000, -1000))

roof = ForegroundObj(screen, "roof", 'roof.png', 2, (-1000, -1000))

foreground_objs = [grass, platform, chest_platform, enemy_platform, wall, roof]

# Interactive Objects
spikes = InteractiveObj(screen, "spikes", 'spikes.png', 1, (enemy_platform.rect.centerx, height/1.25), (200, 40))
spikes_4 = InteractiveObj(screen, "4_spikes", '4_spikes.png', 1, (0, 0), (120, 40))
spikes_3 = InteractiveObj(screen, "3_spikes", '3_spikes.png', 1, (0, 0), (120, 40))
spikes.rect.bottom = grass.rect.top

chest = InteractiveObj(screen, "chest", 'chest.png', 1, (0, 0), (56.25, 43.75))
chest.rect.bottom = chest_platform.rect.top
chest.rect.centerx = chest_platform.rect.centerx

fire = InteractiveObj(screen, "fire", 'fire.png', 1, (0, 0), (45, 45), 2)

key = InteractiveObj(screen, "key", 'key.gif', 1, (-1000, -1000))

health = InteractiveObj(screen, "health", 'health.png', 1, (0, 0))
health.surface.set_alpha(0)

flag = InteractiveObj(screen, "flag", 'flag.png', 0.5, (0, 0))

arrow = InteractiveObj(screen, "arrow", 'arrow.png', 0.5, (0, 0))

interactive_objs = [spikes, spikes_4, spikes_3, chest, fire, key, health, flag, arrow]

on_screen_objects = [sky, sun, cloud1, cloud2, cloud3, cloud4, cloud5, # Background Objects
                    grass] # Foreground Objects

CLOUDS = pygame.USEREVENT + 1
pygame.time.set_timer(CLOUDS, 800)

DEATH = pygame.USEREVENT + 2
RECOVERY = pygame.USEREVENT + 3

ENEMY1MOVE = pygame.USEREVENT + 4
ENEMY1MOVESPEED = 800
ENEMY1JUMP = pygame.USEREVENT + 5
ENEMY1JUMPSPEED = 2500
enemy1move_static = 0
enemy1jump_static = 0
enemy1move_timesince = 0
enemy1jump_timesince = 0

ENEMY2MOVE = pygame.USEREVENT + 6
ENEMY2MOVESPEED = 1000
ENEMY2JUMP = pygame.USEREVENT + 7
ENEMY2JUMPSPEED = 2000
enemy2move_static = 0
enemy2jump_static = 0
enemy2move_timesince = 0
enemy2jump_timesince = 0

ENEMY3MOVE = pygame.USEREVENT + 8
ENEMY3MOVESPEED = 1200
ENEMY3JUMP = pygame.USEREVENT + 9
ENEMY3JUMPSPEED = 2250
enemy3move_static = 0
enemy3jump_static = 0
enemy3move_timesince = 0
enemy3jump_timesince = 0

FIREMOVE = pygame.USEREVENT + 10
FIREMOVESPEED = 1000
firemove_static = 0
firemove_timesince = 0

SCREENCHANGE = pygame.USEREVENT + 11
black_screen = pygame.transform.scale(pygame.image.load('black.png'), (width, height))
black_screen.set_alpha(255)
screen_change = False
transparency = 0

PAUSE = pygame.USEREVENT + 12
pause = False

BOSSMOVE = pygame.USEREVENT + 13
BOSSMOVESPEED = 2500
bossmove_static = 0
bossmove_timesince = 0

LEVELDISAPPEAR = pygame.USEREVENT + 14
new_level = False
level_reset = False
level_transparency = 255

DIZZY = pygame.USEREVENT + 15
DIZZYTIME = 3000


escape = False
escape_screen = pygame.transform.scale(pygame.image.load('black.png'), (width, height))
escape_screen.set_alpha(128)
afterenemy1move = False
afterenemy1jump = False
afterenemy2move = False
afterenemy2jump = False
afterenemy3move = False
afterenemy3jump = False
afterfiremove = False
afterbossmove = False
afterbossjump = False

moving_sprites = pygame.sprite.Group()
player = Player(grass.rect.centerx, grass.rect.top - 25, grass)
moving_sprites.add(player)

stars = Stars(0, 0)

game = Game(screen, grass, on_screen_objects, player, moving_sprites, 
            background_objs, foreground_objs, interactive_objs, textbox_objs, button_objs)

game.level = 9
game.next_level()

#game.main()
#pygame.time.set_timer(LEVELDISAPPEAR, 2000, 1)

current_time = 0

while True:

    mouse = pygame.mouse

    ev = pygame.event.get()

    for event in ev:
        if event.type == CLOUDS:
            moveClouds(clouds)
        elif event.type == DEATH:
            player.recovery()
        elif event.type == RECOVERY:
            player.end_recovery()
        if not pause:
            if event.type == ENEMY1MOVE and len(game.enemies) >= 1:
                if afterenemy1move:
                    pygame.time.set_timer(ENEMY1MOVE, 800)
                    afterenemy1move = False
                enemy1move_static = pygame.time.get_ticks()
                if game.enemies[0].moving_right:
                    game.enemies[0].stop_right()
                    game.enemies[0].move_left()
                elif game.enemies[0].moving_left:
                    game.enemies[0].stop_left()
                    game.enemies[0].move_right()
                else:
                    game.enemies[0].move_left()
            elif event.type == ENEMY1JUMP and len(game.enemies) >= 1:
                if afterenemy1jump:
                    pygame.time.set_timer(ENEMY1JUMP, 2500)
                    afterenemy1jump = False
                enemy1jump_static = pygame.time.get_ticks()
                game.enemies[0].jump()
            elif event.type == ENEMY2MOVE and len(game.enemies) >= 2:
                if afterenemy2move:
                    pygame.time.set_timer(ENEMY2MOVE, 1000)
                    afterenemy2move = False
                enemy2move_static = pygame.time.get_ticks()
                if game.enemies[1].moving_right:
                    game.enemies[1].stop_right()
                    game.enemies[1].move_left()
                elif game.enemies[1].moving_left:
                    game.enemies[1].stop_left()
                    game.enemies[1].move_right()
                else:
                    game.enemies[1].move_left()
            elif event.type == ENEMY2JUMP and len(game.enemies) >= 2:
                if afterenemy2jump:
                    pygame.time.set_timer(ENEMY2JUMP, 2000)
                    afterenemy2jump = False
                enemy2jump_static = pygame.time.get_ticks()
                game.enemies[1].jump()
            elif event.type == ENEMY3MOVE and len(game.enemies) >= 3:
                if afterenemy3move:
                    pygame.time.set_timer(ENEMY3MOVE, 1200)
                    afterenemy3move = False
                enemy3move_static = pygame.time.get_ticks()
                if game.enemies[2].moving_right:
                    game.enemies[2].stop_right()
                    game.enemies[2].move_left()
                elif game.enemies[2].moving_left:
                    game.enemies[2].stop_left()
                    game.enemies[2].move_right()
                else:
                    game.enemies[2].move_left()
            elif event.type == ENEMY3JUMP and len(game.enemies) >= 3:
                if afterenemy3jump:
                    pygame.time.set_timer(ENEMY3JUMP, 2250)
                    afterenemy3jump = False
                enemy3jump_static = pygame.time.get_ticks()
                game.enemies[2].jump()
            elif event.type == FIREMOVE and game.level >= 6:
                if afterfiremove:
                    pygame.time.set_timer(FIREMOVE, 1000)
                    afterfiremove = False
                firemove_static = pygame.time.get_ticks()
                for obj in on_screen_objects:
                    if type(obj) == InteractiveObj and obj.name == "fire":
                        if obj.direction == 'up':
                            obj.move('right')
                        elif obj.direction == 'right':
                            obj.move('down')
                        elif obj.direction == 'down':
                            obj.move('left')
                        elif obj.direction == 'left':
                            obj.move('up')
                        else:
                            obj.move('up')
            elif event.type == BOSSMOVE:
                if afterbossmove:
                    pygame.time.set_timer(BOSSMOVE, 3000)
                    afterbossmove = False
                bossmove_static = pygame.time.get_ticks()
                if game.level == 11:
                    print("Change Boss direction!")
                    if game.boss.moving_left:
                        print("Going Right")
                        game.boss.stop_left()
                        game.boss.move_right()
                        game.boss.jump()
                    elif game.boss.moving_right:
                        print("Going Left")
                        game.boss.stop_right()
                        game.boss.move_left()
                        game.boss.jump()
                    else:
                        game.boss.jump()
            elif event.type == DIZZY:
                print("Stun done")
                moving_sprites.remove(stars)
                ev.append(BOSSMOVE)
                pygame.time.set_timer(BOSSMOVE, BOSSMOVESPEED)
        else:
            if event.type == ENEMY1MOVE:
                if afterenemy1move:
                    pygame.time.set_timer(ENEMY1MOVE, ENEMY1MOVESPEED)
                    afterenemy1move = False
                    enemy1move_static = pygame.time.get_ticks()
            elif event.type == ENEMY1JUMP:
                if afterenemy1jump:
                    pygame.time.set_timer(ENEMY1JUMP, ENEMY1JUMPSPEED)
                    afterenemy1jump = False
                    enemy1jump_static = pygame.time.get_ticks()
            elif event.type == ENEMY2MOVE:
                if afterenemy2move:
                    pygame.time.set_timer(ENEMY2MOVE, ENEMY2MOVESPEED)
                    afterenemy2move = False
                    enemy2move_static = pygame.time.get_ticks()
            elif event.type == ENEMY2JUMP:
                if afterenemy2jump:
                    pygame.time.set_timer(ENEMY2JUMP, ENEMY2JUMPSPEED)
                    afterenemy2jump = False
                    enemy2jump_static = pygame.time.get_ticks()
            elif event.type == ENEMY3MOVE:
                if afterenemy3move:
                    pygame.time.set_timer(ENEMY3MOVE, ENEMY3MOVESPEED)
                    afterenemy3move = False
                    enemy3move_static = pygame.time.get_ticks()
            elif event.type == ENEMY3JUMP:
                if afterenemy3jump:
                    pygame.time.set_timer(ENEMY3JUMP, ENEMY3JUMPSPEED)
                    afterenemy3jump = False
                    enemy3jump_static = pygame.time.get_ticks()
            elif event.type == FIREMOVE:
                if afterfiremove:
                    pygame.time.set_timer(FIREMOVE, FIREMOVESPEED)
                    afterfiremove = False
                    firemove_static = pygame.time.get_ticks()
            elif event.type == BOSSMOVE:
                if afterbossmove:
                    pygame.time.set_timer(BOSSMOVE, BOSSMOVESPEED)
                    afterbossmove = False
                    bossmove_static = pygame.time.get_ticks()
        if event.type == LEVELDISAPPEAR:
            level_reset = True
            new_level = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_w or event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.move_down()
            elif event.key == pygame.K_ESCAPE:
                current_time = pygame.time.get_ticks()
                if escape:
                    escape = False
                    pause = False
                    pygame.time.set_timer(ENEMY1MOVE, ENEMY1MOVESPEED - enemy1move_timesince, 1)
                    pygame.time.set_timer(ENEMY1JUMP, ENEMY1JUMPSPEED - enemy1jump_timesince, 1)
                    pygame.time.set_timer(ENEMY2MOVE, ENEMY2MOVESPEED - enemy2move_timesince, 1)
                    pygame.time.set_timer(ENEMY2JUMP, ENEMY2JUMPSPEED - enemy2jump_timesince, 1)
                    pygame.time.set_timer(ENEMY3MOVE, ENEMY3MOVESPEED - enemy3move_timesince, 1)
                    pygame.time.set_timer(ENEMY3JUMP, ENEMY3JUMPSPEED - enemy3jump_timesince, 1)
                    pygame.time.set_timer(FIREMOVE, FIREMOVESPEED - firemove_timesince, 1)
                    pygame.time.set_timer(BOSSMOVE, BOSSMOVESPEED - bossmove_timesince, 1)
                    afterenemy1move = True
                    afterenemy1jump = True
                    afterenemy2move = True
                    afterenemy2jump = True
                    afterenemy3move = True
                    afterenemy3jump = True
                    afterfiremove = True
                    afterbossmove = True
                else:
                    escape = True
                    pause = True
                    screen.blit(escape_screen, (0, 0))
                    print(f'enemy1move time since: {current_time} - {enemy1move_static} = {current_time - enemy1move_static}')
                    print(f'enemy1jump time since: {current_time} - {enemy1jump_static} = {current_time - enemy1jump_static}')
                    print(f'enemy2move time since: {current_time} - {enemy2move_static} = {current_time - enemy2move_static}')
                    print(f'enemy2jump time since: {current_time} - {enemy2jump_static} = {current_time - enemy2jump_static}')
                    print(f'enemy3move time since: {current_time} - {enemy3move_static} = {current_time - enemy3move_static}')
                    print(f'enemy3jump time since: {current_time} - {enemy3jump_static} = {current_time - enemy3jump_static}')
                    if enemy1move_static > 0:
                        enemy1move_timesince = current_time - enemy1move_static
                        if enemy1move_timesince > ENEMY1MOVESPEED:
                            enemy1move_timesince = 0
                    if enemy1jump_static > 0:
                        enemy1jump_timesince = current_time - enemy1jump_static
                        if enemy1jump_timesince > ENEMY1JUMPSPEED:
                            enemy1jump_timesince = 0
                    if enemy2move_static > 0:
                        enemy2move_timesince = current_time - enemy2move_static
                        if enemy2move_timesince > ENEMY2MOVESPEED:
                            enemy2move_timesince = 0
                    if enemy1jump_static > 0:
                        enemy2jump_timesince = current_time - enemy2jump_static
                        if enemy2jump_timesince > ENEMY2JUMPSPEED:
                            enemy2jump_timesince = 0
                    if enemy3move_static > 0:
                        enemy3move_timesince = current_time - enemy3move_static
                        if enemy3move_timesince > ENEMY3MOVESPEED:
                            enemy3move_timesince = 0
                    if enemy3jump_static > 0:
                        enemy3jump_timesince = current_time - enemy3jump_static
                        if enemy3jump_timesince > ENEMY3JUMPSPEED:
                            enemy3jump_timesince = 0
                    if firemove_static > 0:
                        firemove_timesince = current_time - firemove_static
                        if firemove_timesince > FIREMOVESPEED:
                            firemove_timesince = 0
                    if bossmove_static > 0:
                        bossmove_timesince = current_time - bossmove_static
                        if bossmove_timesince > BOSSMOVESPEED:
                            bossmove_timesince = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.stop_right()
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.stop_left()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.stop_down()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play.checkMouse(mouse):
                game.next_level()
                play.hide()
            if escape:
                if resume.checkMouse(mouse):
                    escape = False
                    pause = False
                    pygame.time.set_timer(ENEMY1MOVE, ENEMY1MOVESPEED - enemy1move_timesince, 1)
                    pygame.time.set_timer(ENEMY1JUMP, ENEMY1JUMPSPEED - enemy1jump_timesince, 1)
                    pygame.time.set_timer(ENEMY2MOVE, ENEMY2MOVESPEED - enemy2move_timesince, 1)
                    pygame.time.set_timer(ENEMY2JUMP, ENEMY2JUMPSPEED - enemy2jump_timesince, 1)
                    pygame.time.set_timer(ENEMY3MOVE, ENEMY3MOVESPEED - enemy3move_timesince, 1)
                    pygame.time.set_timer(ENEMY3JUMP, ENEMY3JUMPSPEED - enemy3jump_timesince, 1)
                    pygame.time.set_timer(FIREMOVE, FIREMOVESPEED - firemove_timesince, 1)
                    pygame.time.set_timer(BOSSMOVE, BOSSMOVESPEED - bossmove_timesince, 1)
                    afterenemy1move = True
                    afterenemy1jump = True
                    afterenemy2move = True
                    afterenemy2jump = True
                    afterenemy3move = True
                    afterenemy3jump = True
                    afterfiremove = True
                    afterbossmove = True
                elif mainmenu.checkMouse(mouse):
                    escape = False
                    pause = False
                    game.main()
        if event.type == pygame.QUIT: pygame.quit()
    
    if play.checkMouse(mouse):
        play.change_text_color("white")
    else:
        play.change_text_color("black")

    if resume.checkMouse(mouse):
        resume.change_text_color("white")
    else:
        resume.change_text_color("black")

    if mainmenu.checkMouse(mouse):
        mainmenu.change_text_color("white")
    else:
        mainmenu.change_text_color("black")
    
    if player.lives <= 0:
        game.restart()
    if pause:
        if escape:
            updatePause(options_objs)
    else:
        updateBackground(on_screen_objects)
        updateForeground(on_screen_objects)
        updateInteractive(on_screen_objects)
        if game.level == 11:
            if game.boss.rect.bottom < -200:
                game.boss.rect.center = (game.player.rect.centerx, game.boss.rect.centery)
            if game.boss.rect.bottom < 0:
                for obj in on_screen_objects:
                    if type(obj) == InteractiveObj and obj.name == "arrow":
                        obj.place(game.boss.rect.centerx, 50)
            else:
                for obj in on_screen_objects:
                    if type(obj) == InteractiveObj and obj.name == "arrow":
                        obj.hide()
            for obj in on_screen_objects:
                if type(obj) == ForegroundObj and obj.name == "platform":
                    if obj.rect.left > width:
                        obj.move_left()
                    elif obj.rect.right < 0:
                        obj.move_right()
            if game.boss.collide(spikes.name, on_screen_objects):
                pygame.time.set_timer(BOSSMOVE, 0)
                stars.place(game.boss.rect.centerx, game.boss.rect.top)
                moving_sprites.add(stars)
                pygame.time.set_timer(DIZZY, DIZZYTIME)
        updateLives(player, on_screen_objects)
        updateText(on_screen_objects)
        moving_sprites.draw(screen)
        moving_sprites.update()
        updatePlayer(player, on_screen_objects, screen)
        for curr_enemy in game.enemies:
            if type(curr_enemy) == Boss:
                updateBoss(curr_enemy, on_screen_objects, screen)
            else:
                updateEnemy(curr_enemy, on_screen_objects, screen)
        if level_reset:
            level_transparency -= 5
            level.text.get_surface().set_alpha(level_transparency)
            if level_transparency < 0:
                level_reset = False
                level_transparency = 255

    if player.collide(spikes.name, on_screen_objects) or player.hit(game.enemies) or player.rect.top > height or player.collide(fire.name, on_screen_objects) or player.collide(spikes_4.name, on_screen_objects) or player.collide(spikes_3.name, on_screen_objects):
        player.death()
    if player.collide(health.name, on_screen_objects):
        for obj in on_screen_objects:
            if type(obj) == InteractiveObj and obj.name == "health" and player.rect.colliderect(obj.rect):
                obj.hide()
        player.life_up()
    if player.collide(chest.name, on_screen_objects):
        print("Level Cleared!")
        player.restart(None, on_screen_objects)
        game.next_level()
        level_reset = False
        level_transparency = 255
        level.text.get_surface().set_alpha(level_transparency)
    if player.collide(key.name, on_screen_objects):
        for obj in on_screen_objects:
            if obj.name == "key":
                obj.hide()
        #makeDark(on_screen_objects)
        screen_change = True
        pygame.time.set_timer(SCREENCHANGE, 50)
    if player.collide(flag.name, on_screen_objects):
        player.new_checkpoint(game.level)
        flag.hide()
    for event in ev:
        if event.type == SCREENCHANGE:
            if transparency < 255:
                pause = True
                black_screen.set_alpha(transparency)
                screen.blit(black_screen, (0, 0))
                transparency += 5
            elif transparency >= 255:
                game.next_level()
                level_reset = False
                level_transparency = 255
                level.text.get_surface().set_alpha(level_transparency)
                makeDark(on_screen_objects)
                pygame.time.set_timer(SCREENCHANGE, 0)
                pygame.time.set_timer(PAUSE, 500, 1)
        elif event.type == PAUSE:
            pause = False
    display.flip()
    clock.tick(60)