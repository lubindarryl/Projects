import pygame
import os
import random

ENEMY1MOVE = pygame.USEREVENT + 4
ENEMY1JUMP = pygame.USEREVENT + 5

ENEMY2MOVE = pygame.USEREVENT + 6
ENEMY2JUMP = pygame.USEREVENT + 7

ENEMY3MOVE = pygame.USEREVENT + 8
ENEMY3JUMP = pygame.USEREVENT + 9

FIREMOVE = pygame.USEREVENT + 10

BOSSMOVE = pygame.USEREVENT + 13

LEVELDISAPPEAR = pygame.USEREVENT + 14

MUSIC = pygame.USEREVENT + 16

pygame.mixer.init()

os.chdir('audio')
pygame.mixer.music.load('mainmenu.wav')

jump_sound = pygame.mixer.Sound('jump.wav')
os.chdir('..')


class Obj:
    """
    Initializes an on abstract screen object
    
    === Attribute ===
    name -> The name of the object
    screen -> The Surface of the game window
    surface -> The Surface of the obj Object
    rect -> The Rect of the obj Object
    pos -> The position of the obj Object on the screen
    visible -> Checks if the obj Object is visible
    place_on -> The surface that this object will be placed on
    """

    name: str
    screen: pygame.Surface
    surface: pygame.Surface
    rect: pygame.Rect
    pos: tuple[int, int]
    visible: bool
    place_on: pygame.Surface | object

    def __init__(self, screen: pygame.Surface, name: str = 'Object') -> None:
        self.name = name
        self.screen = screen
        self.surface = pygame.Surface
        self.rect = pygame.Rect
        self.pos = (0, 0)
        self.visible = True
        self.place_on = screen
    
    def hide(self) -> None:
        self.rect.update(-10000, -10000, self.rect.width, self.rect.height)
        self.visible = False
    
    def show(self) -> None:
        self.rect.center = self.pos
        self.visible = True
    
    def move(self, x: int, y: int) -> None:
        self.rect.move_ip((x, y))
        self.pos = (self.rect.centerx, self.rect.centery)
    
    def place(self, x: int, y: int) -> None:
        self.rect.center = (x, y)
        self.pos = (self.rect.centerx, self.rect.centery)
    
    def place_onto(self, new_surface: pygame.Surface | object) -> None:
        self.place_on = new_surface
    
    def change_img(self, new_img: str, size: tuple[int, int] = None) -> None:
        pass

    def clone(self) -> None:
        pass
    
    def checkMouse(self, mouse: pygame.mouse):
        check_rect = self.rect
        if not (self.place_on == self.screen):
            check_rect = pygame.Rect(self.place_on.rect.left + self.rect.left, self.place_on.rect.top + self.rect.top, self.rect.width, self.rect.height)
        return mouseInBounds(mouse.get_pos(), check_rect)

    def update(self, alpha: int = None) -> None:
        if alpha:
            self.surface.set_alpha(alpha)
        if type(self.place_on) == pygame.Surface:
            self.place_on.blit(self.surface, self.rect)
        else:
            self.place_on.surface.blit(self.surface, self.rect)


class Frame(Obj):
    """
    Initializes a Frame object that stores objects into it and has then place onto it
    
    === Public Attributes ===
    name -> The name of the Frame object
    objects -> The list of objects inside of the Frame
    surface -> The Surface of the Frame
    rect -> The rectangular placement of the Frame on the screen
    color -> The color of the background of the Frame
    moving -> Determines if the object is moving
    moving_* -> Determines which direction the Frame is moving
    speed -> The speed at which this object can move
    move_until -> The position of where the object will end up
    hide_when_stop -> Determines if the Frame should hide when it stops moving
    """

    name: str
    objects: list[Obj]
    surface: pygame.Surface
    rect: pygame.Rect
    color: tuple[int, int, int, int]

    moving: bool
    moving_left: bool
    moving_right: bool
    move_until: tuple[int, int]
    hide_when_stop: bool

    speed: int

    def __init__(self, screen, name: str, size: tuple[int, int], pos: tuple[int, int], img: str = None, alpha: int = None, color: tuple[int, int, int] = None) -> None:
        super().__init__(screen)
        self.name = name
        self.objects = []
        if img:
            self.surface = pygame.image.load(img)
            self.surface = pygame.transform.scale(self.surface, size)
        else:
            self.surface = pygame.image.load('black.png')
            self.surface = pygame.transform.scale(self.surface, size)
            self.surface.set_alpha(0)
        if color:
            self.color = color
            self.surface.fill(color)
            self.surface.set_alpha(alpha)
        if alpha:
            self.surface.set_alpha(alpha)
        self.rect = self.surface.get_rect()
        self.place(pos[0], pos[1])

        self.moving = False
        self.moving_left = False
        self.moving_right = False
        self.move_until = None
        self.hide_when_stop = False

        self.speed = 1
    
    def change_color(self, color: tuple[int, int, int] | tuple[int, int, int, int]) -> None:
        self.surface.fill(color)

    def checkMouse(self, mouse: pygame.mouse) -> bool:
        return mouseInBounds(mouse.get_pos(), self.rect)

    def get_objects(self) -> list[Obj]:
        return self.objects

    def add(self, obj: Obj) -> None:
        self.objects.append(obj)
        obj.place_onto(self)
    
    def addAll(self, objs: list[Obj]) -> None:
        for obj in objs:
            self.add(obj)
    
    def move(self, x: int, y: int) -> None:
        super().move(x, y)

    def dragTo(self, pos: tuple[int, int]) -> None:
        if self.pos[0] < pos[0]:
            self.move_right()
            self.move_until = pos
        elif self.pos[0] > pos[0]:
            self.move_left()
            self.move_until = pos
    
    def dragToHide(self, pos: tuple[int, int]) -> None:
        self.dragTo(pos)
        self.hide_when_stop = True

    def move_left(self) -> None:
        self.moving_left = True
        self.moving_right = False
        self.moving = True
    
    def move_right(self) -> None:
        self.moving_right = True
        self.moving_left = False
        self.moving = True
    
    def stop_moving(self) -> None:
        self.moving_left = False
        self.moving_right = False
        self.moving = False
    
    def place(self, x: int, y: int) -> None:
        super().place(x, y)
    
    def hide(self) -> None:
        super().hide()
        for obj in self.objects:
            obj.hide()
    
    def show(self) -> None:
        super().show()
        for obj in self.objects:
            obj.show()
    
    def update(self) -> None:
        if self.moving_left:
            self.move(-self.speed, 0)
            if self.pos[0] <= self.move_until[0]:
                self.stop_moving()
                self.move_until = None
                if self.hide_when_stop:
                    self.hide_when_stop = False
                    self.hide()
        elif self.moving_right:
            self.move(self.speed, 0)
            if self.pos[0] >= self.move_until[0]:
                self.stop_moving()
                self.move_until = None
                if self.hide_when_stop:
                    self.hide_when_stop = False
                    self.hide()
        self.screen.blit(self.surface, self.rect)
        for obj in self.objects:
            if type(obj) == Textbox:
                obj.fix_text()
                left = self.rect.left + obj.rect.left
                top = self.rect.top + obj.rect.top
                rect = pygame.Rect(left, top, obj.rect.width, obj.rect.height)

                left_rect = self.rect.left + obj.text_rect[0]
                top_rect = self.rect.top + obj.text_rect[1]
                text_rect = pygame.Rect(left_rect, top_rect, obj.rect.width, obj.rect.height)
                if obj.surface:
                    self.screen.blit(obj.surface, rect)
                self.screen.blit(obj.text.get_surface(), text_rect)
            elif type(obj) == Button:
                obj.fix_text()
                left = self.rect.left + obj.rect.left
                top = self.rect.top + obj.rect.top
                rect = pygame.Rect(left, top, obj.rect.width, obj.rect.height)

                left_rect = self.rect.left + obj.text_rect[0]
                top_rect = self.rect.top + obj.text_rect[1]
                text_rect = pygame.Rect(left_rect, top_rect, obj.rect.width, obj.rect.height)
                
                if obj.surface:
                    self.screen.blit(obj.surface, rect)
                self.screen.blit(obj.text.get_surface(), text_rect)
            else:
                left = self.rect.left + obj.rect.left
                top = self.rect.top + obj.rect.top
                rect = pygame.Rect(left, top, obj.rect.width, obj.rect.height)
                self.screen.blit(obj.surface, rect)


class Text:
    """
    This class insitilizes a text box that is used to put text on pygame objects
    === Attributes ===
    txt -> The actual text of the card
    surface -> The Surface of where the txt lies
    """

    txt: pygame.font.Font
    surface: pygame.Surface

    def __init__(self, txt: pygame.font.Font, surf: pygame.Surface) -> None:
        self.txt = txt
        self.surface = surf
    
    def set_txt(self, new: pygame.font.Font) -> None:
        self.txt = new
    
    def get_txt(self) -> pygame.font.Font:
        return self.txt
    
    def set_surface(self, new: pygame.Surface) -> None:
        self.surface = new
    
    def get_surface(self) -> pygame.Surface:
        return self.surface


class Textbox(Obj):
    """
    Initializes a Textbox object that stores text and displays it on a screen
    
    === Attributes ===
    screen -> The Surface of the game window
    name -> The name of the Textbox
    size -> The size of the Textbox
    img -> The iamge value of the image
    surface -> The optional background img of the Textbox
    rect -> The rect of the surface of the Textbox
    current_txt -> Stores the currently displayed text in the Textbox
    text -> The Text of the Textbox
    text_rect -> The Rect of the Text object
    alignment -> Where the text is inside of the box
    pos -> The position of the Textbox
    active -> If the textbox is being filled with text inputs
    """

    screen: pygame.Surface
    name: str
    size: tuple[int, int]
    img: str
    surface: pygame.Surface
    rect: pygame.Rect
    current_txt: str
    text: Text
    text_rect: tuple[int, int]
    alignment: str
    pos: tuple[int, int]
    active: bool
    place_on: pygame.Surface

    def __init__(self, screen: pygame.Surface, name: str, size: tuple[int, int], text: pygame.font.Font, align: str, pos: tuple[int, int], img: str = None) -> None:
        super().__init__(screen)
        self.name = name
        self.size = size
        if img:
            self.img = img
            self.surface = pygame.image.load(img)
            self.surface = pygame.transform.scale(self.surface, self.size)
        else:
            self.img = None
            self.surface = None
        self.current_txt = name
        self.text = Text(text, pygame.transform.scale(text.render(name, True, "white"), self.size))
        self.rect = self.text.get_surface().get_rect()
        self.rect.center = pos
        self.pos = pos
        self.alignment = align
        if align == "top":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top))
        elif align == "topcenter":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/4))
        elif align == "center":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))
        elif align == "bottom":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.bottom))
        self.active = False

    def fix_text(self) -> None:
        if self.alignment == "top":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top))
        elif self.alignment == "topcenter":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/4))
        elif self.alignment == "center":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))
        elif self.alignment == "bottom":
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.bottom))
    
    def clone(self, new_size: tuple[int, int] = None) -> Obj:
        if new_size:
            return Textbox(self.screen, self.name, new_size, self.text.get_txt(), self.alignment, self.pos, self.img)
        else:
            return Textbox(self.screen, self.name, self.size, self.text.get_txt(), self.alignment, self.pos, self.img)

    def checkMouse(self, mouse: pygame.mouse) -> bool:
        check_rect = self.rect
        if not (self.place_on == self.screen):
            check_rect = pygame.Rect(self.place_on.rect.left + self.rect.left, self.place_on.rect.top + self.rect.top, self.rect.width, self.rect.height)
        return mouseInBounds(mouse.get_pos(), check_rect)

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def update(self) -> None:
        self.fix_text()
        if self.surface:
            self.screen.blit(self.surface, self.rect)
        self.screen.blit(self.text.get_surface(), self.text_rect)
    
    def change_text(self, new_text: str, color: str) -> None:
        self.current_txt = new_text
        self.text.set_surface(self.text.get_txt().render(self.current_txt, True, color))


