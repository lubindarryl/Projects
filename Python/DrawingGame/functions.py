import pygame
import pygame.display as display
import os
import sys
from typing import Any
import numpy as np

sys.setrecursionlimit(400000)

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
PENCIL = pygame.USEREVENT + 10
ERASER = pygame.USEREVENT + 11
FILL = pygame.USEREVENT + 12

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
    speed -> The speed at which an object will move on the screen
    """

    name: str
    screen: pygame.Surface
    surface: pygame.Surface
    rect: pygame.Rect
    pos: tuple[int, int]
    visible: bool
    place_on: pygame.Surface | object
    speed: int

    def __init__(self, screen: pygame.Surface, name: str = 'Object') -> None:
        self.name = name
        self.screen = screen
        self.surface = pygame.Surface
        self.rect = pygame.Rect
        self.pos = (0, 0)
        self.visible = True
        self.place_on = screen
        self.speed = 1
    
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
        self.pos = (x, y)
    
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
            self.surface = pygame.image.load('bg1.png')
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
            elif type(obj) == Slider:
                # Bar
                left = self.rect.left + obj.bar.rect.left
                top = self.rect.top + obj.bar.rect.top
                rect = pygame.Rect(left, top, obj.bar.rect.width, obj.bar.rect.height)
                self.screen.blit(obj.bar.surface, rect)
                
                # Button
                left = self.rect.left + obj.button.rect.left
                top = self.rect.top + obj.button.rect.top
                rect = pygame.Rect(left, top, obj.button.rect.width, obj.button.rect.height)
                self.screen.blit(obj.button.surface, rect)
            else:
                print(self.name, obj.name)
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


class Counter(Obj):
    """
    Initializes a Count object used to keep track of the player card count
    
    === Attributes ===
    screen -> The Surface of the game window 
    surface -> The Surface of the Count object
    text -> The Text of the Count object
    rect -> The Rect of the Count object
    count -> The number displayed on the Count object
    x -> The x-coord of the Count object
    y -> The y-coord of the Count object
    pos -> The position of the Count object
    """

    screen: pygame.Surface
    surface: pygame.Surface
    text: Text
    rect: pygame.rect.Rect
    count: int
    x: int
    y: int
    pos: tuple[int, int]

    def __init__(self, screen: pygame.Surface, side: str) -> None:
        super().__init__(screen)
        self.count = 0
        self.text = pygame.font.Font(None, 25)
        self.surface = self.text.render(str(self.count), True, (255, 255, 255))
        self.text = Text(self.text, self.surface)
        self.rect = self.text.surface.get_rect()
        self.place(400, 300)
        if side == "top":
            self.move(0, -200)
            self.pos = self.rect.center
        elif side == "right":
            self.move(200, 0)
            self.pos = self.rect.center
        elif side == "left":
            self.move(-200, 0)
            self.pos = self.rect.center
        elif side == "bottom":
            self.move(0, 200)
            self.pos = self.rect.center
    
    def get_surface(self) -> pygame.Surface:
        return self.surface
    
    def get_rect(self) -> pygame.Rect:
        return self.rect

    def set_count(self, set: int) -> None:
        self.count = set
        self.surface = self.text.get_txt().render(str(self.count), True, (255, 255, 255))


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


class NewTextbox(Obj):
    """
    === Attributes ===
    screen -> The surface of the window screen
    surface -> The surface of the textbox
    text -> The text of the textbox
    rect -> The rect of the surface
    """
    def __init__(self, screen: pygame.Surface, name: str, size: tuple[int, int], text: str, font: pygame.font.Font, pos: tuple[int, int]) -> None:
        super().__init__(screen)
        self.screen = screen
        self.name = name
        self.surface = pygame.transform.scale(pygame.image.load('bg1.png'), size)
        self.text = text
        blit_text(self.surface, self.text, (0, 0), font, 'white')
        self.rect = self.surface.get_rect()
        self.rect.center = pos
        self.pos = pos

    def update(self) -> None:
        self.screen.blit(self.surface, self.rect)
    

class Image(Obj):
    """
    Initializes an Image object
    
    === Attributes ===
    *Obj Attributes
    """
    def __init__(self, screen: pygame.Surface, name: str, img: str, size: tuple[int, int], pos: tuple[int, int]) -> None:
        super().__init__(screen, name)
        self.surface = pygame.transform.scale(pygame.image.load(img), size)
        self.rect = self.surface.get_rect()
        self.rect.center = pos
        self.size = size
        self.pos = pos


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
    pressed -> Determines if the button has been pressed or not
    event -> The event that triggers from pressing the button
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
    pressed: bool
    event: pygame.event.Event
    selected: bool

    def __init__(self, screen: pygame.Surface, name: str, img: str, hover_img: str, press_img: str, size: tuple[int, int], pos: tuple[int, int], event: int = None, text: pygame.font.Font = None) -> None:
        super().__init__(screen)
        self.name = name
        self.size = size
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, self.size)
        self.hover_img = pygame.image.load(hover_img)
        self.hover_img = pygame.transform.scale(self.hover_img, self.size)
        self.press_img = pygame.image.load(press_img)
        self.press_img = pygame.transform.scale(self.press_img, self.size)
        self.surface = self.img
        self.place_on = self.screen
        self.rect = self.surface.get_rect()
        if text:
            self.txt = name
            self.text = Text(text, text.render(self.txt, True, "black"))
            self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))
        else:
            self.text = None
            self.text_rect = None
        self.pos = pos
        self.rect.center = pos
        self.pressed = False
        if event:
            self.event = pygame.event.Event(event)
        else:
            self.event = None
        self.selected = False

    def fix_text(self) -> None:
        self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))

    def default(self) -> None:
        self.pressed = False
        self.selected = False
        self.surface = self.img
        if self.text:
            self.change_text_color('black')

    def hover(self, override: bool = False) -> None:
        if (not self.surface == self.press_img) or override:
            self.pressed = False
            self.surface = self.hover_img
            if self.text:
                self.change_text_color('white')

    def press(self) -> None:
        self.pressed = True
        self.surface = self.press_img

    def select(self) -> None:
        self.selected = True
        self.surface = self.press_img

    def update(self, ev: list[pygame.event.Event]) -> None:
        if not self.selected:
            if self.checkMouse(pygame.mouse):
                self.hover()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        self.press()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.pressed:
                            if self.event:
                                pygame.event.post(self.event)
                        self.hover(True)
            else:
                self.default()
        super().update()
        if self.text:
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
        self.txt = new_text
        self.text.set_surface(self.text.get_txt().render(self.txt, True, color))

    def change_text_color(self, color: str) -> None:
        if color == "empty":
            self.text.set_surface(self.text.get_txt().render('', True, (0, 0, 0, 0)))
        else:
            self.text.set_surface(self.text.get_txt().render(self.txt, True, color))


class Slider(Obj):
    """
    Initializes a slider object
    
    === Attributes ===
    *Obj Attributes
    bar -> The Image object of the bar for the slider
    button -> The Button object for the slider
    orientation -> Determines if the slider is vertical or horizontal
    """
    bar: Image
    button: Button
    orientation: str

    def __init__(self, screen: pygame.Surface, name: str, slider_size: tuple[int, int], slider_pos: tuple[int, int], button_size: tuple[int, int], button_pos: tuple[int, int], vertical = False) -> None:
        super().__init__(screen, name)
        if vertical:
            self.orientation = 'vertical'
            self.bar = Image(screen, 'volume slider', 'vert_slider_bar.png', slider_size, slider_pos)
        else:
            self.orientation = 'horizontal'
            self.bar = Image(screen, 'volume slider', 'slider_bar.png', slider_size, slider_pos)
        self.button = Button(screen, 'volume button', 'small_button.png', 'small_button_hovered.png', 'small_button_pressed.png', button_size, button_pos)
    
    def update(self, ev: list[pygame.event.Event]) -> None:
        mouse = pygame.mouse
        if self.bar.checkMouse(mouse):
            if mouse.get_pressed()[0]:
                if self.orientation == 'vertical':
                    self.button.rect.centery = mouse.get_pos()[1]
                else:
                    self.button.rect.centerx = mouse.get_pos()[0]
        self.bar.update()
        self.button.update(ev)


class Point:
    def __init__(self, size: tuple[int, int], color: tuple[int, int, int], layer: int = 0, blank: bool = False, eraser: bool = False) -> None:
        self.size = size
        self.color = color
        self.layer = layer
        self.blank = blank
        self.eraser = eraser
        self.surface = pygame.Surface(size)
        self.surface.fill(color)


class Pic:
    """
    Initializes a Pic object that stores information on a 2D plane
    
    === Attributes ===
    size -> The size of the Pic object
    data -> The array that represents all data points on the object
    """

    size: tuple[int, int]
    data: np.ndarray[Point]
    surface: pygame.Surface

    def __init__(self, size: tuple[int, int], eraser: bool = False) -> None:
        self.size = size
        self.data = np.full(size, Point((1, 1), (255, 255, 255), 0, True))
        self.surface = pygame.Surface(size)
        self.surface.fill("white")
        self.eraser = eraser

    def check(self, pos: tuple[int, int]) -> Point:
        return self.data[pos[0]][pos[1]]

    def update(self, pos: tuple[int, int], new_data: Point) -> None:
        self.data[pos[0]][pos[1]] = new_data
    
    def clone(self) -> Any:
        new_Pic = Pic(self.size, self.eraser)
        new_Pic.surface.blit(self.surface, (0, 0))
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                new_Pic.update((r,c), self.check((r,c)))
        return new_Pic


class Canvas(Obj):
    """
    Initializes a Canvas object that is used to store drawing inputs
    
    === Attributes ===
    *Obj Attributes
    """

    brush_color: tuple[int, int, int]
    brush_size: tuple[int, int]
    history: list[Pic]
    current: Pic
    current_index: int
    filling: bool

    def __init__(self, screen: pygame.Surface, name: str, size: tuple[int, int], pos: tuple[int, int]) -> None:
        super().__init__(screen, name)
        self.surface = pygame.Surface(size)
        self.surface.fill('white')
        self.rect = self.surface.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.size = size
        self.focus = False
        self.tool = 'pencil'
        self.brush_color = (0, 0, 0)
        self.brush_size = (1, 1)
        self.current = Pic(size)
        self.current_index = 0
        self.history = [Pic(size)]
        self.filling = False
    
    def draw(self, pos: tuple[int, int]) -> None:
        point = Point(self.brush_size, self.brush_color, self.current_index)
        self.surface.blit(point.surface, (pos[0]-self.brush_size[0]*0.5, pos[1]-self.brush_size[1]*0.5))
        self.current.eraser = False
        self.current.update(pos, point)
    
    def erase(self, pos: tuple[int, int]) -> None:
        point = Point(self.brush_size, (255, 255, 255), self.current_index, False, True)
        self.surface.blit(point.surface, (pos[0]-self.brush_size[0]*0.5, pos[1]-self.brush_size[1]*0.5))
        self.current.eraser = True
        self.current.update(pos, point)

    def check_fill(self, pos: tuple[int, int], check_color: tuple[int, int]) -> bool:
        if inBoundsPic(pos, self.current):
            r,g,b,alpha = self.surface.get_at(pos)
            curr_color = (r, g, b)
            if curr_color == check_color:
                return True
        return False

    def fill(self, pos: tuple[int, int], new_color: tuple[int, int, int], check_color: tuple[int, int, int]) -> None:
        new_color = (int(new_color[0]), int(new_color[1]), int(new_color[2]))
        point = Point((1, 1), new_color, self.current_index, False, True)
        current_pic = self.current
        if inBoundsPic(pos, current_pic):
            #curr_color = current_pic.check(pos).color
            r,g,b,alpha = self.surface.get_at(pos)
            curr_color = (r, g, b)
            if curr_color != new_color:
                if curr_color == check_color:
                    self.surface.blit(point.surface, pos)
                    self.current.eraser = False
                    self.current.update(pos, point)

                    if self.check_fill((pos[0]+1, pos[1]), check_color):
                        self.fill((pos[0]+1, pos[1]), new_color, check_color)
                    
                    if self.check_fill((pos[0]-1, pos[1]), check_color):
                        self.fill((pos[0]-1, pos[1]), new_color, check_color)
                    
                    if self.check_fill((pos[0], pos[1]+1), check_color):
                        self.fill((pos[0], pos[1]+1), new_color, check_color)
                    
                    if self.check_fill((pos[0], pos[1]-1), check_color):
                        self.fill((pos[0], pos[1]-1), new_color, check_color)

    def change_color(self, color: tuple[int, int, int]) -> None:
        self.brush_color = color
    
    def update(self, ev: list[pygame.event.Event]) -> None:
        if self.checkMouse(pygame.mouse):
            if self.place_on != pygame.Surface:
                x = pygame.mouse.get_pos()[0] - self.place_on.rect.left - self.rect.left
                y = pygame.mouse.get_pos()[1] - self.place_on.rect.top - self.rect.top
            else:
                x = pygame.mouse.get_pos()[0] - self.rect.left
                y = pygame.mouse.get_pos()[1] - self.rect.top
            if pygame.mouse.get_pressed()[0]:
                if not pygame.mouse.get_pressed()[1]:
                    self.focus = True
                else:
                    self.focus = False
                if self.tool == 'pencil':
                    self.draw((x, y))
                elif self.tool == 'eraser':
                    self.erase((x, y))
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP and self.focus and not pygame.mouse.get_pressed()[0]:
                if self.tool == 'fill' and not self.filling:
                    self.filling = True
                    r,g,b,alpha = self.surface.get_at((x, y))
                    print("Filling")
                    self.fill((x, y), self.brush_color, (r, g, b))
                    self.filling = False
                if self.focus:
                    self.focus = False
                    if self.checkMouse(pygame.mouse):
                        self.current.surface.blit(self.surface, (0, 0))
                        if self.current_index < len(self.history) - 1:
                            count = 0
                            for i,v in enumerate(self.history):
                                if i > self.current_index:
                                    count += 1
                            for i in range(count):
                                self.history.pop()
                            self.history.append(self.current)
                            self.current_index += 1
                            self.current = self.current.clone()
                        elif self.current_index == len(self.history) - 1:
                            self.history.append(self.current)
                            self.current_index += 1
                            self.current = self.current.clone()
            elif event.type == CLEAR:
                self.surface.fill('white')
                self.history = [Pic(self.size)]
                self.current = Pic(self.size)
                self.current_index = 0
            elif event.type == INCRSIZE:
                self.brush_size = (self.brush_size[0] + 1, self.brush_size[1] + 1)
            elif event.type == DECSIZE:
                if not self.brush_size == (0, 0):
                    self.brush_size = (self.brush_size[0] - 1, self.brush_size[1] - 1)
            elif event.type == UNDO:
                if self.current_index > 0:
                    self.current_index -= 1
                    self.current = self.history[self.current_index].clone()
                    self.surface = self.current.surface
                    """self.surface.fill('white')
                    for i in range(len(self.history)):
                        for r in range(self.current.size[0]):
                            for c in range(self.current.size[1]):
                                if not self.current.check((r, c)).blank:
                                    point = self.current.check((r, c))
                                    if point.layer == i:
                                        self.surface.blit(point.surface, (r-point.surface.get_width()*0.5, c-point.surface.get_height()*0.5))"""
                    
            elif event.type == REDO:
                if self.current_index < len(self.history) - 1:
                    self.current_index += 1
                    self.current = self.history[self.current_index].clone()
                    self.surface = self.current.surface
                    """for i in range(len(self.history)):
                        for r in range(self.current.size[0]):
                            for c in range(self.current.size[1]):
                                if not self.current.check((r, c)).blank:
                                    point = self.current.check((r, c))
                                    if point.layer == i:
                                        self.surface.blit(point.surface, (r-point.surface.get_width()*0.5, c-point.surface.get_height()*0.5))"""
                    
            elif event.type == PENCIL:
                self.tool = 'pencil'
            elif event.type == ERASER:
                self.tool = 'eraser'
            elif event.type == FILL:
                self.tool = 'fill'
        super().update()


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
        os.chdir('sounds')
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
    
    def reset(self) -> None:
        self.current_index = 0


class Game:
    """
    Initializes a Game object

    === Attributes ===
    screen -> The surface of the window screen
    bg -> The background of the game Obj
    objects -> The list on-screen objects
    """
    def __init__(self, screen: pygame.Surface, bg: pygame.Surface, objects: list[Obj]) -> None:
        self.screen = screen
        self.bg = bg
        self.objects = objects

    def checkInput(self, ev: list[pygame.event.Event]) -> None:
        for event in ev:
            if event.type == PLAY:
                self.start()
            elif event.type == OPTIONS:
                self.options()
            elif event.type == MENU:
                self.menu()
            elif event.type == PENCIL or event.type == ERASER or event.type == FILL:
                fill = searchFor(self.objects, "fill button")
                eraser = searchFor(self.objects, "eraser button")
                pencil = searchFor(self.objects, "pencil button")
                if event.type == PENCIL:
                    eraser.default()
                    fill.default()
                    pencil.select()
                elif event.type == ERASER:
                    pencil.default()
                    fill.default()
                    eraser.select()
                elif event.type == FILL:
                    pencil.default()
                    eraser.default()
                    fill.select()
        
        if searchFor(self.objects, 'size display'):
            canvas = searchFor(self.objects, 'canvas')
            display = searchFor(self.objects, 'size display')
            display.surface.fill('white')
            point = Point(canvas.brush_size, canvas.brush_color)
            display.surface.blit(point.surface, (display.rect.width/2-canvas.brush_size[0]*0.5, display.rect.height/2-canvas.brush_size[1]*0.5))

        if checkSlider(self.objects, 'volume slider'):
            ratio = checkSlider(self.objects, 'volume slider')
            pygame.mixer.music.set_volume(ratio)
        
        if checkSlider(self.objects, 'red slider'):
            ratio = checkSlider(self.objects, 'red slider')
            canvas = searchFor(self.objects, 'canvas')
            display = searchFor(self.objects, 'display')
            color = (255*ratio, canvas.brush_color[1], canvas.brush_color[2])
            display.surface.fill(color)
            canvas.change_color(color)
        
        if checkSlider(self.objects, 'green slider'):
            ratio = checkSlider(self.objects, 'green slider')
            canvas = searchFor(self.objects, 'canvas')
            display = searchFor(self.objects, 'display')
            color = (canvas.brush_color[0], 255*ratio, canvas.brush_color[2])
            display.surface.fill(color)
            canvas.change_color(color)
        
        if checkSlider(self.objects, 'blue slider'):
            ratio = checkSlider(self.objects, 'blue slider')
            canvas = searchFor(self.objects, 'canvas')
            display = searchFor(self.objects, 'display')
            color = (canvas.brush_color[0], canvas.brush_color[1], 255*ratio)
            display.surface.fill(color)
            canvas.change_color(color)
                
    def menu(self) -> None:
        self.clear()
        play_button = Button(self.screen, 'play button', 'button.png', 'button_hovered.png', 'button_pressed.png', (100, 40), (500, 300), PLAY, pygame.font.SysFont('Verdana', 18, True))
        play_button.change_text('Play', 'black')
        self.objects.append(play_button)
        
        options_button = Button(self.screen, 'options button', 'button.png', 'button_hovered.png', 'button_pressed.png', (100, 40), (500, 500), OPTIONS, pygame.font.SysFont('Verdana', 18, True))
        options_button.change_text('Options', 'black')
        self.objects.append(options_button)
        
    def start(self) -> None:
        self.clear()
        back_button = Button(self.screen, 'back button', 'button.png', 'button_hovered.png', 'button_pressed.png', (100, 40), (60, 30), MENU, pygame.font.SysFont('Verdana', 18, True))
        back_button.change_text('Back', 'black')
        self.objects.append(back_button)

        border = Image(self.screen, 'border', 'border.png', (465, 365), (500, 400))
        self.objects.append(border)

        canvas = Canvas(self.screen, 'canvas', (400, 300), (border.size[0]/2, border.size[1]/2))
        canvas.place_onto(border)
        self.objects.append(canvas)

        rgb_frame = Frame(self.screen, 'rgb', (100, 300), (125, 400))

        r = Textbox(self.screen, 'r', (5, 5), pygame.font.SysFont('Verdana', 12, True), 'center', (rgb_frame.rect.left + rgb_frame.rect.width*1/4, rgb_frame.rect.top + 25))
        r.change_text('R', 'white')
        r_slider = Slider(self.screen, 'red slider', (20, 100), (rgb_frame.rect.left + rgb_frame.rect.width*1/4, rgb_frame.rect.top + rgb_frame.rect.height*1/3), (20, 20), (rgb_frame.rect.left + rgb_frame.rect.width*1/4, (rgb_frame.rect.top + rgb_frame.rect.height*1/3)+50), True)

        self.objects.append(r)
        self.objects.append(r_slider)

        g = Textbox(self.screen, 'g', (5, 5), pygame.font.SysFont('Verdana', 12, True), 'center', (rgb_frame.rect.left + rgb_frame.rect.width*2/4, rgb_frame.rect.top + 25))
        g.change_text('G', 'white')
        g_slider = Slider(self.screen, 'green slider', (20, 100), (rgb_frame.rect.left + rgb_frame.rect.width*2/4, rgb_frame.rect.top + rgb_frame.rect.height*1/3), (20, 20), (rgb_frame.rect.left + rgb_frame.rect.width*2/4, (rgb_frame.rect.top + rgb_frame.rect.height*1/3)+50), True)

        self.objects.append(g)
        self.objects.append(g_slider)
        
        b = Textbox(self.screen, 'b', (5, 5), pygame.font.SysFont('Verdana', 12, True), 'center', (rgb_frame.rect.left + rgb_frame.rect.width*3/4, rgb_frame.rect.top + 25))
        b.change_text('B', 'white')
        b_slider = Slider(self.screen, 'blue slider', (20, 100), (rgb_frame.rect.left + rgb_frame.rect.width*3/4, rgb_frame.rect.top + rgb_frame.rect.height*1/3), (20, 20), (rgb_frame.rect.left + rgb_frame.rect.width*3/4, (rgb_frame.rect.top + rgb_frame.rect.height*1/3)+50), True)

        self.objects.append(b)
        self.objects.append(b_slider)

        pencil_button = Button(self.screen, 'pencil button', 'small_button.png', 'small_button_hovered.png', 'small_button_pressed.png', (40, 40), (450, 700), PENCIL)
        pencil_image = Image(self.screen, 'pencil image', 'pencil.png', (30, 30), (20, 20))
        pencil_button.select()
        pencil_image.place_onto(pencil_button)
        self.objects.append(pencil_image)
        self.objects.append(pencil_button)

        fill_button = Button(self.screen, 'fill button', 'small_button.png', 'small_button_hovered.png', 'small_button_pressed.png', (40, 40), (500, 700), FILL)
        fill_image = Image(self.screen, 'fill image', 'bucket.png', (30, 30), (20, 20))
        fill_image.place_onto(fill_button)
        self.objects.append(fill_image)
        self.objects.append(fill_button)

        eraser_button = Button(self.screen, 'eraser button', 'small_button.png', 'small_button_hovered.png', 'small_button_pressed.png', (40, 40), (550, 700), ERASER)
        eraser_image = Image(self.screen, 'eraser image', 'eraser.png', (30, 30), (20, 20))
        eraser_image.place_onto(eraser_button)
        self.objects.append(eraser_image)
        self.objects.append(eraser_button)

        color_display = Image(self.screen, 'display', 'bg1.png', (25, 25), (g.rect.centerx, g.rect.top - 25))
        color_display.surface.fill('black')
        self.objects.append(color_display)

        clear_button = Button(self.screen, 'back button', 'button.png', 'button_hovered.png', 'button_pressed.png', (100, 40), (500, 650), CLEAR, pygame.font.SysFont('Verdana', 18, True))
        clear_button.change_text('Clear', 'black')
        self.objects.append(clear_button)

        incr_size_button = Button(self.screen, 'size button', 'small_button.png', 'small_button_hovered.png', 'small_button_pressed.png', (40, 40), (775, 350), INCRSIZE, pygame.font.SysFont('Verdana', 18, True))
        incr_size_button.change_text('+', 'black')
        self.objects.append(incr_size_button)

        dec_size_button = Button(self.screen, 'size button', 'small_button.png', 'small_button_hovered.png', 'small_button_pressed.png', (40, 40), (775, 450), DECSIZE, pygame.font.SysFont('Verdana', 18, True))
        dec_size_button.change_text('-', 'black')
        self.objects.append(dec_size_button)

        size_display = Image(self.screen, 'size display', 'bg1.png', (50, 50), (500, 150))
        size_display.surface.fill('white')
        self.objects.append(size_display)

        undo_button = Button(self.screen, 'undo button', 'button.png', 'button_hovered.png', 'button_pressed.png', (50, 20), (400, 650), UNDO, pygame.font.SysFont('Verdana', 15, True))
        undo_button.change_text('undo', 'black')
        self.objects.append(undo_button)

        redo_button = Button(self.screen, 'redo button', 'button.png', 'button_hovered.png', 'button_pressed.png', (50, 20), (600, 650), REDO, pygame.font.SysFont('Verdana', 15, True))
        redo_button.change_text('redo', 'black')
        self.objects.append(redo_button)


    def options(self) -> None:
        self.clear()
        back_button = Button(self.screen, 'back button', 'button.png', 'button_hovered.png', 'button_pressed.png', (100, 40), (60, 30), MENU, pygame.font.SysFont('Verdana', 18, True))
        back_button.change_text('Back', 'black')
        self.objects.append(back_button)

        # Background Options

        slider = Slider(self.screen, 'slider', (100, 20), (666, 300), (20, 20), (666, 300))
        self.objects.append(slider)

        # Volume options
        volume_textbox = NewTextbox(self.screen, 'volume textbox', (300, 50), 'Background Volume:', pygame.font.SysFont('Verdana', 25, True), (333, 200))
        self.objects.append(volume_textbox)

        volume_slider = Slider(self.screen, 'volume slider', (100, 20), (666, 200), (20, 20), (616 + pygame.mixer.music.get_volume()*100, 200))
        self.objects.append(volume_slider)
        

    def clear(self) -> None:
        self.objects = []

    def update(self, ev: list[pygame.event.Event]) -> None:
        refresh(self.screen, self.bg, self.objects, ev)


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

def refresh(screen: pygame.Surface, bg: pygame.Surface, objects: list[Obj], ev: list[pygame.event.Event], alert: str = ''):
    if alert == 'alert':
        print("Alerted!")
    screen.blit(bg, (0, 0))
    for obj in objects:
        if type(obj) == Button or type(obj) == Canvas or type(obj) == Slider:
            obj.update(ev)
        else:
            obj.update()
    display.flip()

def inBounds(pos: tuple[int, int], rect: pygame.rect.Rect) -> bool: 
    if pos[0] > rect.left and pos[0] < rect.right:
        if pos[1] < rect.bottom and pos[1] > rect.top:
            return True
    return False

def inBoundsPic(pos: tuple[int, int], pic: Pic) -> bool:
    if pos[0] >= 0 and pos[0] < pic.size[0]:
        if pos[1] >= 0 and pos[1] < pic.size[1]:
            return True
    return False

def mouseInBounds(coords: tuple[int], rect: pygame.rect.Rect) -> bool: 
    if coords[0] > rect.left and coords[0] < rect.right:
        if coords[1] < rect.bottom and coords[1] > rect.top:
            return True
    return False

def hide_objs(lst: list[Obj]) -> None:
    for obj in lst:
        obj.hide()
    
def show_objs(lst: list[Obj]) -> None:
    for obj in lst:
        obj.show()

def blit_text(surface: pygame.Surface, text: str, pos: tuple[int, int], font: pygame.font.Font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def checkSlider(objects: list[Obj], slider_name: str) -> float | None:
    slider = searchFor(objects, slider_name)
    if slider:
        mouse = pygame.mouse
        if slider.bar.checkMouse(mouse):
            if mouse.get_pressed()[0]:
                if slider.orientation == 'vertical':
                    ratio = 1 - (mouse.get_pos()[1] - slider.bar.rect.top)/slider.bar.rect.height
                    return ratio
                else:
                    ratio = (mouse.get_pos()[0] - slider.bar.rect.left)/slider.bar.rect.width
                    return ratio
    return None