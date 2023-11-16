import pygame, os, sys
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
key_active = False

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
title = Textbox(screen, "title", (550, 50), title_text, 'center', (width/2, 105))

options_text = pygame.font.SysFont('Verdana', 20)
options_volume = Textbox(screen, "Options Volume", (475, 30), options_text, 'center', (width* 1/3, height/2))

options_volume_count = Textbox(screen, "Options Volume Count", (200, 30), options_text, 'center', (width* 2/3, height/2))
options_volume_count.rect.left = options_volume.rect.right + 50
options_volume_count.change_text('Input Volume Here', 'black')

options_volume_slider = Textbox(screen, "Options Volume Slider", (130, 26), options_text, 'center', (0, 0), 'slider_bar.png')
options_volume_slider.change_text('', "black")
options_volume_slider.rect.left = options_volume.rect.right + 50
options_volume_slider.rect.centery = options_volume.rect.centery

level_text = pygame.font.SysFont('Verdana', 30, True)
level = Textbox(screen, "level", (100, 20), level_text, 'center', (width/2, height-30))

deaths_text = pygame.font.SysFont('Sans-serif', 30)
deaths = Textbox(screen, "deaths", (100, 20), deaths_text, 'center', (width* 18.5/20, height-30))
deaths.rect.update(deaths.rect.width-100, deaths.rect.top, deaths.rect.width, deaths.rect.height)

textbox_objs = [title, options_volume, options_volume_slider, options_volume_count, level, deaths]

# Button objects
play_text = pygame.font.SysFont('Verdana', 25, True)
play = Button(screen, "Play", 'button.png', (125, 40), play_text, (width/2, height * 1/3))

options_text = pygame.font.SysFont('Verdana', 25, True)
options = Button(screen, "Options", 'button.png', (150, 40), options_text, (width/2, height * 1/2))

options_volume_button = Button(screen, "Options Volume Button", 'slider_button.png', (30, 26), options_text, (0, 0))
options_volume_button.change_text('', "black")
options_volume_button.rect.centery = options_volume_slider.rect.centery
options_volume_button.rect.centerx = options_volume_slider.rect.left + pygame.mixer.music.get_volume()*options_volume_slider.rect.width

volume_icon = Button(screen, 'volume icon', 'volume_icon_button.png', (40, 40), options_text, (30, height-30))
volume_icon.change_text('', "black")

hard_mode_text = pygame.font.SysFont('Verdana', 20, True)
hard_mode = Button(screen, "Hard Mode", 'greyscaled_button.png', (150, 40), hard_mode_text, (width/2, height * 2/3))

exit_text = pygame.font.SysFont('Verdana', 0)
exit = Button(screen, 'exit', 'exit.png', (25, 25), exit_text, (25, 25))
exit.change_text_color('empty')

button_objs = [play, options, options_volume_button, volume_icon, hard_mode, exit]

# Foreground Objects
grass = ForegroundObj(screen, 'grass', 'grass.png', 1, (width/2, height-25), (width, 75))

platform = ForegroundObj(screen, 'platform', 'platform.png', 2, (-10000, -10000))
key_platform = ForegroundObj(screen, 'key_platform', 'platform.png', 2, (-10000, -10000))
chest_platform = ForegroundObj(screen, 'chest_platform', 'platform.png', 2, (width/2, height/5))
enemy_platform = ForegroundObj(screen, 'enemy_platform', 'platform.png', 2, (100, height/2))

wall = ForegroundObj(screen, "wall", 'wall.png', 2, (-1000, -1000))

roof = ForegroundObj(screen, "roof", 'roof.png', 2, (-1000, -1000))

foreground_objs = [grass, platform, key_platform, chest_platform, enemy_platform, wall, roof]

# Interactive Objects
spikes = InteractiveObj(screen, "spikes", 'spikes.png', 1, (enemy_platform.rect.centerx, height/1.25), (200, 40))
spikes_4 = InteractiveObj(screen, "4_spikes", '4_spikes.png', 1, (0, 0), (120, 40))
spikes_3 = InteractiveObj(screen, "3_spikes", '3_spikes.png', 1, (0, 0), (120, 40))
spikes.rect.bottom = grass.rect.top