class Button(Obj):
    """
    Initiatlizes a button
    
    === Attributes ===
    screen -> The Surface of the game window
    name -> The name of the Button
    size -> The size of the Button
    img -> The image of the Button
    surface -> The surface of the Button
    rect -> The Rect of the surface of the Button
    text -> The text of the Button
    text_rect -> The Rect of the Text object
    pos -> The position of the Button
    place_on -> The surface that this object will be placed on
    """

    screen: pygame.Surface
    name: str
    size: tuple[int, int]
    img: str
    surface: pygame.Surface
    rect: pygame.Rect
    text: Text
    text_rect: tuple[int, int]
    pos: tuple[int, int]
    place_on: pygame.Surface

    def __init__(self, screen: pygame.Surface, name: str, img: str, size: tuple[int, int], text: pygame.font.Font, pos: tuple[int, int]) -> None:
        super().__init__(screen)
        self.name = name
        self.size = size
        self.img = img
        self.surface = pygame.image.load(img)
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.rect = self.surface.get_rect()
        self.text = Text(text, text.render(name, True, "black"))
        self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))
        self.pos = pos
        self.rect.center = pos

    def fix_text(self) -> None:
        self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))

    def update(self) -> None:
        super().update()
        self.fix_text()
        self.screen.blit(self.text.get_surface(), self.text_rect)

    def clone(self) -> Obj:
        return Button(self.screen, self.name, self.img, self.size, self.text.get_txt(), self.pos)
    
    def change_img(self, new_img: str, size: tuple[int, int] = None) -> None:
        if size:
            self.surface = pygame.transform.scale(pygame.image.load(new_img), size)
        else:
            self.surface = pygame.transform.scale(pygame.image.load(new_img), self.size)

    def change_text(self, new_text: str, color: str) -> None:
        self.text.set_surface(self.text.get_txt().render(new_text, True, color))

    def change_text_color(self, color: str) -> None:
        if color == "empty":
            self.text.set_surface(self.text.get_txt().render('', True, (0, 0, 0, 0)))
        else:
            self.text.set_surface(self.text.get_txt().render(self.name, True, color))


class BackgroundObj(Obj):
    """
    Initializes a background object that projects an image on the background
    
    === Attributes ===
    name -> The name of the object
    screen -> The Surface of the game window
    img -> The image that is pasted onto the Surface
    surface -> The Surface of the obj Object
    scale -> The scale of the img that is pasted onto the Surface
    rect -> The Rect of the obj Object
    pos -> The position of the obj Object on the screen
    size -> An optional attribute that represents the exact size of the object
    visible -> Checks if the obj Object is visible
    speed -> The speed at which this obj moves on the screen
    """

    name: str
    screen: pygame.Surface
    img: str
    surface: pygame.Surface
    scale: int
    rect: pygame.Rect
    pos: tuple[int, int]
    size: tuple[int, int] | None
    visible: bool
    speed: int
    place_on: pygame.Surface

    def __init__(self, screen: pygame.Surface, name: str, img: str, scale: int, pos: tuple[int, int], size: tuple[int, int] = None, speed: int = 0):
        super().__init__(screen, name)
        self.img = img
        self.surface = pygame.image.load(img)
        self.scale = scale
        if size is None:
            self.size = None
            self.surface = pygame.transform.scale(self.surface, (self.surface.get_rect().width*scale, self.surface.get_rect().height*scale))
        else: 
            self.size = size
            self.surface = pygame.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect()
        self.pos = pos
        self.place(pos[0], pos[1])
        self.speed = speed
    
    def change_img(self, new_img: str, new_size: tuple[int, int] = None) -> None:
        self.img = new_img
        self.surface = pygame.image.load(self.img)
        if new_size:
            self.size = new_size
        if self.size is None:
            self.surface = pygame.transform.scale(self.surface, (self.surface.get_rect().width*self.scale, self.surface.get_rect().height*self.scale))
        else: 
            self.surface = pygame.transform.scale(self.surface, self.size)

    def clone(self) -> Obj:
        return BackgroundObj(self.screen, self.name, self.img, self.scale, self.pos, self.size, self.speed)

    def move(self) -> None:
        super().move(self.speed, 0)
    

class ForegroundObj(Obj):
    """
    Initializes a foreground object that projects an image on the screen
    
    === Attributes ===
    name -> The name of the object
    screen -> The Surface of the game window
    img -> The image that is pasted onto the Surface
    surface -> The Surface of the obj Object
    scale -> The scale of the img that is pasted onto the Surface
    rect -> The Rect of the obj Object
    pos -> The position of the obj Object on the screen
    size -> An optional attribute that represents the exact size of the object
    visible -> Checks if the obj Object is visible
    speed -> The speed at which this obj moves on the screen
    moving_* -> Determines if the Foreground object is moving a certain direction
    """

    name: str
    screen: pygame.Surface
    img: str
    surface: pygame.Surface
    scale: int
    rect: pygame.Rect
    pos: tuple[int, int]
    size: tuple[int, int] | None
    visible: bool
    speed: int
    moving_left: bool
    moving_right: bool
    place_on: pygame.Surface

    def __init__(self, screen: pygame.Surface, name: str, img: str, scale: int, pos: tuple[int, int], size: tuple[int, int] = None, speed: int = 0):
        super().__init__(screen, name)
        self.img = img
        self.surface = pygame.image.load(img)
        self.scale = scale
        if size is None:
            self.size = None
            self.surface = pygame.transform.scale(self.surface, (self.surface.get_rect().width*scale, self.surface.get_rect().height*scale))
        else: 
            self.size = size
            self.surface = pygame.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect()
        self.pos = pos
        self.place(pos[0], pos[1])
        self.speed = speed
        self.moving_left = False
        self.moving_right = False
    
    def clone(self) -> Obj:
        return ForegroundObj(self.screen, self.name, self.img, self.scale, self.pos, self.size, self.speed)
    
    def change_img(self, new_img: str, new_size: tuple[int, int] = None) -> None:
        self.img = new_img
        self.surface = pygame.image.load(self.img)
        if new_size:
            self.size = new_size
        if self.size is None:
            self.surface = pygame.transform.scale(self.surface, (self.surface.get_rect().width*self.scale, self.surface.get_rect().height*self.scale))
        else: 
            self.surface = pygame.transform.scale(self.surface, self.size)

    def move_left(self) -> None:
        self.moving_left = True
        self.moving_right = False
    
    def move_right(self) -> None:
        self.moving_right = True
        self.moving_left = False

    def move(self, inverse: False) -> None:
        if inverse:
            super().move(-self.speed, 0)
        else:
            super().move(self.speed, 0)
    
    def update(self, alpha: int = None) -> None:
        if self.moving_left:
            self.move(True)
        elif self.moving_right:
            self.move(False)
        super().update(alpha)


class InteractiveObj(Obj):
    """
    Initializes an Interactive screen object
    
    === Attributes ===
    name -> The name of the object
    screen -> The Surface of the game window
    img -> The image that is pasted onto the Surface
    surface -> The Surface of the obj Object
    scale -> The scale of the img that is pasted onto the Surface
    rect -> The Rect of the obj Object
    pos -> The position of the obj Object on the screen
    size -> An optional attribute that represents the exact size of the object
    visible -> Checks if the obj Object is visible
    speed -> The speed at which this obj moves on the screen
    moving_* -> Determines if the object is moving in a certain direction
    direction -> The direction in which the object is moving
    """

    name: str
    screen: pygame.Surface
    img: str
    surface: pygame.Surface
    scale: int
    rect: pygame.Rect
    pos: tuple[int, int]
    size: tuple[int, int]
    visible: bool
    speed: int
    moving_up: bool
    moving_right: bool
    moving_left: bool
    moving_down: bool
    direction: str
    place_on: pygame.Surface

    def __init__(self, screen: pygame.Surface, name: str, img: str, scale: int, pos: tuple[int, int], size: tuple[int, int] = None, speed: int = 0):
        super().__init__(screen, name)
        self.img = img
        self.surface = pygame.image.load(img)
        self.scale = scale
        if size is None:
            self.size = None
            self.surface = pygame.transform.scale(self.surface, (self.surface.get_rect().width*scale, self.surface.get_rect().height*scale))
        else: 
            self.size = size
            self.surface = pygame.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect()
        self.pos = pos
        self.place(pos[0], pos[1])
        self.speed = speed
        self.direction = None
    
    def clone(self) -> Obj:
        return InteractiveObj(self.screen, self.name, self.img, self.scale, self.pos, self.size, self.speed)
    
    def move(self, type: str = None) -> None:
        if type == 'right':
            self.direction = 'right'
        elif type == 'left':
            self.direction = 'left'
        elif type == 'up':
            self.direction = 'up'
        elif type == 'down':
            self.direction = 'down'
        else:
            super().move(self.speed, 0)
    
    def change_img(self, new_img: str, surface: pygame.Surface = None) -> None:
        if surface:
            self.surface = surface
        else:
            self.surface = pygame.transform.scale(pygame.image.load(new_img), self.size)

    def update(self, alpha: int = None) -> None:
        if self.direction == 'right':
            super().move(self.speed, 0)
        elif self.direction == 'left':
            super().move(-self.speed, 0)
        elif self.direction == 'up':
            super().move(0, -self.speed)
        elif self.direction == 'down':
            super().move(0, self.speed)
        super().update()


