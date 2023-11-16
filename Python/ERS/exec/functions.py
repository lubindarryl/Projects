import pygame
import pygame.display as display
import os
from typing import Any

MUSIC = pygame.USEREVENT + 7


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
        self.surface = pygame.transform.scale(pygame.image.load('bg1.png'), (720, 480))
        self.text = text
        blit_text(self.surface, self.text, (0, 0), font, 'white')
        self.rect = self.surface.get_rect()
        self.rect.center = pos
        self.pos = pos

    def update(self) -> None:
        self.screen.blit(self.surface, self.rect)
    

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


class Card(Obj):
    """
    This class initializes a card that is used in a deck of playing cards
    === Attributes ===
    screen -> The Surface of the game window
    pos -> The position of the Card on the screen
    name -> The name of the card.
    suit -> The suit of the card.
    num -> The number of the card.
    flipped -> Is the card flipped over face up? (If True then the card is displayed face up)

    img -> The image of the card.
    rect -> The in-game physical entity of the card.
    back -> The back of the card.
    back_rect -> The rect object associated with the back attribute.
    moving_* -> Determines if the Card is moving in a certain direction
    speed -> The speed at which an object will move onto the screen
    """

    screen: pygame.Surface
    pos: tuple[int, int]
    name: str
    suit: str
    num: int
    flipped: bool
    img: pygame.surface
    rect: pygame.rect.Rect
    back: pygame.surface
    moving_right: bool
    moving_left: bool
    moving_up: bool
    moving_down: bool
    speed: int
    hide_when_stop: bool

    def __init__(self, screen: pygame.Surface, name: str, suit: str, num: int, img) -> None:
        super().__init__(screen)
        self.name = name
        self.suit = suit
        self.num = num
        self.flipped = False
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.back = pygame.transform.scale(pygame.image.load("back.png"), (50, 73))
        self.pos = (400, 300)
        self.rect.center = self.pos
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.hide_when_stop = False

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'{self.name}'

    def flipCard(self):
        if self.flipped == False:
            self.screen.blit(self.img, self.rect)
            self.flipped = True
        else:
            self.screen.blit(self.back, self.rect)
            self.flipped = False

    def move_right(self) -> None:
        self.moving_right = True
    
    def move_left(self) -> None:
        self.moving_left = True
    
    def move_up(self) -> None:
        self.moving_up = True
    
    def move_down(self) -> None:
        self.moving_down = True
    
    def stop_moving(self, type: str = None) -> None:
        if type:
            if type == 'right':
                self.moving_right = False
            elif type == 'left':
                self.moving_left = False
            elif type == 'up':
                self.moving_up = False
            elif type == 'down':
                self.moving_down = False
        else:
            self.moving_down = False
            self.moving_left = False
            self.moving_up = False
            self.moving_right = False
            self.move_until = None

    def dragTo(self, pos: tuple[int, int], speed: int = 1) -> None:
        self.speed = speed
        if self.pos[1] < pos[1]:
            self.move_down()
            self.move_until = pos
        elif self.pos[1] > pos[1]:
            self.move_up()
            self.move_until = pos
        if self.pos[0] < pos[0]:
            self.move_right()
            self.move_until = pos
        elif self.pos[0] > pos[0]:
            self.move_left()
            self.move_until = pos

    def update(self):
        if self.moving_left:
            self.move(-self.speed, 0)
            if self.pos[0] <= self.move_until[0]:
                self.stop_moving('left')
                if not (self.moving_up or self.moving_down):
                    self.move_until = None
                self.speed = 1
                if self.hide_when_stop:
                    self.hide_when_stop = False
                    self.hide()
        elif self.moving_right:
            self.move(self.speed, 0)
            if self.pos[0] >= self.move_until[0]:
                self.stop_moving('right')
                if not (self.moving_up or self.moving_down):
                    self.move_until = None
                self.speed = 1
                if self.hide_when_stop:
                    self.hide_when_stop = False
                    self.hide()
        if self.moving_up:
            self.move(0, -self.speed)
            if self.pos[1] <= self.move_until[1]:
                self.stop_moving('up')
                if not (self.moving_right or self.moving_left):
                    self.move_until = None
                self.speed = 1
                if self.hide_when_stop:
                    self.hide_when_stop = False
                    self.hide()
        elif self.moving_down:
            self.move(0, self.speed)
            if self.pos[1] >= self.move_until[1]:
                self.stop_moving('down')
                if not (self.moving_right or self.moving_left):
                    self.move_until = None
                self.speed = 1
                if self.hide_when_stop:
                    self.hide_when_stop = False
                    self.hide()

        if self.flipped == False:
            self.screen.blit(self.back, self.rect)
        else:
            self.screen.blit(self.img, self.rect)
    
    def moveCard(self, x: int, y: int, type: str = '', game = None):
        while (self.rect.centerx, self.rect.centery) != (x, y):
            rectx = self.rect.centerx
            recty = self.rect.centery
            x_incr = 1
            y_incr = 1
            
            greater = ''
            if abs(rectx-x) > abs(recty-y):
                greater = 'x'
            elif abs(recty-y) > abs(rectx-x):
                greater = 'y'
            
            if greater == 'x':
                y_incr = abs((recty-y)/(rectx-x))
            elif greater == 'y':
                x_incr = abs((rectx-x)/(recty-y))
            
            x_incr *= 2
            y_incr *= 2

            if rectx-x == abs(rectx-x):
                x_incr *= -1
                if recty-y == abs(recty-y):
                    y_incr *= -1
                    self.move(x_incr, y_incr)
                else:
                    self.move(x_incr, y_incr)
            else:
                if recty-y == abs(recty-y):
                    y_incr *= -1
                    self.move(x_incr, y_incr)
                else:
                    self.move(x_incr, y_incr)
            if game and len(game.pile.cards) > 0:
                if type == 'transfer':
                    try:
                        refresh(self.screen, game.bg, game.objects, game.deck, game.pile, game, '', self, 'transfer')
                    except(TypeError):
                        continue
                else:
                    try:
                        refresh(self.screen, game.bg, game.objects, game.deck, game.pile, game, '', self)
                    except(TypeError):
                        continue
            else:
                refresh(self.screen, game.bg, game.objects, game.deck)
            if type == "play":
                pygame.time.wait(10)
            elif type == "transfer":
                pygame.time.wait(5)
  