chest = InteractiveObj(screen, "chest", 'chest.png', 1, (0, 0), (56.25, 43.75))
golden_chest = InteractiveObj(screen, "golden_chest", 'golden_chest.png', 1, (0, 0), (56.25, 43.75))

fire = InteractiveObj(screen, "fire", 'fire.png', 1, (0, 0), (45, 45), 2)

key = InteractiveObj(screen, "key", 'key.gif', 1, (-1000, -1000))

health = InteractiveObj(screen, "health", 'health.png', 1, (0, 0))

flag = InteractiveObj(screen, "flag", 'flag.png', 0.5, (0, 0))

arrow = InteractiveObj(screen, "arrow", 'arrow.png', 0.5, (0, 0))

light = InteractiveObj(screen, "light", 'light.png', 2, (0, 0))

interactive_objs = [spikes, spikes_4, spikes_3, chest, golden_chest, fire, key, health, flag, arrow, light]

on_screen_objects: list[Obj]
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

ENEMY2MOVE = pygame.USEREVENT + 6
ENEMY2MOVESPEED = 900
ENEMY2JUMP = pygame.USEREVENT + 7
ENEMY2JUMPSPEED = 2000

ENEMY3MOVE = pygame.USEREVENT + 8
ENEMY3MOVESPEED = 1200
ENEMY3JUMP = pygame.USEREVENT + 9
ENEMY3JUMPSPEED = 2250

FIREMOVE = pygame.USEREVENT + 10
FIREMOVESPEED = 1000

SCREENCHANGE = pygame.USEREVENT + 11
black_screen = pygame.transform.scale(pygame.image.load('black.png'), (width, height))
black_screen.set_alpha(255)
screen_change = False
transparency = 0

PAUSE = pygame.USEREVENT + 12
pause = False

BOSSMOVE = pygame.USEREVENT + 13
BOSSMOVESPEED = 3000

LEVELDISAPPEAR = pygame.USEREVENT + 14
new_level = False
level_reset = False
level_transparency = 255

DIZZY = pygame.USEREVENT + 15
DIZZYTIME = 3000

MUSIC = pygame.USEREVENT + 16

moving_sprites = pygame.sprite.Group()
player = Player(grass.rect.centerx, grass.rect.top - 25, grass)
moving_sprites.add(player)

os.chdir('..')
os.chdir('audio')
songs = ['bgm1.wav', 'bgm2.wav', 'bgm3.wav', 'bgm4.wav', 'bgm5.wav', 'bgm6.wav']

click_sound = pygame.mixer.Sound('click.wav')
click_sound.set_volume(0.1)

error_sound = pygame.mixer.Sound('error.wav')
error_sound.set_volume(0.1)

jump_sound = pygame.mixer.Sound('jump.wav')
jump_sound.set_volume(0.5)

death_sound = pygame.mixer.Sound('death.wav')
death_sound.set_volume(0.5)

treasure_sound = pygame.mixer.Sound('treasure.wav')

flag_sound = pygame.mixer.Sound('flag.wav')
flag_sound.set_volume(pygame.mixer.music.get_volume()+0.2)

health_sound = pygame.mixer.Sound('health.wav')
health_sound.set_volume(pygame.mixer.music.get_volume()+0.2)

burn_sound = pygame.mixer.Sound('burn.wav')
os.chdir('..')
os.chdir('images')

stars = Stars(0, 0)

game = Game(screen, grass, on_screen_objects, player, moving_sprites, 
            background_objs, foreground_objs, interactive_objs, textbox_objs, button_objs, songs)

game.level = 9
game.next_level()