class Stars(pygame.sprite.Sprite):
    """
    Initializes a dizzy stars sprite
    
    === Attributes ===
    sprites -> A collection of different frames for the dizzy stars sprite
    current_sprite -> The index of the current sprite frame
    image -> The image of the sprite
    rect -> The area of the screen where the sprite is located
    """

    sprites: list[pygame.Surface]
    image: pygame.Surface
    current_sprite: float
    rect: pygame.Rect

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars1.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars2.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars3.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars4.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars5.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars6.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars7.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars8.png'), (128, 64)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('stars9.png'), (128, 64)))
        self.current_sprite = 0
        
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def place(self, x: int, y: int) -> None:
        self.rect.center = (x, y)

    def update(self) -> None:
        self.current_sprite += 0.2
        if self.current_sprite > len(self.sprites)-1:
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]


class Enemy(pygame.sprite.Sprite):
    """
    Initializes a Player object that uses sprites to differentiate between idle and moving stages

    === Attributes ===
    sprites -> A list of sprite images for the Player
    current_sprite -> The current sprite displayed on the player at a given time
    rect -> The physical object of the Player
    alive -> Determines if the Player is alive
    recovering -> Determines if the Player is recovering
    is_animating -> Determines if the Sprite is animating
    is_jumping -> Determines of the Sprite is jumping
    moving_* -> Determines if the Sprite is moving in a certain direction
    fast_fall -> Dertermines if the Player is in fast fall
    grounded -> Determines if the Sprite is on the ground
    *accel -> The acceleration of the Player in a certain direction
    init_*vel -> The initial velocity of the player in a certain direction
    *vel -> The velocity of the Player in a certain direction
    maxspeed -> The maximum speed that the Player can travel moving left and right
    floor -> The floor underneath the Player
    """

    sprites: list[pygame.Surface]
    current_sprite: int
    rect: pygame.Rect

    alive: bool

    is_animating: bool
    moving_right: bool
    moving_left: bool
    moving_up: bool

    grounded: bool
    airbourne: bool
    air_resistance: int
    jumps: int

    accel: float
    init_vel: float
    vel: float
    maxspeed: float

    jumpaccel: float
    init_jumpvel: float
    jumpvel: float

    gravityaccel: float
    init_gravityvel: float
    gravityvel: float

    floor: ForegroundObj

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load('enemy_idle.png'), (40, 40))) # Index 0
        self.sprites.append(pygame.transform.scale(pygame.image.load('enemy_jump1.png'), (55, 40))) # Index 1
        self.sprites.append(pygame.transform.scale(pygame.image.load('enemy_jump2.png'), (55, 40))) # Index 2
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.alive = True
        self.recovering = False

        self.is_animating = False
        self.is_jumping = False
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.fast_fall = False
        self.grounded = False

        self.airbourne = False
        self.air_resistance = 1
        self.jumps = 1

        self.accel = 0.2
        self.init_vel = 3
        self.vel = self.init_vel
        self.maxspeed = 3

        self.jumpaccel = 2.0
        self.init_jumpvel = 25.0
        self.jumpvel = self.init_jumpvel

        self.fallaccel = 2
        self.init_fallvel = 2
        self.fallvel = self.init_fallvel

        self.gravityaccel = 0.25
        self.init_gravityvel = 3
        self.gravityvel = self.init_gravityvel

        self.floor = None
    
    def move_right(self) -> None:
        self.moving_right = True
    
    def move_left(self) -> None:
        self.moving_left = True

    def jump(self) -> None:
        if self.jumps > 0:
            self.is_animating = True
            self.current_sprite = 1
            self.moving_up = False
            self.jumpvel = self.init_jumpvel

    def in_air(self) -> None:
        self.airbourne = True
        self.grounded = False

    def ground(self) -> None:
        self.fallvel = self.init_fallvel
        self.grounded = True
        self.airbourne = False
        self.jumps = 2
    
    def stop_left(self) -> None:
        self.moving_left = False
        self.vel = self.init_vel
    
    def stop_right(self) -> None:
        self.moving_right = False
        self.vel = self.init_vel
    
    def make_ground(self, ground: ForegroundObj) -> None:
        self.floor = ground
    
    def change_speed(self, new_speed: float, max: float) -> None:
        self.init_vel = new_speed
        self.maxspeed = max
    
    def kill(self) -> None:
        super().kill()
        self.alive = False

    def collide(self, name: str, objects: list[Obj]) -> bool:
        for object in objects:
            if object.name == name and self.rect.colliderect(object.rect):
                return True
        return False

    def update(self) -> None:
        if self.is_animating: # Jumping Animation
            self.current_sprite += 0.3
            if self.current_sprite >= len(self.sprites):
                self.airbourne = True
                self.jumps -= 1
                self.gravityvel = self.init_gravityvel
                self.current_sprite = 0
                self.is_animating = False
                self.moving_up = True

        if self.moving_up: # Jumping
            self.rect.move_ip(0, -self.jumpvel)
            self.grounded = False
            self.jumpvel -= self.jumpaccel
            if self.jumpvel <= self.init_jumpvel/2:
                self.is_jumping = False
            if self.jumpvel <= 0:
                self.moving_up = False
                self.jumpvel = 20
        else: # Falling
            if self.airbourne:
                self.rect.move_ip(0, self.gravityvel)
                self.gravityvel += self.gravityaccel
                self.airbourne = True
                if self.grounded:
                    self.gravityvel = 5

        if self.moving_right: # Moving right on ground
            self.rect.move_ip(self.vel, 0)
            self.vel += self.accel
            if self.vel > self.maxspeed:
                self.vel = self.maxspeed
        elif self.moving_left: # Moving left on ground
            self.rect.move_ip(-self.vel, 0)
            self.vel += self.accel
            if self.vel > self.maxspeed:
                self.vel = self.maxspeed

        self.image = self.sprites[int(self.current_sprite)]


class Player(pygame.sprite.Sprite):
    """
    Initializes a Player object that uses sprites to differentiate between idle and moving stages

    === Attributes ===
    sprites -> A list of sprite images for the Player
    current_sprite -> The current sprite displayed on the player at a given time
    rect -> The physical object of the Player
    alive -> Determines if the Player is alive
    lives -> The amount of lives a Player has
    recovering -> Determines if the Player is recovering
    is_animating -> Determines if the Sprite is animating
    is_jumping -> Determines of the Sprite is jumping
    moving_* -> Determines if the Sprite is moving in a certain direction
    fast_fall -> Dertermines if the Player is in fast fall
    grounded -> Determines if the Sprite is on the ground
    *accel -> The acceleration of the Player in a certain direction
    init_*vel -> The initial velocity of the player in a certain direction
    *vel -> The velocity of the Player in a certain direction
    maxspeed -> The maximum speed that the Player can travel moving left and right
    floor -> The floor underneath the Player
    checkpoint -> The level that the Player respawns at
    deaths -> Represents the amount of times the Player has died
    """

    sprites: list[pygame.Surface]
    current_sprite: int
    rect: pygame.Rect
    spawnpoint: tuple[int, int]

    alive: bool
    lives: int
    recovering: bool

    is_animating: bool
    moving_right: bool
    moving_left: bool
    moving_up: bool
    fast_fall: bool
    grounded: bool

    airbourne: bool
    air_resistance: int
    jumps: int

    accel: float
    init_vel: float
    vel: float
    maxspeed: float

    jumpaccel: float
    init_jumpvel: float
    jumpvel: float

    fallaccel: float
    init_fallvel: float
    fallvel: float

    gravityaccel: float
    init_gravityvel: float
    gravityvel: float

    floor: ForegroundObj
    base: ForegroundObj

    checkpoint: int

    deaths: int

    def __init__(self, x: int, y: int, base: ForegroundObj) -> None:
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load('idle.png'), (40, 40))) # Index 0
        self.sprites.append(pygame.transform.scale(pygame.image.load('dead.png'), (40, 40))) # Index 1
        self.sprites.append(pygame.transform.scale(pygame.image.load('jump_1.png'), (55, 40))) # Index 2
        self.sprites.append(pygame.transform.scale(pygame.image.load('jump_2.png'), (55, 40))) # Index 3
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawnpoint = (x, y)

        self.alive = True
        self.lives = 3
        self.recovering = False

        self.is_animating = False
        self.is_jumping = False
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.fast_fall = False
        self.grounded = False

        self.airbourne = False
        self.air_resistance = 1.25
        self.jumps = 2

        self.accel = 0.2
        self.init_vel = 5.0
        self.vel = self.init_vel
        self.maxspeed = 10.0

        self.jumpaccel = 2.0
        self.init_jumpvel = 25.0
        self.jumpvel = self.init_jumpvel

        self.fallaccel = 2
        self.init_fallvel = 2
        self.fallvel = self.init_fallvel

        self.gravityaccel = 0.25
        self.init_gravityvel = 3
        self.gravityvel = self.init_gravityvel

        self.floor = None
        self.base = base

        self.checkpoint = 1

        self.deaths = 0

    def move_right(self) -> None:
        self.moving_right = True
    
    def move_left(self) -> None:
        self.moving_left = True

    def jump(self) -> None:
        if self.jumps > 0 and not self.is_jumping and not self.recovering:
            jump_sound.play()
            self.is_animating = True
            self.current_sprite = 2
            self.is_jumping = True
            self.moving_up = False
            self.jumpvel = self.init_jumpvel
    
    def move_down(self) -> None:
        self.fast_fall = True

    def in_air(self) -> None:
        self.airbourne = True
        self.grounded = False

    def ground(self) -> None:
        self.fallvel = self.init_fallvel
        self.grounded = True
        self.airbourne = False
        self.jumps = 2
    
    def make_ground(self, ground: ForegroundObj) -> None:
        self.floor = ground

    def stop_left(self) -> None:
        self.moving_left = False
        self.vel = self.init_vel
    
    def stop_right(self) -> None:
        self.moving_right = False
        self.vel = self.init_vel
    
    def stop_down(self) -> None:
        self.fast_fall = False
    
    def collide(self, name: str, objects: list[Obj]) -> bool:
        for object in objects:
            if object.name == name and self.rect.colliderect(object.rect):
                return True
        return False

    def death(self) -> None:
        if self.alive and not self.recovering:
            self.deaths += 1
            self.lives -= 1
            self.alive = False
            self.current_sprite = 1
            self.floor = self.base
            self.rect.center = self.spawnpoint
            self.alive = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 100, 10)
            pygame.time.set_timer(pygame.USEREVENT + 3, 1000, 1)
            self.is_animating = False
            self.is_jumping = False
            self.recovering = True
    
    def restart(self, new_spawn: tuple[int, int] = None, objects: list[Obj] = None) -> None:
        if new_spawn:
            self.spawnpoint = new_spawn
            self.restart(None, objects)
        else:
            self.rect.center = self.spawnpoint
            self.floor = check_ground(self, objects)
    
    def reset_lives(self) -> None:
        self.lives = 3

    def life_up(self) -> None:
        if self.lives < 3:
            self.lives += 1

    def recovery(self) -> None:
        if self.recovering:
            if self.current_sprite == 0:
                self.current_sprite = 1
            else:
                self.current_sprite = 0
    
    def end_recovery(self) -> None:
        self.recovering = False
        self.current_sprite = 0

    def hit(self, enemies: list[Enemy]) -> bool:
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False

    def new_checkpoint(self, level: int) -> None:
        self.checkpoint = level
    
    def get_checkpoint(self) -> None:
        return self.checkpoint

    def update(self) -> None:
        if self.is_animating: # Jumping Animation
            if self.airbourne: #In Air
                self.current_sprite = 0
                self.moving_up = True
                self.jumps -= 1
                self.gravityvel = self.init_gravityvel
                self.current_sprite = 0
                self.is_animating = False
            else: # On Ground
                self.current_sprite += 0.3
                if self.current_sprite >= len(self.sprites):
                    self.airbourne = True
                    self.jumps -= 1
                    self.gravityvel = self.init_gravityvel
                    self.current_sprite = 0
                    self.is_animating = False
                    self.moving_up = True

        if self.moving_up: # Jumping
            self.rect.move_ip(0, -self.jumpvel)
            self.grounded = False
            self.jumpvel -= self.jumpaccel
            if self.jumpvel <= self.init_jumpvel/2:
                self.is_jumping = False
            if self.jumpvel <= 0:
                self.moving_up = False
                self.jumpvel = 20
        else: # Falling
            if self.airbourne:
                self.rect.move_ip(0, self.gravityvel)
                self.gravityvel += self.gravityaccel
                self.airbourne = True
                if self.grounded:
                    self.gravityvel = 5
        
        if self.moving_right and self.moving_left:
            self.vel = self.init_vel

        if self.airbourne: # In air
            if self.moving_right: # Moving right in air
                self.rect.move_ip(self.vel/self.air_resistance, 0)
                self.vel += self.accel/self.air_resistance
                if self.vel > self.maxspeed/self.air_resistance:
                    self.vel = self.maxspeed/self.air_resistance
            elif self.moving_left: # Moving left in air
                self.rect.move_ip(-self.vel/self.air_resistance, 0)
                self.vel += self.accel/self.air_resistance
                if self.vel > self.maxspeed/self.air_resistance:
                    self.vel = self.maxspeed/self.air_resistance
            elif not self.is_animating:
                self.vel = self.init_vel
        else: # On ground
            if self.moving_right: # Moving right on ground
                self.rect.move_ip(self.vel, 0)
                self.vel += self.accel
                if self.vel > self.maxspeed:
                    self.vel = self.maxspeed
            elif self.moving_left: # Moving left on ground
                self.rect.move_ip(-self.vel, 0)
                self.vel += self.accel
                if self.vel > self.maxspeed:
                    self.vel = self.maxspeed
            elif not self.is_animating:
                self.vel = self.init_vel
        
        if self.fast_fall: # Fast falling
            self.rect.move_ip(0, self.fallvel)
            self.fallvel += self.fallaccel
            if self.grounded:
                self.fallvel = self.init_fallvel
                self.fast_fall = False

        self.image = self.sprites[int(self.current_sprite)]