class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the first item added is the one that is removed.

    === Public Attributes ===
    lst: The storage of all data added to this class
    """

    lst: list[Card]

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self.lst = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        if len(self.lst) == 0:
            return True
        else:
            return False

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        self.lst.append(item)

    def dequeue(self) -> Card:
        """Remove and return the item at the front of this queue.

        Return None if this Queue is empty.
        (We illustrate a different mechanism for handling an erroneous case.)

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """
        if self.is_empty():
            return None
        else:
            return self.lst.pop(0)


class Hand:
    """
    Used to initialize a Hand object that stores cards for a player
    === Attributes ===
    user -> The name for who the Hand object belongs to
    cards -> A list of cards that are stored inthe Hand object
    x -> The x-coord for the Hand object
    y -> The y-coord for the Hand object
    """

    user: str
    cards: Queue
    x: int
    y: int

    def __init__(self, x: int, y: int, name: str) -> None:
        self.x = x
        self.y = y
        self.cards = Queue()
        self.user = name

    def view(self) -> list[Card]:
        result = []
        new_queue = Queue()
        while not self.cards.is_empty():
            temp = self.cards.dequeue()
            new_queue.enqueue(temp)
            result.append(temp)
        
        while not new_queue.is_empty():
            self.cards.enqueue(new_queue.dequeue())
        
        return result

    def addCard(self, card: Card) -> None:
        self.cards.enqueue(card)
    
    def addCards(self, lst: list[Card]) -> None:
        for c in lst:
            self.cards.enqueue(c)
    
    def clear(self) -> None:
        while not self.cards.is_empty():
            self.cards.dequeue()
    
    def playCard(self, game) -> None:
        temp = self.cards.dequeue()
        game.updateCounter()
        print(f'card: {temp.name} goes from hand: {self.user} at coords: {temp.pos}, to pile at coords: {game.pile.pos()}')
        temp.dragTo(game.pile.pos(), 1)
        game.pile.add(temp)
        temp.flipCard()
        game.updateGame()


class Pile:
    """
    Used to initialize a Pile object that stores cards
    === Attributes ===
    screen -> The Surface of the game window
    game -> The Game object
    cards -> A list of cards that are stored in the Pile object
    x -> The x-coord for the Pile object
    y -> The y-coord for the Pile object
    first -> The card at the beginning of the Pile
    last -> The card at the end of the Pile
    second_last -> The second to last card in the Ppile
    slappable -> A bool that tells if the Pile can be successfully slapped
    """

    screen: pygame.Surface
    cards: list[Card]
    x: int
    y: int
    first: Card
    last: Card
    second_last: Card
    slappable: bool

    def __init__(self, screen: pygame.Surface, x: int, y: int) -> None:
        self.screen = screen
        self.cards = []
        self.x = x
        self.y = y
        self.first = Card
        self.last = Card
        self.second_last = Card
        self.slappable = False
    
    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f'{self.cards}'
    
    def view(self) -> list[Card]:
        return self.cards
    
    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def add(self, card: Card) -> None:
        if len(self.cards) == 0:
            self.first = card
            self.last = card
            self.cards.append(card)
        else:
            self.second_last = self.last
            self.last = card
            self.cards.append(card)

    def clear(self) -> None:
        self.cards = []
    
    def checkSlap(self, type = 'None') -> bool:
        if type == 'None':
            if len(self.cards) == 2:
                if self.first.num == self.last.num: # Double
                    return True
                else:
                    return False
            elif len(self.cards) > 2:
                if self.first.num == self.last.num: # Super Sandwhich
                    return True
                elif self.last.num == self.cards[len(self.cards)-2].num: # Double
                    return True
                elif self.last.num == self.cards[len(self.cards)-3].num: # Sandwhich
                    return True
                else:
                    return False
            else:
                return False
        elif type == 'Double':
            if len(self.cards) == 2:
                if self.first.num == self.last.num:
                    return True
                else:
                    return False
            elif len(self.cards) > 2:
                if self.last.num == self.cards[len(self.cards)-2].num:
                    return True
                else:
                    return False
        elif type == 'Sandwhich':
            if len(self.cards) > 2:
                if self.last.num == self.cards[len(self.cards)-3].num:
                    return True
                else:
                    return False
        elif type == 'Super Sandwhich':
            if len(self.cards) > 2:
                if self.first.num == self.last.num:
                    return True
                else:
                    return False

    def transfer(self, hand: Hand, game) -> None:
        #self.last.moveCard(hand.x, hand.y, 'transfer', game)
        self.last.dragTo((hand.x, hand.y))
        hand.addCards(self.cards)
        if self.last.flipped:
            flipCards(self.cards)
        self.cards.pop(len(self.cards)-1)
        moveCards(self.cards, (hand.x - self.x, hand.y - self.y))
        self.cards = []


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


class Player:
    """
    Initializes a PLayer object that stores each players info for the game
    
    === Attributes ===
    name -> A string used to depict a player from other players
    hand -> Used to reference the hand of the player
    out -> Determines if the player is out of the game or not
    sound -> The Sound it makes when the Player plays a card
    """

    name: str
    hand: Hand
    out: bool
    sound: pygame.mixer.Sound

    def __init__(self, name: str, hand: Hand, sound: pygame.mixer.Sound) -> None:
        self.name = name
        self.hand = hand
        self.out = False
        self.sound = sound
    
    def checkOut(self) -> bool:
        if len(self.hand.cards.lst) == 0:
            self.out = True
        else:
            self.out = False
        return self.out


class Repeat:
    """
    Initializes a Repeat object that repeats for a set amount of times
    
    === Attributes ===
    user -> The player who will collect the cards once the repeating is over
    repeating -> A bool that indicates if the object is repeating
    times -> The remaining amount of times the object will repeat
    """
    user: Player
    repeating: bool
    times: int

    def __init__(self) -> None:
        self.user = None
        self.repeating = False
        self.times = 0

    def get_plr(self) -> Player:
        return self.user

    def set(self, new: int, user) -> None:
        self.user = user
        self.times = new
        self.repeating = True
    
    def decrease(self) -> None:
        self.times -= 1
        if self.times == 0:
            self.repeating = False
    
    def checkRepeat(self) -> bool:
        return self.repeating

    def stop(self) -> None:
        self.user = None
        self.times = 0
        self.repeating = False


class Timer:
    """Initializes a timer that runs in the background of a program
    
    === Attributes ===
    done -> Determine if the timer is finished or not
    """

    done: False

    def __init__(self) -> None:
        self.done = True
    
    def start(self) -> None:
        self.done = False
    
    def finish(self) -> None:
        self.done = True


class Game:
    """
    Initializes a Game object that is used to keep track of the turn based events of the game
    
    === Attributes ===
    started -> Determines if the game has started or not
    timer -> The timer for the game
    players -> A list of all of the players in the game
    previous_player -> The player whose turn it was previously
    current_player -> The player whose turn it is currently is
    next_player -> The player whose next turn it will be
    oppsite_player -> The player whose opposite of the current player
    screen -> The screen of the game
    deck -> The entire deck of cards
    pile -> The pile of cards in the middle
    burn_pile -> The hand in which burned cards go
    buttons -> A list of all of the objects on the screen
    win_state -> Determines if a player is to win a hand
    win_sound -> The Sound it makes when a plr wins a hand
    repeat -> Determines if the game repeats a players turn
    """

    started: bool
    timer: Timer
    players: list[Player]
    previous_player: Player
    current_player: Player
    next_player: Player
    opposite_player: Player
    counters: list[Counter]
    screen: pygame.Surface
    deck: list[Card]
    pile: Pile
    burn_pile: Pile
    objects: list[Obj]
    win_state: bool
    win_sound: pygame.mixer.Sound
    repeat: Repeat

    def __init__(self, timer: Timer, players: list[Player], counters: list[Counter], screen: pygame.Surface, deck: list[Card], pile: Pile, burn_pile: Pile, objects: list[Obj], win_sound: pygame.mixer.Sound, songs: list[str]) -> None:
        self.started = False
        self.timer = timer
        self.players = players
        self.previous_player = players[3]
        self.current_player = players[0]
        self.next_player = players[1]
        self.opposite_player = players[2]
        self.counters = counters
        self.screen = screen
        self.deck = deck
        self.pile = pile
        self.burn_pile = burn_pile
        self.objects = objects
        self.win_state = False
        self.win_sound = win_sound
        self.repeat = Repeat()
        self.jukebox = Jukebox(songs, True)
        os.chdir('..')
        os.chdir('images')
        self.bg = pygame.image.load("woodbg.jpg")
        self.bg = pygame.transform.scale(self.bg, (800, 600))
    
    def menu(self) -> None:
        self.started = False
        hide_objs(self.objects)
        hide_objs(self.deck)
        for obj in self.objects:
            if (type(obj) == Button or type(obj) == Textbox) and (obj.name == "Start" or obj.name == "Options" or obj.name == "Instructions" or obj.name == "Quit" or obj.name == "Title"):
                obj.show()
    
    def options(self) -> None:
        hide_objs(self.objects)
        for obj in self.objects:
            if (type(obj) == Button or type(obj) == Textbox) and (obj.name == "Back" or obj.name == "Options Volume" or obj.name == "Options Volume Slider" or obj.name == "Options Volume Button"):
                obj.show()

    def instructions(self) -> None:
        hide_objs(self.objects)
        condition = True
        for obj in self.objects:
            if (type(obj) == Button or type(obj) == NewTextbox) and (obj.name == "Back" or obj.name == "Instructions Text"):
                obj.show()
            if type(obj) == NewTextbox and obj.name == "Instructions Text":
                condition = False
        if condition:
            txt = "All four players are given an equal portion of the main deck of cards (13 cards for each player). Player 1 (you) starts the game by placing a card from the top of their deck. The next player then places another card from the top of their deck, once a second card is placed, any player can slap the pile in the middle based on certain criteria:\n - Doubles\n   - Same number/face for two cards in a row\n - Sandwhich\n   - Same number/face for two cards with one card in the middle of the two\n   - Super Sandwhich\n   - Same number/face for the card on the bottom of the pile and the top of the pile\nIf a player places one of the following cards, the next player can play an X amount of cards before the previous player can claim all of the cards in the middle:\n - Jack: 1 card\n - Queen: 2 cards\n - King: 3 cards\n - Ace: 4 cards\n Once one player has all 52 cards they have won Egyptian Ratslap!"
            instructions = NewTextbox(self.screen, "Instructions Text", (self.screen.get_width()-150, self.screen.get_height()-150), txt, pygame.font.SysFont('Serif', 21), (400, 350))
            self.objects.append(instructions)

    def start(self) -> None:
        self.current_player = self.players[0]
        self.timer.start()
        self.started = True
        show_objs(self.objects)
        show_objs(self.deck)
        for obj in self.objects:
            if (type(obj) == Button or type(obj) == Textbox or type(obj) == NewTextbox) and (obj.name == "Start" or obj.name == "Options" or obj.name == "Instructions" or obj.name == "Instructions Text" or obj.name == "Options Volume" or obj.name == "Options Volume Slider" or obj.name == "Options Volume Button" or obj.name == "Back" or obj.name == "Quit" or obj.name == "Win" or obj.name == "Title"):
                obj.hide()

    def updateCounter(self) -> None:
        for i, c in enumerate(self.counters):
            c.set_count(len(self.players[i].hand.cards.lst))

    def updateGame(self) -> None:
        for player in self.players:
            player.checkOut()
        self.updateCounter()
        refresh(self.screen, self.bg, self.objects, self.deck, self.pile, self)

    def makeTurn(self, player: Player):
        self.current_player = player
        for i, plr in enumerate(self.players):
            if plr == player:
                if i == 3:
                    self.next_player = self.players[0]
                else:
                    self.next_player = self.players[i + 1]
                if i == 0:
                    self.previous_player = self.players[3]
                else:
                    self.previous_player = self.players[i - 1]
                if i == 0 or i == 1:
                    if i == 0:
                        self.opposite_player = self.players[2]
                    else:
                        self.opposite_player = self.players[3]
                else:
                    self.opposite_player = self.players[i - 2]
        
    def check_next(self):
        if len(self.next_player.hand.cards.lst) == 0:
            if len(self.opposite_player.hand.cards.lst) == 0:
                if len(self.previous_player.hand.cards.lst) == 0:
                    self.makeTurn(self.current_player)
                else:
                    self.makeTurn(self.previous_player)
            else:
                self.makeTurn(self.opposite_player)
        else:
            self.makeTurn(self.next_player)

    def takeTurn(self):
        if self.checkWin():
            self.plrwin(self.checkWin())
        elif len(self.current_player.hand.cards.lst) == 0:
            self.makeTurn(self.next_player)
            if self.current_player != self.players[0]:
                self.takeTurn()
        else:
            self.current_player.sound.play()
            self.current_player.hand.playCard(self)
            if self.pile.last.num >= 11 or self.pile.last.num == 1: # Played a face card
                num = self.pile.last.num
                if num == 11:
                    self.repeat.set(1, self.current_player)
                elif num == 12:
                    self.repeat.set(2, self.current_player)
                elif num == 13:
                    self.repeat.set(3, self.current_player)
                elif num == 1:
                    self.repeat.set(4, self.current_player)
                self.check_next()
            else: # Didn't play a face card
                if self.repeat.checkRepeat():
                    self.repeat.decrease()
                    if not self.repeat.checkRepeat():
                        self.win_state = True
                        self.makeTurn(self.repeat.get_plr())
                else:
                    self.check_next()
    
    def burn_card(self) -> None:
        temp = self.players[0].hand.cards.dequeue()
        self.updateCounter()
        self.burn_pile.add(temp)
        #temp.moveCard(self.burn_pile.x, self.burn_pile.y, 'play', self)
        temp.dragTo(self.burn_pile.pos())

    def check(self) -> bool:
        if self.current_player != self.players[0]:
            if self.win_state:
                self.win(self.current_player)
            self.win_state = False
            print(f"It is {self.current_player.name}'s turn (1)")
            return True
        else:
            if self.win_state:
                self.win(self.current_player)
            elif self.started and len(self.current_player.hand.cards.lst) == 0:
                self.makeTurn(self.next_player)
            self.win_state = False
            print(f"It is {self.current_player.name}'s turn (2)")
            if self.current_player != self.players[0]:
                return True
            return False
        
    def checkWin(self) -> Player | None:
        lst = []
        for plr in self.players:
            if len(plr.hand.cards.lst) > 0:
                lst.append(plr)
        if len(lst) == 1:
            return lst[0]
        else:
            return None

    def win(self, plr: Player) -> None:
        self.repeat.stop()
        self.win_sound.play()
        if len(self.burn_pile.cards) > 0:
            self.burn_pile.transfer(plr.hand, self)
            self.updateCounter()
        self.pile.transfer(plr.hand, self)
        self.updateCounter()
    
    def plrwin(self, plr: Player) -> None:
        self.started = False
        hide_objs(self.objects)
        hide_objs(self.deck)
        for obj in self.objects:
            if type(obj) == Textbox and obj.name == "Win":
                obj.text.set_surface(obj.text.get_txt().render(f'{plr.name} has won Egyptian Ratslap!', True, "white"))
                obj.show()
            elif type(obj) == Button and obj.name == "Exit":
                obj.place(400, 300)

    def over(self) -> bool:
        self.reset()
        self.menu()
    
    def reset(self) -> None:
        self.jukebox.reset()
        self.jukebox.play()
        self.repeat.stop()
        self.timer.finish()
        for plr in self.players:
            plr.hand.clear()
        for card in self.pile.cards:
            card.flipCard()
        for card in self.deck:
            card.stop_moving()
        self.pile.clear()
        placeCards(self.deck, (400, 300))
        for obj in self.objects:
            if type(obj) == Button and obj.name == "Exit":
                obj.place(700, 50)


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

def search(lst: list[pygame.event.Event], item: int) -> bool:
    for x in lst:
        if x.type == item:
            return True
    return False

def searchCard(deck: list[str], name: str) -> str:
    if len(name) == 2:
        for d in deck:
            if d[0:2] == name:
                return d
    else:
        for d in deck:
            if d[0:3] == name:
                return d

def moveCards(deck: list[Card], coord: tuple[int, int]):
    x = coord[0]
    y = coord[1]
    for card in deck:
        card.move(x, y)

def placeCards(deck: list[Card], coord: tuple[int, int]):
    x = coord[0]
    y = coord[1]
    for card in deck:
        card.place(x, y)
        card.pos = (x, y)

def updateCards(deck: list[Card]) -> None:
    for card in deck:
        card.update()

def flipCards(deck: list[Card]):
    for card in deck:
        card.flipCard()

def updateHands(hands: list[Hand]) -> None:
    for h in hands:
        updateCards(h.cards.lst)

def pilerefresh(pile: Pile) -> None:
    try:
        if len(pile.cards) > 1:
            if pile.last.move_until is not None:
                pile.second_last.update()
                pile.last.update()
            else:
                pile.last.update()
        else:
            pile.last.update()
    except(TypeError):
        print("Type Error")
        pass

def refresh(screen: pygame.Surface, bg: pygame.Surface, objects: list[Obj], deck: list[Card], pile: Pile = None, game: Game = None, alert: str = '', card: Card = None, type: str = ''):
    if alert == 'alert':
        print("Alerted!")
    screen.blit(bg, (0, 0))
    for obj in objects:
        obj.update()
    if pile and game:
        hands = []
        for p in game.players:
            hands.append(p.hand)
        updateHands(hands)
        pilerefresh(pile)
        if game.burn_pile:
            if type == 'transfer':
                pilerefresh(game.burn_pile)
            else:
                updateCards(game.burn_pile.cards)
        if card:
            card.update()
    else:
        updateCards(deck)
    display.flip()

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