#game.main()

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
        if event.type == ENEMY1MOVE and len(game.enemies) >= 1:
            if game.enemies[0].moving_right:
                game.enemies[0].stop_right()
                game.enemies[0].move_left()
            elif game.enemies[0].moving_left:
                game.enemies[0].stop_left()
                game.enemies[0].move_right()
            else:
                game.enemies[0].move_left()
        elif event.type == ENEMY1JUMP and len(game.enemies) >= 1:
            game.enemies[0].jump()
        elif event.type == ENEMY2MOVE and len(game.enemies) >= 2:
            if game.enemies[1].moving_right:
                game.enemies[1].stop_right()
                game.enemies[1].move_left()
            elif game.enemies[1].moving_left:
                game.enemies[1].stop_left()
                game.enemies[1].move_right()
            else:
                game.enemies[1].move_left()
        elif event.type == ENEMY2JUMP and len(game.enemies) >= 2:
            game.enemies[1].jump()
        elif event.type == ENEMY3MOVE and len(game.enemies) >= 3:
            if game.enemies[2].moving_right:
                game.enemies[2].stop_right()
                game.enemies[2].move_left()
            elif game.enemies[2].moving_left:
                game.enemies[2].stop_left()
                game.enemies[2].move_right()
            else:
                game.enemies[2].move_left()
        elif event.type == ENEMY3JUMP and len(game.enemies) >= 3:
            game.enemies[2].jump()
        elif event.type == FIREMOVE and game.level >= 6:
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
            if game.level == 11:
                if game.boss.moving_left:
                    game.boss.stop_left()
                    game.boss.move_right()
                    game.boss.jump()
                elif game.boss.moving_right:
                    game.boss.stop_right()
                    game.boss.move_left()
                    game.boss.jump()
                else:
                    game.boss.jump()
        if event.type == DIZZY:
            moving_sprites.remove(stars)
            ev.append(pygame.event.Event(BOSSMOVE))
            pygame.time.set_timer(BOSSMOVE, BOSSMOVESPEED)
        elif event.type == LEVELDISAPPEAR:
            level_reset = True
            new_level = True
        elif event.type == MUSIC:
            game.jukebox.next()
        if options_volume_count.active:
            if event.type == pygame.KEYDOWN:
                user_text = options_volume_count.current_txt
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                    options_volume_count.change_text(user_text, "black")
                elif event.key == pygame.K_RETURN:
                    options_volume_count.deactivate()
                    try:
                        pygame.mixer.music.set_volume(float(options_volume_count.current_txt))
                    except:
                        options_volume_count.deactivate()
                        options_volume_count.change_text(options_volume_count.current_txt, "red")
                    else:
                        jump_sound.set_volume(pygame.mixer.music.get_volume()+0.3)
                        death_sound.set_volume(pygame.mixer.music.get_volume()+0.4)
                        treasure_sound.set_volume(pygame.mixer.music.get_volume()+0.4)
                        health_sound.set_volume(pygame.mixer.music.get_volume()+0.4)
                        flag_sound.set_volume(pygame.mixer.music.get_volume()+0.5)
                        burn_sound.set_volume(pygame.mixer.music.get_volume()+1)
                        user_text = 'Input Volume Here'
                        options_volume_count.deactivate()
                        options_volume_count.change_text(user_text, "black")
                else:
                    user_text += event.unicode
                    options_volume_count.change_text(user_text, "black")
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.move_down()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.stop_right()
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.stop_left()
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.stop_down()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse.get_pressed()[0]:
                if game.level == 0:
                    if play.checkMouse(mouse):
                        click_sound.play()
                        game.next_level()
                        game.jukebox.play()
                        #play.hide()
                    elif options.checkMouse(mouse):
                        click_sound.play()
                        game.options()
                    elif hard_mode.checkMouse(mouse):
                        if game.hard:
                            click_sound.play()
                            game.hard_mode()
                        else:
                            error_sound.play()
                elif exit.checkMouse(mouse):
                    if game.level == -1:
                        game.main('options')
                    else:
                        game.main()
                elif game.level < 0:
                    if searchFor(on_screen_objects, 'Back').checkMouse(mouse):
                        click_sound.play()
                        game.main('options')
                elif game.level > 0:
                    if volume_icon.checkMouse(mouse):
                        click_sound.play()
                        for obj in on_screen_objects:
                            if obj.name == 'Music Frame' and not obj.moving:
                                if obj.visible:
                                    obj.dragToHide((obj.rect.centerx - 50, obj.rect.centery))
                                else:
                                    obj.show()
                                    if pygame.mixer.music.get_busy():
                                        searchFor(obj.objects, 'play_button').hide()
                                    else:
                                        searchFor(obj.objects, 'pause_button').hide()
                                    obj.dragTo((obj.rect.centerx + 50, obj.rect.centery))
                    else:
                        for obj in on_screen_objects:
                            if obj.name == "Music Frame":
                                volume_play = searchFor(obj.objects, 'play_button')
                                volume_pause = searchFor(obj.objects, 'pause_button')
                                volume_skip = searchFor(obj.objects, 'skip_button')
                                if volume_play.checkMouse(mouse):
                                    game.jukebox.unpause()
                                    volume_play.hide()
                                    volume_pause.show()
                                elif volume_pause.checkMouse(mouse):
                                    game.jukebox.pause()
                                    volume_pause.hide()
                                    volume_play.show()
                                elif volume_skip.checkMouse(mouse):
                                    game.jukebox.next()
                            elif obj.name == "Win Frame":
                                mainmenu_button = searchFor(obj.objects, 'Main Menu')
                                if mainmenu_button.checkMouse(mouse):
                                    click_sound.play()
                                    game.main()


        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

    if play.checkMouse(mouse):
        play.change_text_color("white")
    else:
        play.change_text_color("black")

    if options.checkMouse(mouse):
        options.change_text_color("white")
    else:
        options.change_text_color("black")
    
    if game.level < 0:
        if searchFor(on_screen_objects, 'Back').checkMouse(mouse):
            searchFor(on_screen_objects, 'Back').change_text_color("white")
        else:
            searchFor(on_screen_objects, 'Back').change_text_color("black")
        

    if game.hard:
        if hard_mode.checkMouse(mouse):
            hard_mode.change_text_color("white")
        else:
            hard_mode.change_text_color("black")
    
    if volume_icon.checkMouse(mouse):
        volume_icon.change_img('volume_icon_hovered.png')
    else:
        volume_icon.change_img('volume_icon_button.png')
    
    if game.level == 12:
        win_frame = searchFor(on_screen_objects, 'Win Frame')
        mainmenu_button = searchFor(win_frame.objects, 'Main Menu')
        if mainmenu_button.checkMouse(mouse):
            mainmenu_button.change_text_color("white")
        else:
            mainmenu_button.change_text_color("black")

    if game.level == -1:
        if options_volume_slider.checkMouse(mouse):
            if mouse.get_pressed()[0]:
                ratio = (mouse.get_pos()[0] - options_volume_slider.rect.left)/options_volume_slider.rect.width
                options_volume_button.rect.centerx = mouse.get_pos()[0]
                pygame.mixer.music.set_volume(ratio)
    elif game.level > 0:
        slider = Textbox
        for obj in on_screen_objects:
            if obj.name == "Music Frame":
                for new_obj in obj.get_objects():
                    if new_obj.name == 'Options Volume Slider':
                        slider = new_obj
                    if new_obj.name == 'Options Volume Button':
                        if slider.checkMouse(mouse):
                            if mouse.get_pressed()[0]:
                                ratio = ((mouse.get_pos()[0] - obj.rect.left) - slider.rect.left)/slider.rect.width
                                new_obj.rect.centerx = mouse.get_pos()[0] - obj.rect.left
                                new_obj.place(mouse.get_pos()[0] - obj.rect.left, new_obj.rect.centery)
                                pygame.mixer.music.set_volume(ratio)

    if exit.checkMouse(mouse):
        exit.change_img('exit_hovered.png')
    else:
        exit.change_img('exit.png')

    if player.lives <= 0:
        game.restart()
    if not pause:
        updateBackground(on_screen_objects)
        updateForeground(on_screen_objects)
        updateInteractive(on_screen_objects)
        if game.level == 11:
            if game.boss.rect.bottom < -200:
                game.boss.rect.center = (game.player.rect.centerx, game.boss.rect.centery)
            if game.boss.rect.bottom < 0:
                game.boss.stunned = False
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
            if not game.boss.stunned and game.boss.collide(spikes.name, on_screen_objects):
                game.boss.stunned = True
                pygame.time.set_timer(BOSSMOVE, 0)
                stars.place(game.boss.rect.centerx, game.boss.rect.top)
                moving_sprites.add(stars)
                pygame.time.set_timer(DIZZY, DIZZYTIME, 1)
            if player.collide(light.name, on_screen_objects):
                game.next_level()
                makeLight(on_screen_objects)
            if player.collide(golden_chest.name, on_screen_objects):
                for obj in on_screen_objects:
                    if obj.name == "key_platform" or obj.name == "key" or obj.name == "golden_chest" or obj.name == "platform":
                        obj.hide()
                    elif obj.name == "spikes" and obj.rect.centerx > width/2:
                        obj.hide()
                    elif obj.name == "light":
                        obj.rect.right = width
                        obj.rect.bottom = grass.rect.top
            if player.collide(key.name, on_screen_objects):
                if game.stage == 0:
                    key_platform: ForegroundObj
                    for obj in on_screen_objects:
                        if obj.name == "key_platform":
                            obj.rect.left = 0
                            key_platform = obj
                    for obj in on_screen_objects:
                        if obj.name == "key":
                            obj.rect.centerx = key_platform.rect.centerx
                    game.stage += 1
                elif game.stage == 1:
                    key_platform: ForegroundObj
                    for obj in on_screen_objects:
                        if obj.name == "key_platform":
                            obj.rect.centerx = width/2
                            key_platform = obj
                        elif obj.name == "key":
                            obj.hide()
                    for obj in on_screen_objects:
                        if obj.name == "golden_chest":
                            obj.rect.centerx = key_platform.rect.centerx
                            obj.rect.bottom = key_platform.rect.top
                    game.stage += 1
        moving_sprites.draw(screen)
        moving_sprites.update()
        updatePlayer(player, on_screen_objects, screen)
        updateGUI(on_screen_objects)
        updateLives(player, on_screen_objects)
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

    if player.collide(spikes.name, on_screen_objects) or player.hit(game.enemies) or player.rect.top > height or player.collide(spikes_4.name, on_screen_objects) or player.collide(spikes_3.name, on_screen_objects):
        if not player.recovering:
            death_sound.play()
        player.death()
        for obj in on_screen_objects:
            if obj.name == "deaths":
                obj.change_text(f'Deaths: {player.deaths}', 'white')
    if player.collide(fire.name, on_screen_objects):
        if not player.recovering:
            burn_sound.play()
        player.death()
        for obj in on_screen_objects:
            if obj.name == "deaths":
                obj.change_text(f'Deaths: {player.deaths}', 'white')
    if player.collide(health.name, on_screen_objects):
        health_sound.play()
        for obj in on_screen_objects:
            if type(obj) == InteractiveObj and obj.name == "health" and player.rect.colliderect(obj.rect):
                obj.hide()
        player.life_up()
    if player.collide(chest.name, on_screen_objects):
        treasure_sound.play()
        player.restart(None, on_screen_objects)
        game.next_level()
        level_reset = False
        level_transparency = 255
        level.text.get_surface().set_alpha(level_transparency)
    if player.collide(flag.name, on_screen_objects):
        flag_sound.play()
        player.new_checkpoint(game.level)
        flag.hide()
    if player.collide(key.name, on_screen_objects):
        for obj in on_screen_objects:
            if obj.name == "key" and game.level != 11:
                os.chdir('..')
                os.chdir('audio')
                pygame.mixer.music.stop()
                pygame.mixer.music.load('bossmusic.wav')
                pygame.mixer.music.play(-1)
                os.chdir('..')
                os.chdir('images')
                obj.hide()
                screen_change = True
                pygame.time.set_timer(SCREENCHANGE, 50)

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