class Boss(Enemy):
    """
    Initializes a Player object that uses sprites to differentiate between idle and moving stages

    === Attributes ===
    sprites -> A list of sprite images for the Player
    current_sprite -> The current sprite displayed on the player at a given time
    rect -> The physical object of the Player
    alive -> Determines if the Player is alive
    recovering -> Determines if the Player is recovering
    is_animating -> Determines if the Sprite is animating
    is_jumping -> Determines of the Sprite is jumping
    moving_* -> Determines if the Sprite is moving in a certain direction
    fast_fall -> Dertermines if the Player is in fast fall
    grounded -> Determines if the Sprite is on the ground
    *accel -> The acceleration of the Player in a certain direction
    init_*vel -> The initial velocity of the player in a certain direction
    *vel -> The velocity of the Player in a certain direction
    maxspeed -> The maximum speed that the Player can travel moving left and right
    floor -> The floor underneath the Player
    stunned -> Determines if the Boss is stunned or not
    """

    sprites: list[pygame.Surface]
    current_sprite: int
    rect: pygame.Rect

    alive: bool

    is_animating: bool
    moving_right: bool
    moving_left: bool
    moving_up: bool

    grounded: bool
    airbourne: bool
    air_resistance: int
    jumps: int

    accel: float
    init_vel: float
    vel: float
    maxspeed: float

    jumpaccel: float
    init_jumpvel: float
    jumpvel: float

    gravityaccel: float
    init_gravityvel: float
    gravityvel: float

    floor: ForegroundObj

    stunned: bool

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load('enemy_idle.png'), (200, 200))) # Index 0
        self.sprites.append(pygame.transform.scale(pygame.image.load('enemy_jump1.png'), (275, 200))) # Index 1
        self.sprites.append(pygame.transform.scale(pygame.image.load('enemy_jump2.png'), (275, 200))) # Index 2
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.alive = True
        self.recovering = False

        self.is_animating = False
        self.is_jumping = False
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.fast_fall = False
        self.grounded = False

        self.airbourne = False
        self.air_resistance = 1.25
        self.jumps = 1

        self.accel = 0.2
        self.init_vel = 10
        self.vel = self.init_vel
        self.maxspeed = 10

        self.jumpaccel = 1.0
        self.init_jumpvel = 50.0
        self.jumpvel = self.init_jumpvel

        self.fallaccel = 2
        self.init_fallvel = 2
        self.fallvel = self.init_fallvel

        self.gravityaccel = 0.25
        self.init_gravityvel = 3
        self.gravityvel = self.init_gravityvel

        self.floor = None

        self.stunned = False
    

class Jukebox():
    """
    Initializes a Jukebox object that controls sounds that are to play from a list
    
    === Attribites ===
    song_list -> The list of songs that the Jukebox will play from
    current_song -> The name of the song that is playing
    current_index -> The current song index of the Jukebox
    next_song -> The next song that will play from the Jukebox
    looping -> Determines if the Jukebox will loop the queue or not
    """
    song_list: list[str]
    current_index: int
    current_song: str
    next_index: int
    next_song: str
    looping: bool

    def __init__(self, lst: list[str], loop: bool) -> None:
        self.song_list = lst
        self.current_index = 0
        self.current_song = self.song_list[self.current_index]
        self.looping = loop
        if self.looping:
            if len(self.song_list) == self.current_index + 1:
                self.next_index = 0
            else:
                self.next_index = self.current_index + 1
        else:
            if len(self.song_list) == self.current_index + 1:
                self.next_index = -1
            else:
                self.next_index = self.current_index + 1
        if self.next_index >= 0:
            self.next_song = self.song_list[self.next_index]
        else:
            self.next_song = None
    
    def get_current_song(self) -> str:
        return self.current_song
    
    def get_next_song(self) -> str:
        return self.next_song
    
    def playing(self) -> bool:
        return pygame.mixer.music.get_busy()
    
    def play(self) -> None:
        os.chdir('..')
        os.chdir('audio')
        if self.current_song:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(MUSIC)
        os.chdir('..')
        os.chdir('images')
    
    def pause(self) -> None:
        pygame.mixer.music.pause()
    
    def unpause(self) -> None:
        pygame.mixer.music.unpause()

    def next(self) -> None:
        self.current_index = self.next_index
        self.current_song = self.next_song
        if self.looping:
            if len(self.song_list) == self.current_index + 1:
                self.next_index = 0
            else:
                self.next_index = self.current_index + 1
        else:
            if len(self.song_list) == self.current_index + 1:
                self.next_index = -1
            else:
                self.next_index = self.current_index + 1
        if self.next_index >= 0:
            self.next_song = self.song_list[self.next_index]
        else:
            self.next_song = None
        self.play()



class Game():
    """
    Initializes a Game object that controls what happpens in the game
    
    === Attributes ===
    screen -> The Surface of the game screen
    level -> The current level of the game
    base -> The lowest possible source of ground in the game (usually the grass)
    *_objs -> A list of certain object types
    player -> The Player of the game
    enemies -> A list of all the enemies in the game
    boss -> The boss of the game
    moving_sprites -> All of the sprites in the game
    stage -> The stage of a certain level
    jukebox -> The Jukebox of the game
    hard -> Determines if Hard Mode is unlocked
    """

    screen: pygame.Surface
    level: int
    base: ForegroundObj
    background_objs: list[BackgroundObj]
    foreground_objs: list[ForegroundObj]
    interactive_objs: list[InteractiveObj]
    textbox_objs: list[Textbox]
    button_objs: list[Button]
    on_screen_objects: list[Obj]
    player: Player
    enemies: list[Enemy]
    boss: Boss
    moving_sprites: pygame.sprite.Group
    stage: int
    jukebox: Jukebox
    hard: bool

    def __init__(self, screen: pygame.Surface, base: ForegroundObj, on_screen_objects: list[Obj], 
                 player: Player, moving_sprites: pygame.sprite.Group, background_objs: list[BackgroundObj], 
                 foreground_objs: list[ForegroundObj], interactive_objs: list[InteractiveObj], 
                 textbox_objs: list[Textbox], button_objs: list[Button], songs: list[str]) -> None:
        self.screen = screen
        self.level = 1
        self.base = base
        self.on_screen_objects = on_screen_objects
        self.background_objs = background_objs
        self.foreground_objs = foreground_objs
        self.interactive_objs = interactive_objs
        self.textbox_objs = textbox_objs
        self.button_objs = button_objs
        self.player = player
        self.enemies = []
        self.boss = None
        self.moving_sprites = moving_sprites

        self.stage = 0

        self.jukebox = Jukebox(songs, True)

        self.hard = False

    def clear_level(self) -> None:
        pygame.time.set_timer(ENEMY1MOVE, 0)
        pygame.time.set_timer(ENEMY1JUMP, 0)
        pygame.time.set_timer(ENEMY2MOVE, 0)
        pygame.time.set_timer(ENEMY2JUMP, 0)
        pygame.time.set_timer(ENEMY3MOVE, 0)
        pygame.time.set_timer(ENEMY3JUMP, 0)
        pygame.time.set_timer(FIREMOVE, 0)
        pygame.time.set_timer(BOSSMOVE, 0)
        pygame.event.clear()
        
        for sprite in self.moving_sprites.sprites():
            if type(sprite) == Enemy or type(sprite) == Boss:
                sprite.kill()
                self.moving_sprites.remove(sprite)
                self.enemies.pop()
            elif type(sprite) == Stars:
                self.moving_sprites.remove(sprite)
        
        self.on_screen_objects.clear()
    
    def next_level(self) -> None:
        self.start_time = pygame.time.get_ticks()
        self.clear_level()
        self.level += 1
        pygame.time.set_timer(LEVELDISAPPEAR, 2000, 1)
        pygame.time.set_timer(ENEMY1MOVE, 800)
        pygame.time.set_timer(ENEMY1JUMP, 2500)
        pygame.time.set_timer(ENEMY2MOVE, 1000)
        pygame.time.set_timer(ENEMY2JUMP, 2000)
        pygame.time.set_timer(ENEMY3MOVE, 1200)
        pygame.time.set_timer(ENEMY3JUMP, 2250)
        pygame.time.set_timer(FIREMOVE, 1000)
        self.generate()
    
    def main(self, type: str = '') -> None:
        self.clear_level()
        self.player.reset_lives()
        self.player.deaths = 0
        self.player.checkpoint = 1
        self.level = 0
        self.generate(type)
        makeLight(self.on_screen_objects)
    
    def options(self) -> None:
        self.clear_level()
        self.level = -1
        self.generate()
    
    def hard_mode(self) -> None:
        self.clear_level()
        self.level = -2
        self.generate()

    def restart(self) -> None:
        self.start_time = pygame.time.get_ticks()
        self.clear_level()
        self.player.reset_lives()
        self.level = self.player.get_checkpoint()
        self.generate()
        makeLight(self.on_screen_objects)
        pygame.time.set_timer(LEVELDISAPPEAR, 2000, 1)
        pygame.time.set_timer(ENEMY1MOVE, 800)
        pygame.time.set_timer(ENEMY1JUMP, 2500)
        pygame.time.set_timer(ENEMY2MOVE, 1000)
        pygame.time.set_timer(ENEMY2JUMP, 2000)
        pygame.time.set_timer(ENEMY3MOVE, 1200)
        pygame.time.set_timer(ENEMY3JUMP, 2250)
        pygame.time.set_timer(FIREMOVE, 1000)

    def generate(self, type: str = '') -> None:
        self.stage = 0
        for obj in self.background_objs:
            self.on_screen_objects.append(obj)
        for obj in self.foreground_objs:
            if obj.name == "grass":
                self.on_screen_objects.append(obj)

        if self.level == -2:
            remove_list = []
            for obj in self.on_screen_objects:
                if obj.name == "heart1" or obj.name == "heart2" or obj.name == "heart3":
                    remove_list.append(obj)
            for obj in remove_list:
                self.on_screen_objects.remove(obj)
            for obj in self.textbox_objs:
                if obj.name == 'title':
                    title = obj.clone()
                    title.change_text("Makeshift Mario", "white")
                    title_outline = obj.clone((400, 60))
                    title_outline.text.set_txt(pygame.font.SysFont('Verdana', 61, True))
                    title_outline.change_text("Makeshift Mario", "black")
                    self.on_screen_objects.append(title_outline)
                    self.on_screen_objects.append(title)
            text1 = Textbox(self.screen, 'text1', (100, 50), pygame.font.SysFont('Verdana', 20), 'center', (self.screen.get_width()/2, self.screen.get_height()/2))
            text1.change_text("Hard Mode is coming soon!", "white")
            self.on_screen_objects.append(text1)

            back = Button(self.screen, "Back", 'Button.png', (125, 40), pygame.font.SysFont('Verdana', 25, True), (self.screen.get_width()/2, self.screen.get_height()*2/3))
            self.on_screen_objects.append(back)

        if self.level == -1:
            volume_slider = Textbox
            remove_list = []
            for obj in self.on_screen_objects:
                if obj.name == "heart1" or obj.name == "heart2" or obj.name == "heart3":
                    remove_list.append(obj)
            for obj in remove_list:
                self.on_screen_objects.remove(obj)
            for obj in self.textbox_objs:
                if obj.name == 'title':
                    title = obj.clone()
                    title.change_text("Makeshift Mario", "white")
                    title_outline = obj.clone((400, 60))
                    title_outline.text.set_txt(pygame.font.SysFont('Verdana', 61, True))
                    title_outline.change_text("Makeshift Mario", "black")
                    self.on_screen_objects.append(title_outline)
                    self.on_screen_objects.append(title)
                elif obj.name == 'Options Volume':
                    volume = obj.clone()
                    volume.change_text("Background Music:", "black")
                    self.on_screen_objects.append(volume)
                elif obj.name == 'Options Volume Slider':
                    volume_slider = obj
                    self.on_screen_objects.append(obj)
            for obj in self.button_objs:
                if obj.name == 'Options Volume Button':
                    obj.place(volume_slider.rect.left + pygame.mixer.music.get_volume()*volume_slider.rect.width, volume_slider.rect.centery)
                    self.on_screen_objects.append(obj)
            back = Button(self.screen, "Back", 'Button.png', (125, 40), pygame.font.SysFont('Verdana', 25, True), (self.screen.get_width()/2, self.screen.get_height()*2/3))
            self.on_screen_objects.append(back)

        if self.level == 0:
            if not type == 'options':
                os.chdir('..')
                os.chdir('audio')
                pygame.mixer.music.load('mainmenu.wav')
                os.chdir('..')
                os.chdir('images')
                pygame.mixer.music.play(1000)
            remove_list = []
            for obj in self.on_screen_objects:
                if obj.name == "heart1" or obj.name == "heart2" or obj.name == "heart3":
                    remove_list.append(obj)
            for obj in remove_list:
                self.on_screen_objects.remove(obj)
            for obj in self.textbox_objs:
                if obj.name == "title":
                    title = obj.clone()
                    title.change_text("Makeshift Mario", "white")
                    title_outline = obj.clone((400, 60))
                    title_outline.text.set_txt(pygame.font.SysFont('Verdana', 61, True))
                    title_outline.change_text("Makeshift Mario", "black")
                    self.on_screen_objects.append(title_outline)
                    self.on_screen_objects.append(title)
            for obj in self.button_objs:
                if obj.name == "Play":
                    obj.show()
                    self.on_screen_objects.append(obj)
                elif obj.name == "Options":
                    obj.show()
                    self.on_screen_objects.append(obj)
                elif obj.name == "Hard Mode":
                    if self.hard:
                        obj.change_img("hard_mode_button.png")
                    obj.show()
                    self.on_screen_objects.append(obj)

        if self.level > 0:
            volume_icon = Button
            volume_slider = Textbox
            music_frame = Frame(self.screen, "Music Frame", (175, 150), (0, 0), 'volume_background.png', 60)
            music_frame.speed = 2
            for obj in self.button_objs:
                if obj.name == "volume icon":
                    volume_icon = obj
                    music_frame.rect.left = volume_icon.rect.right - 20
                    music_frame.rect.bottom = volume_icon.rect.bottom
                    music_frame.place(music_frame.rect.centerx, music_frame.rect.centery)
                    self.on_screen_objects.append(obj)
                elif obj.name == "exit":
                    self.on_screen_objects.append(obj)
            for obj in self.textbox_objs:
                if obj.name == "deaths":
                    deaths = obj.clone()
                    deaths.change_text(f'Deaths: {self.player.deaths}', "white")
                    self.on_screen_objects.append(deaths)
                elif obj.name == "Options Volume Slider":
                    volume_slider = obj.clone()
                    volume_slider.change_text('', "black")
                    volume_slider.place(music_frame.rect.width/2, music_frame.rect.height - 20)
                    music_frame.add(volume_slider)
            for obj in self.button_objs:
                if obj.name == 'Options Volume Button':
                    volume_button = obj.clone()
                    volume_button.change_img('slider_button_2.png', (25, 25))
                    volume_button.change_text('', "black")
                    volume_button.place(volume_slider.rect.left + pygame.mixer.music.get_volume()*volume_slider.rect.width, volume_slider.rect.centery)
                    music_frame.add(volume_button)
            play_button = Button(self.screen, "play_button", 'play.png', (25, 25), pygame.font.Font(None, 0), (music_frame.rect.width * 1/3, music_frame.rect.height/2))
            play_button.change_text_color("empty")
            pause_button = Button(self.screen, "pause_button", 'pause.png', (25, 25), pygame.font.Font(None, 0), (music_frame.rect.width * 1/3, music_frame.rect.height/2))
            pause_button.change_text_color("empty")
            pause_button.hide()
            skip_button = Button(self.screen, "skip_button", 'fast_forward.png', (25, 25), pygame.font.Font(None, 0), (music_frame.rect.width * 2/3, music_frame.rect.height/2))
            skip_button.change_text_color("empty")
            music_frame.addAll([play_button, pause_button, skip_button])
            music_frame.hide()
            self.on_screen_objects.append(music_frame)

        if self.level == 1:
            self.player.restart((self.base.rect.centerx, self.base.rect.top - 50), self.on_screen_objects)
            left_enemy_platform = ForegroundObj
            right_enemy_platform = ForegroundObj
            chest_platform = ForegroundObj
            for object in self.foreground_objs:
                if object.name == "enemy_platform":
                    left_enemy_platform = object.clone()
                    left_enemy_platform.rect.left = 0
                    left_enemy_platform.rect.centery = self.screen.get_height()/2
                    right_enemy_platform = object.clone()
                    right_enemy_platform.rect.right = self.screen.get_width()
                    right_enemy_platform.rect.centery = self.screen.get_height()/2
                    self.on_screen_objects.append(left_enemy_platform)
                    self.on_screen_objects.append(right_enemy_platform)
                elif object.name == "chest_platform":
                    chest_platform = object.clone()
                    self.on_screen_objects.append(chest_platform)

            for object in self.interactive_objs:
                if object.name == "spikes":
                    left_spikes = object.clone()
                    left_spikes.rect.left = 0
                    left_spikes.rect.bottom = self.base.rect.top
                    right_spikes = object.clone()
                    right_spikes.rect.right = self.screen.get_width()
                    right_spikes.rect.bottom = self.base.rect.top
                    self.on_screen_objects.append(left_spikes)
                    self.on_screen_objects.append(right_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = chest_platform.rect.top
                    chest.rect.centerx = chest_platform.rect.centerx
                    self.on_screen_objects.append(chest)
            
            enemy1 = Enemy(left_enemy_platform.rect.centerx, left_enemy_platform.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()
            enemy2 = Enemy(right_enemy_platform.rect.centerx, right_enemy_platform.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()

        elif self.level == 2:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            left_roof = ForegroundObj
            right_roof = ForegroundObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    left_roof = object.clone()
                    left_roof.rect.left = 0 
                    left_roof.rect.centery = self.screen.get_height()/1.6
                    right_roof = object.clone()
                    right_roof.rect.right = self.screen.get_width()
                    right_roof.rect.centery = self.screen.get_height()/3
                    self.on_screen_objects.append(left_roof)
                    self.on_screen_objects.append(right_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = left_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = right_roof.rect.top
                    chest.rect.right = self.screen.get_width()-100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    rnd = random.randint(1, 3)
                    check = random.randint(1, 3)
                    if rnd == check:
                        health = object.clone()
                        health.rect.left = chest.rect.right + 10
                        health.rect.centery = chest.rect.centery
                        self.on_screen_objects.append(health)
            
            enemy1 = Enemy(left_roof.rect.right - 25, left_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()

        elif self.level == 3:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            left_roof = ForegroundObj
            right_roof = ForegroundObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    left_roof = object.clone()
                    left_roof.rect.left = 0 
                    left_roof.rect.centery = self.screen.get_height()/1.6
                    right_roof = object.clone()
                    right_roof.rect.right = self.screen.get_width()
                    right_roof.rect.centery = self.screen.get_height()/3
                    self.on_screen_objects.append(left_roof)
                    self.on_screen_objects.append(right_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = left_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = right_roof.rect.top
                    chest.rect.right = self.screen.get_width()-100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    rnd = random.randint(1, 3)
                    check = random.randint(1, 3)
                    if rnd == check:
                        health = object.clone()
                        health.rect.left = chest.rect.right + 10
                        health.rect.centery = chest.rect.centery
                        self.on_screen_objects.append(health)
            
            enemy1 = Enemy(left_roof.rect.right - 25, left_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()
            enemy2 = Enemy(right_roof.rect.left + 20, right_roof.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()

        elif self.level == 4:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            left_roof = ForegroundObj
            right_roof = ForegroundObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    left_roof = object.clone()
                    left_roof.rect.left = 0 
                    left_roof.rect.centery = self.screen.get_height()/1.6
                    right_roof = object.clone()
                    right_roof.rect.right = self.screen.get_width()
                    right_roof.rect.centery = self.screen.get_height()/3
                    self.on_screen_objects.append(left_roof)
                    self.on_screen_objects.append(right_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = left_roof.rect.top
                    level_three_spikes = object.clone()
                    level_three_spikes.rect.centerx = right_roof.rect.centerx - 100
                    level_three_spikes.rect.bottom = right_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                    self.on_screen_objects.append(level_three_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = right_roof.rect.top
                    chest.rect.right = self.screen.get_width()-100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    rnd = random.randint(1, 3)
                    check = random.randint(1, 3)
                    if rnd == check:
                        health = object.clone()
                        health.rect.left = chest.rect.right + 10
                        health.rect.centery = chest.rect.centery
                        self.on_screen_objects.append(health)
            
            enemy1 = Enemy(left_roof.rect.right - 25, left_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()
            enemy2 = Enemy(right_roof.rect.left, right_roof.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()

        elif self.level == 5:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            left_roof = ForegroundObj
            right_roof = ForegroundObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    left_roof = object.clone()
                    left_roof.rect.left = 0 
                    left_roof.rect.centery = self.screen.get_height()/1.6
                    right_roof = object.clone()
                    right_roof.rect.right = self.screen.get_width()
                    right_roof.rect.centery = self.screen.get_height()/3
                    self.on_screen_objects.append(left_roof)
                    self.on_screen_objects.append(right_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = left_roof.rect.top
                    level_three_spikes = object.clone()
                    level_three_spikes.rect.centerx = right_roof.rect.centerx - 100
                    level_three_spikes.rect.bottom = right_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                    self.on_screen_objects.append(level_three_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = right_roof.rect.top
                    chest.rect.right = self.screen.get_width()-100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    rnd = random.randint(1, 3)
                    check = random.randint(1, 3)
                    if rnd == check:
                        health = object.clone()
                        health.rect.left = chest.rect.right + 10
                        health.rect.centery = chest.rect.centery
                        self.on_screen_objects.append(health)
            
            enemy1 = Enemy(left_roof.rect.right - 25, left_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()
            enemy2 = Enemy(right_roof.rect.left, right_roof.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()
            enemy3 = Enemy(level_one_spikes.rect.left - 25, self.base.rect.top - 25)
            self.moving_sprites.add(enemy3)
            self.enemies.append(enemy3)
            enemy3.move_left()

        elif self.level == 6:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            left_roof = ForegroundObj
            right_roof = ForegroundObj
            level_one_spikes = InteractiveObj
            chest = InteractiveObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    left_roof = object.clone()
                    left_roof.rect.left = 0 
                    left_roof.rect.centery = self.screen.get_height()/1.6
                    right_roof = object.clone()
                    right_roof.rect.right = self.screen.get_width()
                    right_roof.rect.centery = self.screen.get_height()/3
                    self.on_screen_objects.append(left_roof)
                    self.on_screen_objects.append(right_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = left_roof.rect.top
                    level_three_spikes = object.clone()
                    level_three_spikes.rect.centerx = right_roof.rect.centerx - 100
                    level_three_spikes.rect.bottom = right_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                    self.on_screen_objects.append(level_three_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = right_roof.rect.top
                    chest.rect.right = self.screen.get_width()-100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    rnd = random.randint(1, 3)
                    check = random.randint(1, 3)
                    if rnd == check:
                        health = object.clone()
                        health.rect.left = chest.rect.right + 10
                        health.rect.centery = chest.rect.centery
                        self.on_screen_objects.append(health)
                elif object.name == "fire":
                    fire = object.clone()
                    fire.rect.centerx = level_one_spikes.rect.centerx - 50
                    fire.rect.centery = level_one_spikes.rect.centery - 100
                    self.on_screen_objects.append(fire)
                elif object.name == "flag":
                    if not self.player.get_checkpoint() == self.level:
                        object.rect.right = chest.rect.left - 20
                        object.rect.bottom = right_roof.rect.top
                        self.on_screen_objects.append(object)
            
            enemy1 = Enemy(left_roof.rect.right - 25, left_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()
            enemy2 = Enemy(right_roof.rect.left, right_roof.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()
            enemy3 = Enemy(level_one_spikes.rect.left - 25, self.base.rect.top - 25)
            self.moving_sprites.add(enemy3)
            self.enemies.append(enemy3)
            enemy3.move_left()

        elif self.level == 7:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            left_roof = ForegroundObj
            right_roof = ForegroundObj
            level_one_spikes = InteractiveObj
            level_two_spikes = InteractiveObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    left_roof = object.clone()
                    left_roof.rect.left = 0 
                    left_roof.rect.centery = self.screen.get_height()/1.6
                    right_roof = object.clone()
                    right_roof.rect.right = self.screen.get_width()
                    right_roof.rect.centery = self.screen.get_height()/3
                    self.on_screen_objects.append(left_roof)
                    self.on_screen_objects.append(right_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = left_roof.rect.top
                    level_three_spikes = object.clone()
                    level_three_spikes.rect.centerx = right_roof.rect.centerx - 100
                    level_three_spikes.rect.bottom = right_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                    self.on_screen_objects.append(level_three_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = right_roof.rect.top
                    chest.rect.right = self.screen.get_width()-100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    rnd = random.randint(1, 3)
                    check = random.randint(1, 3)
                    if rnd == check:
                        health = object.clone()
                        health.rect.left = chest.rect.right + 10
                        health.rect.centery = chest.rect.centery
                        self.on_screen_objects.append(health)
                elif object.name == "fire":
                    fire = object.clone()
                    fire.rect.centerx = level_one_spikes.rect.centerx - 50
                    fire.rect.centery = level_one_spikes.rect.centery - 100
                    fire2 = object.clone()
                    fire2.rect.centerx = level_two_spikes.rect.centerx - 50
                    fire2.rect.centery = level_two_spikes.rect.centery - 75
                    self.on_screen_objects.append(fire)
                    self.on_screen_objects.append(fire2)
            
            enemy1 = Enemy(left_roof.rect.right - 25, left_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()
            enemy2 = Enemy(right_roof.rect.left, right_roof.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()
            enemy3 = Enemy(level_one_spikes.rect.left - 25, self.base.rect.top - 25)
            self.moving_sprites.add(enemy3)
            self.enemies.append(enemy3)
            enemy3.move_left()

        elif self.level == 8:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            bot_roof = ForegroundObj
            middle_roof = ForegroundObj
            top_roof = ForegroundObj
            level_one_spikes = InteractiveObj
            level_two_spikes = InteractiveObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    bot_roof = object.clone()
                    bot_roof.rect.left = 0 
                    bot_roof.rect.centery = self.screen.get_height()/1.5
                    middle_roof = object.clone()
                    middle_roof.rect.right = self.screen.get_width() 
                    middle_roof.rect.centery = self.screen.get_height()/2.25
                    top_roof = object.clone()
                    top_roof.rect.left = 0 
                    top_roof.rect.centery = self.screen.get_height()/5
                    self.on_screen_objects.append(bot_roof)
                    self.on_screen_objects.append(middle_roof)
                    self.on_screen_objects.append(top_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = bot_roof.rect.top
                    level_three_spikes = object.clone()
                    level_three_spikes.rect.right = self.screen.get_width()
                    level_three_spikes.rect.bottom = middle_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                    self.on_screen_objects.append(level_three_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = top_roof.rect.top
                    chest.rect.left = 100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    rnd = random.randint(1, 3)
                    check = random.randint(1, 3)
                    if rnd == check:
                        health = object.clone()
                        health.rect.left = chest.rect.right + 10
                        health.rect.centery = chest.rect.centery
                        self.on_screen_objects.append(health)
                elif object.name == "fire":
                    fire = object.clone()
                    fire.rect.centerx = level_one_spikes.rect.centerx - 75
                    fire.rect.centery = level_one_spikes.rect.centery - 100
                    fire.speed = 3
                    fire2 = object.clone()
                    fire2.rect.centerx = level_two_spikes.rect.centerx - 35
                    fire2.rect.centery = level_two_spikes.rect.centery - 75
                    fire2.speed = 3
                    self.on_screen_objects.append(fire)
                    self.on_screen_objects.append(fire2)
                    pygame.time.set_timer(FIREMOVE, 600)
            
            enemy1 = Enemy(bot_roof.rect.right - 25, bot_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.move_left()
            enemy1.change_speed(4.0, 4.0)
            pygame.time.set_timer(ENEMY1MOVE, 2300)
            enemy2 = Enemy(middle_roof.rect.centerx - 225, middle_roof.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()
            enemy3 = Enemy(level_one_spikes.rect.left - 25, self.base.rect.top - 25)
            self.moving_sprites.add(enemy3)
            self.enemies.append(enemy3)
            enemy3.move_left()
            pygame.time.set_timer(ENEMY3MOVE, 1500)

        elif self.level == 9:
            bot_roof = ForegroundObj
            middle_roof = ForegroundObj
            top_roof = ForegroundObj
            level_one_spikes = InteractiveObj
            level_two_spikes = InteractiveObj
            level_three_spikes = InteractiveObj
            for object in self.foreground_objs:
                if object.name == "roof":
                    bot_roof = object.clone()
                    bot_roof.rect.left = 0 
                    bot_roof.rect.centery = self.screen.get_height()/1.5
                    middle_roof = object.clone()
                    middle_roof.rect.right = self.screen.get_width() 
                    middle_roof.rect.centery = self.screen.get_height()/2.25
                    top_roof = object.clone()
                    top_roof.rect.left = 0 
                    top_roof.rect.centery = self.screen.get_height()/5
                    self.on_screen_objects.append(bot_roof)
                    self.on_screen_objects.append(middle_roof)
                    self.on_screen_objects.append(top_roof)
            for object in self.interactive_objs:
                if object.name == "spikes":
                    level_one_spikes = object.clone()
                    level_one_spikes.rect.right = self.screen.get_width()
                    level_one_spikes.rect.bottom = self.base.rect.top
                    level_two_spikes = object.clone()
                    level_two_spikes.rect.left = 0
                    level_two_spikes.rect.bottom = bot_roof.rect.top
                    level_three_spikes = object.clone()
                    level_three_spikes.rect.right = self.screen.get_width()
                    level_three_spikes.rect.bottom = middle_roof.rect.top
                    self.on_screen_objects.append(level_one_spikes)
                    self.on_screen_objects.append(level_two_spikes)
                    self.on_screen_objects.append(level_three_spikes)
                elif object.name == "3_spikes":
                    level_four_spikes = object.clone()
                    level_four_spikes.rect.right = top_roof.rect.right
                    level_four_spikes.rect.bottom = top_roof.rect.top
                    self.on_screen_objects.append(level_four_spikes)
                elif object.name == "chest":
                    chest = object.clone()
                    chest.rect.bottom = top_roof.rect.top
                    chest.rect.left = 100
                    self.on_screen_objects.append(chest)
                elif object.name == "health":
                    health_right = object.clone()
                    health_right.rect.left = chest.rect.right + 10
                    health_right.rect.centery = chest.rect.centery
                    health_left = object.clone()
                    health_left.rect.right = chest.rect.left - 10
                    health_left.rect.centery = chest.rect.centery
                    self.on_screen_objects.append(health_right)
                    self.on_screen_objects.append(health_left)
                elif object.name == "fire":
                    fire = object.clone()
                    fire.rect.centerx = level_one_spikes.rect.centerx - 75
                    fire.rect.centery = level_one_spikes.rect.centery - 100
                    fire.speed = 3
                    fire2 = object.clone()
                    fire2.rect.centerx = level_two_spikes.rect.centerx - 35
                    fire2.rect.centery = level_two_spikes.rect.centery - 75
                    fire2.speed = 3
                    fire3 = object.clone()
                    fire3.rect.centerx = level_three_spikes.rect.centerx - 75
                    fire3.rect.centery = level_three_spikes.rect.centery - 100
                    fire3.speed = 3
                    self.on_screen_objects.append(fire)
                    self.on_screen_objects.append(fire2)
                    self.on_screen_objects.append(fire3)
                    pygame.time.set_timer(FIREMOVE, 600)
            
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)

            enemy1 = Enemy(bot_roof.rect.right - 25, bot_roof.rect.top - 25)
            self.moving_sprites.add(enemy1)
            self.enemies.append(enemy1)
            enemy1.change_speed(4.0, 4.0)
            enemy1.move_left()
            pygame.time.set_timer(ENEMY1MOVE, 2300)
            enemy2 = Enemy(middle_roof.rect.left + 25, middle_roof.rect.top - 25)
            self.moving_sprites.add(enemy2)
            self.enemies.append(enemy2)
            enemy2.move_right()
            enemy2.change_speed(4.0, 4.0)
            pygame.time.set_timer(ENEMY2MOVE, 2300)
            enemy3 = Enemy(level_one_spikes.rect.left - 30, self.base.rect.top - 25)
            self.moving_sprites.add(enemy3)
            self.enemies.append(enemy3)
            enemy3.change_speed(4.0, 4.0)
            enemy3.move_left()
            pygame.time.set_timer(ENEMY3MOVE, 2000)
        
        elif self.level == 10:
            self.player.restart((50, self.base.rect.top - 25), self.on_screen_objects)
            left_platform = ForegroundObj
            middle_platform = ForegroundObj
            right_platform = ForegroundObj
            for obj in self.foreground_objs:
                if obj.name == "platform":
                    left_platform = obj.clone()
                    left_platform.rect.centerx = self.screen.get_width()/4
                    left_platform.rect.centery = self.screen.get_height() * 2/3

                    middle_platform = obj.clone()
                    middle_platform.rect.centerx = self.screen.get_width()/2
                    middle_platform.rect.centery = self.screen.get_height()* 2/5

                    right_platform = obj.clone()
                    right_platform.rect.centerx = self.screen.get_width() * 3/4
                    right_platform.rect.centery = self.screen.get_height() * 2/3

                    self.on_screen_objects.append(left_platform)
                    self.on_screen_objects.append(middle_platform)
                    self.on_screen_objects.append(right_platform)
            for obj in self.interactive_objs:
                if obj.name == "key":
                    key = obj.clone()
                    key.rect.bottom = middle_platform.rect.top
                    key.rect.centerx = middle_platform.rect.centerx
                    self.on_screen_objects.append(key)
        
        elif self.level == 11:
            self.player.restart((self.screen.get_width()/2, self.base.rect.top - 25), self.on_screen_objects)
            right_platform = ForegroundObj
            for obj in self.foreground_objs:
                if obj.name == "key_platform":
                    right_platform = obj.clone()
                    right_platform.rect.right = self.screen.get_width()
                    right_platform.rect.centery = self.screen.get_height() * 1/5
                    
                    self.on_screen_objects.append(right_platform)
                elif obj.name == "platform":

                    level_one_platform = obj.clone()
                    level_one_platform.rect.right = -10
                    level_one_platform.rect.centery = self.screen.get_height() * 2/3
                    level_one_platform.speed = 1

                    level_two_platform = obj.clone()
                    level_two_platform.rect.left = self.screen.get_width() + 10
                    level_two_platform.rect.centery = self.screen.get_height() * 1/3
                    level_two_platform.speed = 1

                    self.on_screen_objects.append(level_one_platform)
                    self.on_screen_objects.append(level_two_platform)
                elif obj.name == "roof":
                    right_grass = obj.clone()
                    right_grass.rect.left = self.base.rect.right
                    right_grass.rect.top = self.base.rect.top
                    left_grass = obj.clone()
                    left_grass.rect.right = self.base.rect.left
                    left_grass.rect.top = self.base.rect.top
                    self.on_screen_objects.append(right_grass)
                    self.on_screen_objects.append(left_grass)
            for obj in self.interactive_objs:
                if obj.name == "key":
                    key = obj.clone()
                    key.rect.bottom = right_platform.rect.top
                    key.rect.centerx = right_platform.rect.centerx
                    self.on_screen_objects.append(key)
                elif obj.name == "golden_chest":
                    gold_chest = obj.clone()
                    gold_chest.rect.center = (-1000, -1000)
                    self.on_screen_objects.append(gold_chest)
                elif obj.name == "spikes":
                    left_spikes = obj.clone()
                    left_spikes.rect.left = 0
                    left_spikes.rect.bottom = self.base.rect.top
                    right_spikes = obj.clone()
                    right_spikes.rect.right = self.screen.get_width()
                    right_spikes.rect.bottom = self.base.rect.top
                    self.on_screen_objects.append(left_spikes)
                    self.on_screen_objects.append(right_spikes)
                elif obj.name == "arrow":
                    arrow = obj.clone()
                    arrow.rect.centerx = -1000
                    arrow.rect.centery = -1000
                    self.on_screen_objects.append(arrow)
                elif obj.name == "light":
                    light = obj.clone()
                    light.surface.set_alpha(200)
                    light.rect.center = (-1000, -1000)
                    self.on_screen_objects.append(light)
            
            self.boss = Boss(self.screen.get_width()* 4/5, -1000)
            self.moving_sprites.add(self.boss)
            self.enemies.append(self.boss)
            pygame.time.set_timer(ENEMY1MOVE, 0)
            pygame.time.set_timer(ENEMY1JUMP, 0)
            pygame.time.set_timer(BOSSMOVE, 3000)

        elif self.level == 12:
            self.hard = True
            self.player.restart((self.screen.get_width()/2, self.base.rect.top - 25), self.on_screen_objects)
            win_frame = Frame(self.screen, "Win Frame", (300, 300), (self.screen.get_width()/2, self.screen.get_height()* 1/3))
            win_text1 = Textbox(self.screen, "Win Text", (600, 100), pygame.font.Font(None, 30), 'center', (win_frame.rect.width/2, win_frame.rect.height * 1/5))
            if self.player.deaths == 0:
                win_text1.change_text(f"Congratulations on beating Normal Mode with no deaths!", "white")
            elif self.player.deaths == 1:
                win_text1.change_text(f"Congratulations on beating Normal Mode with only 1 death!", "white")
            elif self.player.deaths == 2:
                win_text1.change_text(f"Congratulations on beating Normal Mode with only {self.player.deaths} deaths!", "white")
            win_text2 = Textbox(self.screen, "Win Text", (300, 100), pygame.font.Font(None, 30), 'center', (win_frame.rect.width/2, win_frame.rect.height * 2/3))
            win_text2.change_text(f"You've unlocked Hard Mode!", "white")
            mainmenu_button = Button(self.screen, "Main Menu", 'button.png', (175, 40), pygame.font.SysFont('Verdana', 25, True), (win_frame.rect.width/2, win_frame.rect.height))
            win_frame.addAll([win_text1, win_text2, mainmenu_button])
            self.on_screen_objects.append(win_frame)
            
        if self.level > 0:
            for obj in self.textbox_objs:
                if obj.name == "level":
                    if self.level < 11:
                        obj.change_text(f'Level {self.level}', "white")
                        self.on_screen_objects.append(obj)
                    else:
                        obj.change_text(f'Level {self.level}', "white")
                        self.on_screen_objects.append(obj)

            
def moveClouds(clouds: list[Obj]) -> None:
    for cloud in clouds:
        cloud.move()
        if cloud.rect.left == cloud.screen.get_width():
            cloud.rect.right = 0

def updateBackground(objects: list[Obj], alpha: int = None) -> None:
    """if alpha:
        for object in objects:
            if type(object) == BackgroundObj:
                object.update(alpha)
    else:"""
    for object in objects:
        if type(object) == BackgroundObj:
            object.update()

def searchFor(lst: list[Obj], name: str) -> Obj | None:
    for obj in lst:
        if obj.name == name:
            return obj
    return None

def updateForeground(objects: list[Obj], alpha: int = None) -> None:
    """if alpha:
        for object in objects:
            if type(object) == ForegroundObj:
                object.update(alpha)
    else:"""
    for object in objects:
        if type(object) == ForegroundObj:
            object.update()

def updateInteractive(objects: list[Obj], alpha: int = None) -> None:
    """if alpha:
        for object in objects:
            if type(object) == InteractiveObj:
                object.update(alpha)
    else:"""
    for object in objects:
        if type(object) == InteractiveObj:
            object.update()

def updateGUI(objects: list[Obj], alpha: int = None) -> None:
    """if alpha:
        for object in objects:
            if type(object) == Textbox or type(object) == Button or type(object) == Frame:
                object.update(alpha)
    else:"""
    for object in objects:
        if type(object) == Frame:
            object.update()
    for object in objects:
        if type(object) == Textbox or type(object) == Button:
            object.update()

def above(player: Player, check: ForegroundObj) -> bool:
    if player.rect.right > check.rect.left and player.rect.left < check.rect.right:
        if player.rect.bottom <= check.rect.top:
            return True
    return False

def below(player: Player, check: ForegroundObj) -> None:
    if check:
        if player.rect.right > check.rect.left and player.rect.left < check.rect.right:
            if player.rect.bottom >= check.rect.top:
                return True
    return False

def onTop(player: Player, check: ForegroundObj) -> bool:
    if check:
        if player.rect.right > check.rect.left and player.rect.left < check.rect.right:
            if player.rect.bottom >= check.rect.top and player.rect.bottom < check.rect.top + check.rect.height/4.5:
                return True
    return False

def on_top_of_others(player: Player, lst: list[Obj]) -> None:
    for obj in lst:
        if type(obj) == ForegroundObj or type(obj) == Button:
            if onTop(player, obj):
                return True
    return False

def onBottom(player: Player, check: ForegroundObj) -> bool:
    if player.rect.centerx > check.rect.left and player.rect.centerx < check.rect.right:
        if player.rect.top < check.rect.bottom and player.rect.top > check.rect.top:
            return True
    return False

def on_left_side(player: Player, check: ForegroundObj) -> bool:
    if player.rect.right > check.rect.left and player.rect.left < check.rect.left:
        if player.rect.bottom > check.rect.top and player.rect.top < check.rect.bottom:
            return True
    return False

def on_right_side(player: Player, check: ForegroundObj) -> bool:
    if player.rect.left < check.rect.right and player.rect.right > check.rect.right:
        if player.rect.bottom > check.rect.top and player.rect.top < check.rect.bottom:
            return True
    return False

def check_ground(player: Player, lst: list[Obj]) -> ForegroundObj:
    dist = 99999999999999999999999999999
    new_obj = None
    for obj in lst:
        if (type(obj) == ForegroundObj or type(obj) == Button) and above(player, obj):
            new_dist = obj.rect.top - player.rect.bottom
            if new_dist < dist:
                dist = new_dist
                new_obj = obj
    return new_obj

def updatePlayer(player: Player, objects: list[Obj], screen: pygame.Surface) -> None:
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > screen.get_width():
        player.rect.right = screen.get_width()
    if onTop(player, player.floor) or below(player, player.floor):
        player.rect.bottom = player.floor.rect.top
        player.ground()
    for object in objects:
        if type(object) == ForegroundObj:
            if not on_top_of_others(player, objects):
                player.in_air()
            if object.name == "wall":
                if on_left_side(player, object):
                    player.rect.right = object.rect.left
                elif on_right_side(player, object):
                    player.rect.left = object.rect.right
            elif object.name == "roof": 
                if onBottom(player, object):
                    player.rect.top = object.rect.bottom
                elif on_left_side(player, object):
                    player.rect.right = object.rect.left
                elif on_right_side(player, object):
                    player.rect.left = object.rect.right
    player.make_ground(check_ground(player, objects))

def updateEnemy(enemy: Enemy, objects: list[Obj], screen: pygame.Surface) -> None:
    if enemy.rect.left < 0:
        enemy.rect.left = 0
    if enemy.rect.right > screen.get_width():
        enemy.rect.right = screen.get_width()
    if onTop(enemy, enemy.floor) or below(enemy, enemy.floor):
        enemy.rect.bottom = enemy.floor.rect.top
        enemy.ground()
    for object in objects:
        if type(object) == ForegroundObj:
            if not on_top_of_others(enemy, objects):
                enemy.in_air()
            if object.name == "enemy_platform":
                if above(enemy, object):
                    if enemy.rect.left < object.rect.left:
                        enemy.rect.left = object.rect.left
                    elif enemy.rect.right > object.rect.right:
                        enemy.rect.right = object.rect.right
            elif object.name == "wall":
                if on_left_side(enemy, object):
                    enemy.rect.right = object.rect.left
                elif on_right_side(enemy, object):
                    enemy.rect.left = object.rect.right
            elif object.name == "roof": 
                if onBottom(enemy, object):
                    enemy.rect.top = object.rect.bottom
                elif on_left_side(enemy, object):
                    enemy.rect.right = object.rect.left
                elif on_right_side(enemy, object):
                    enemy.rect.left = object.rect.right
    enemy.make_ground(check_ground(enemy, objects))

def updateBoss(boss: Boss, objects: list[Obj], screen: pygame.Surface) -> None:
    if boss.rect.right > screen.get_width() + 205:
        boss.rect.right = screen.get_width() + 200
    elif boss.rect.left < -205:
        boss.rect.left = -200
    if onTop(boss, boss.floor) or below(boss, boss.floor):
        if boss.floor.name == "grass":
            boss.rect.bottom = boss.floor.rect.top
            boss.ground()
    for object in objects:
        if type(object) == ForegroundObj:
            if not on_top_of_others(boss, objects):
                boss.in_air()
            elif object.name == "wall":
                if on_left_side(boss, object):
                    boss.rect.right = object.rect.left
                elif on_right_side(boss, object):
                    boss.rect.left = object.rect.right
            elif object.name == "roof": 
                if onBottom(boss, object):
                    boss.rect.top = object.rect.bottom
                elif on_left_side(boss, object):
                    boss.rect.right = object.rect.left
                elif on_right_side(boss, object):
                    boss.rect.left = object.rect.right
    boss.make_ground(check_ground(boss, objects))

def updateLives(player: Player, objects: list[Obj]) -> None:
    for object in objects:
        if player.lives == 3:
            if object.name == "heart1" or object.name == "heart2" or object.name == "heart3":
                object.change_img("heart.png")
        elif player.lives == 2:
            if object.name == "heart1" or object.name == "heart2":
                object.change_img('heart.png')
            elif object.name == "heart3":
                object.change_img('heart_placeholder.png')
        elif player.lives == 1:
            if object.name == "heart1":
                object.change_img('heart.png')
            elif object.name == "heart2" or object.name == "heart3":
                object.change_img('heart_placeholder.png')
        else:
            if object.name == "heart1" or object.name == "heart2" or object.name == "heart3":
                object.change_img("heart_placeholder.png")

def updatePause(objects: list[Obj]) -> None:
    for obj in objects:
        if obj.name == "Resume" or obj.name == "Main Menu":
            obj.update()

def makeDark(objects: list[Obj]) -> None:
    for obj in objects:
        if type(obj) == BackgroundObj:
            if obj.name == "sky":
                obj.change_img('new_dark_sky.jpg')
            elif obj.name == "sun":
                obj.change_img('blood_moon.png', (200, 200))
                obj.place(100, 100)
            elif obj.img == "cloud1.png":
                obj.change_img('dark_cloud1.png')
            elif obj.img == "cloud2.png":
                obj.change_img('dark_cloud2.png')
            elif obj.img == "cloud3.png":
                obj.change_img('dark_cloud3.png')
            elif obj.img == "cloud4.png":
                obj.change_img('dark_cloud4.png')
        elif type(obj) == ForegroundObj:
            if obj.name == "grass":
                obj.change_img('dark_grass.png')
            elif obj.name == "platform":
                obj.change_img('dark_platform.png')
            elif obj.name == "key_platform":
                obj.change_img('dark_platform.png')

def makeLight(objects: list[Obj]) -> None:
    for obj in objects:
        if type(obj) == BackgroundObj:
            if obj.name == "sky":
                obj.change_img('sky.jpg')
            elif obj.name == "sun":
                obj.change_img('sun.png', (255, 255))
                obj.place(15, 15)
            elif obj.img == "dark_cloud1.png":
                obj.change_img('cloud1.png')
            elif obj.img == "dark_cloud2.png":
                obj.change_img('cloud2.png')
            elif obj.img == "dark_cloud3.png":
                obj.change_img('cloud3.png')
            elif obj.img == "dark_cloud4.png":
                obj.change_img('cloud4.png')
        elif type(obj) == ForegroundObj:
            if obj.name == "grass":
                obj.change_img('grass.png')
            elif obj.name == "platform":
                obj.change_img('platform.png')

def mouseInBounds(coords: tuple[int], rect: pygame.rect.Rect) -> bool:
    if coords[0] > rect.left and coords[0] < rect.right:
        if coords[1] < rect.bottom and coords[1] > rect.top:
            return True
    return False

def queueSongs(lst: list[str]) -> None:
    pygame.mixer.music.unload()
    os.chdir('..')
    os.chdir('audio')
    for i, song in enumerate(lst):
        if i == 0:
            pygame.mixer.music.load(song)
        else:
            pygame.mixer.music.queue(song)
    os.chdir('..')
    os.chdir('images')
    pygame.mixer.music.play()