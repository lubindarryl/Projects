import asyncio
import os, pygame, sys
import pygame.display as display
import time
import random

from typing import Any

os.chdir('images')

pygame.init()

size = width, height = 800, 600

screen = display.set_mode(size)
bg = pygame.image.load("woodbg.jpg")
bg = pygame.transform.scale(bg, (800, 600))
color = (100, 200, 100)
empty = (0, 0, 0, 0)

async def main():

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
        """

        name: str
        screen: pygame.Surface
        surface: pygame.Surface
        rect: pygame.Rect
        pos: tuple[int, int]
        visible: bool

        def __init__(self, screen: pygame.Surface, name: str = 'Object') -> None:
            self.name = name
            self.screen = screen
            self.surface = pygame.Surface
            self.rect = pygame.Rect
            self.pos = (0, 0)
            self.visible = True
        
        def hide(self) -> None:
            print(f'Hid: {self.name}')
            self.rect.update(-10000, -10000, self.rect.width, self.rect.height)
            self.visible = False
        
        def show(self) -> None:
            print(f'Showed: {self.name}')
            self.rect.center = self.pos
            self.visible = True
        
        def move(self, x: int, y: int) -> None:
            self.rect.move_ip((x, y))
            self.pos = (self.rect.centerx, self.rect.centery)
        
        def place(self, x: int, y: int) -> None:
            self.rect.center = (x, y)
            self.pos = (self.rect.centerx, self.rect.centery)
        
        def update(self) -> None:
            self.screen.blit(self.surface, self.rect)


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

        def update(self):
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
                            refresh(self.screen, bg, game.objects, game.deck, game.pile, game, '', self, 'transfer')
                        except(TypeError):
                            continue
                    else:
                        try:
                            refresh(self.screen, bg, game.objects, game.deck, game.pile, game, '', self)
                        except(TypeError):
                            continue
                else:
                    refresh(self.screen, bg, game.objects, game.deck)
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
            print(f'card: {temp.name} goes from hand: {self.user}, to pile at coords: {game.pile.pos()}')
            temp.moveCard(game.pile.pos()[0], game.pile.pos()[1], "play", game)
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
        slappable -> A bool that tells if the Pile can be successfully slapped
        """

        screen: pygame.Surface
        cards: list[Card]
        x: int
        y: int
        first: Card
        last: Card
        slappable: bool

        def __init__(self, screen: pygame.Surface, x: int, y: int) -> None:
            self.screen = screen
            self.cards = []
            self.x = x
            self.y = y
            self.first = Card
            self.last = Card
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
                self.last = card
                self.cards.append(card)

        def clear(self) -> None:
            self.cards = []
        
        def checkSlap(self) -> bool:
            if len(self.cards) == 2:
                if self.first.num == self.last.num:
                    self.slappable = True
                else:
                    self.slappable = False
            elif len(self.cards) > 2:
                if self.first.num == self.last.num:
                    self.slappable = True
                elif self.last.num == self.cards[len(self.cards)-2].num:
                    self.slappable = True
                elif self.last.num == self.cards[len(self.cards)-3].num:
                    self.slappable = True
                else:
                    self.slappable = False
            else:
                self.slappable = False
            return self.slappable

        def transfer(self, hand: Hand, game) -> None:
            self.last.moveCard(hand.x, hand.y, 'transfer', game)
            hand.addCards(self.cards)
            if self.last.flipped:
                flipCards(self.cards)
            self.cards.pop(len(self.cards)-1)
            moveCards(self.cards, (hand.x - self.x, hand.y - self.y))
            self.cards = []


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


    class Button(Obj):
        """
        Initiatlizes a button
        
        === Attributes ===
        screen -> The Surface of the game window
        name -> The name of the Button
        size -> The size of the Button
        surface -> The surface of the Button
        rect -> The Rect of the surface of the Button
        text -> The text of the Button
        text_rect -> The Rect of the Text object
        pos -> The position of the Button
        """

        screen: pygame.Surface
        name: str
        size: tuple[int, int]
        surface: pygame.Surface
        rect: pygame.Rect
        text: Text
        text_rect: tuple[int, int]
        pos: tuple[int, int]

        def __init__(self, screen: pygame.Surface, name: str, img: str, size: tuple[int, int], text: pygame.font.Font, pos: tuple[int, int]) -> None:
            super().__init__(screen)
            self.name = name
            self.size = size
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

        def checkMouse(self, mouse: pygame.mouse) -> bool:
            return mouseInBounds(mouse.get_pos(), self.rect)
        
        def change_text_color(self, color: str) -> None:
            if color == "empty":
                self.text.set_surface(self.text.get_txt().render('', True, (0, 0, 0, 0)))
            else:
                self.text.set_surface(self.text.get_txt().render(self.name, True, color))
            

    class Textbox(Obj):
        """
        Initializes a Textbox object that stores text and displays it on a screen
        
        === Attributes ===
        screen -> The Surface of the game window
        name -> The name of the Textbox
        size -> The size of the Textbox
        surface -> The optional background img of the Textbox
        rect -> The rect of the surface of the Textbox
        text -> The Text of the Textbox
        text_rect -> The Rect of the Text object
        alignment -> Where the text is inside of the box
        pos -> The position of the Textbox
        """

        screen: pygame.Surface
        name: str
        size: tuple[int, int]
        surface: pygame.Surface
        rect: pygame.Rect
        text: Text
        text_rect: tuple[int, int]
        alignment: str
        pos: tuple[int, int]

        def __init__(self, screen: pygame.Surface, name: str, size: tuple[int, int], text: pygame.font.Font, align: str, pos: tuple[int, int], img: str = None) -> None:
            super().__init__(screen)
            self.name = name
            self.size = size
            if img:
                self.surface = pygame.image.load(img)
                self.surface = pygame.transform.scale(self.surface, self.size)
            else:
                self.surface = None
            self.text = Text(text, pygame.transform.scale(text.render(name, True, "white"), self.size))
            self.rect = self.text.get_surface().get_rect()
            self.rect.center = pos
            self.pos = self.rect.center
            self.alignment = align
            if align == "top":
                self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top))
            elif align == "center":
                self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))
            elif align == "bottom":
                self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.bottom))
        
        def fix_text(self) -> None:
            if self.alignment == "top":
                self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top))
            elif self.alignment == "topcenter":
                self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/4))
            elif self.alignment == "center":
                self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.top+(self.rect.height - self.text.get_surface().get_height())/2))
            elif self.alignment == "bottom":
                self.text_rect = ((self.rect.left+(self.rect.width - self.text.get_surface().get_width())/2), (self.rect.bottom))
        
        def update(self) -> None:
            self.fix_text()
            if self.surface:
                self.screen.blit(self.surface, self.rect)
            self.screen.blit(self.text.get_surface(), self.text_rect)
        
        def change_text(self, new_text: str, color: str) -> None:
            self.text.set_surface(self.text.get_txt().render(new_text, True, color))


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


    class Game:
        """
        Initializes a Game object that is used to keep track of the turn based events of the game
        
        === Attributes ===
        started -> Determines if the game has started or not
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

        def __init__(self, players: list[Player], counters: list[Counter], screen: pygame.Surface, deck: list[Card], pile: Pile, burn_pile: Pile, objects: list[Obj], win_sound: pygame.mixer.Sound) -> None:
            self.started = False
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
        
        def menu(self) -> None:
            self.started = False
            hide_objs(self.objects)
            hide_objs(self.deck)
            for obj in self.objects:
                if (type(obj) == Button or type(obj) == Textbox) and (obj.name == "Start" or obj.name == "Options" or obj.name == "Quit" or obj.name == "Title"):
                    obj.show()

        def start(self) -> None:
            self.started = True
            show_objs(self.objects)
            show_objs(self.deck)
            for obj in self.objects:
                if (type(obj) == Button or type(obj) == Textbox) and (obj.name == "Start" or obj.name == "Options" or obj.name == "Quit" or obj.name == "Win" or obj.name == "Title"):
                    obj.hide()

        def updateCounter(self) -> None:
            for i, c in enumerate(self.counters):
                c.set_count(len(self.players[i].hand.cards.lst))

        def updateGame(self) -> None:
            for player in self.players:
                player.checkOut()
            self.updateCounter()
            refresh(self.screen, bg, self.objects, self.deck, self.pile, self)

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
                    self.makeTurn(self.next_player)
                else: # Didn't play a face card
                    if self.repeat.checkRepeat():
                        self.repeat.decrease()
                        if not self.repeat.checkRepeat():
                            self.win_state = True
                            self.makeTurn(self.repeat.get_plr())
                    else:
                        self.makeTurn(self.next_player)
        
        def burn_card(self) -> None:
            temp = self.players[0].hand.cards.dequeue()
            self.updateCounter()
            self.burn_pile.add(temp)
            temp.moveCard(self.burn_pile.x, self.burn_pile.y, 'play', self)

        def check(self) -> bool:
            if self.current_player != self.players[0]:
                if self.win_state:
                    self.win(self.current_player)
                self.win_state = False
                self.takeTurn()
                self.updateGame()
                return True
            else:
                if self.win_state:
                    self.win(self.current_player)
                elif game.started and len(self.current_player.hand.cards.lst) == 0:
                    self.makeTurn(self.next_player)
                self.win_state = False
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
                game.updateCounter()
            self.pile.transfer(plr.hand, self)
            game.updateCounter()
        
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
            self.repeat.stop()
            for plr in self.players:
                plr.hand.clear()
            for card in self.pile.cards:
                card.flipCard()
            self.pile.clear()
            placeCards(self.deck, (400, 300))
            for obj in self.objects:
                if type(obj) == Button and obj.name == "Exit":
                    obj.place(700, 50)


    class Timer:
        """Initializes a timer that runs in the background of a program
        
        === Attributes ===

        beginning -> The instantaneous datetime in seconds since epoch
        duration -> How long the timer will last
        end -> The end datetime in seconds since epoch
        done -> Determine if the timer is finished or not
        """

        beginning: int
        duration: int
        end: int
        done: False

        def __init__(self, duration: int) -> None:
            self.beginning = 0
            self.duration = duration
            self.end = 0
            self.done = True
        
        def start(self) -> None:
            self.beginning = int(time.time())
            self.end = self.beginning + self.duration
            self.done = False
        
        def finish(self) -> None:
            self.done = True

        def checkTimer(self) -> None:
            if self.end == int(time.time()):
                self.done = True


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

    # Options Button
    options_text = pygame.font.SysFont('Serif', 30)
    options_button = Button(screen, "Options", 'small_banner.png', (150, 50), options_text, (400, 300))

    # Quit Button
    quit_text = pygame.font.SysFont('Serif', 30)
    quit_button = Button(screen, "Quit", 'small_banner.png', (125, 50), options_text, (400, 400))

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

    plr_hand = Hand(400, 400, "plr")
    com1_hand = Hand(500, 300, "com1")
    com2_hand = Hand(400, 200, "com2")
    com3_hand = Hand(300, 300, "com3")

    pile = Pile(screen, 400, 300)
    burn_pile = Pile(screen, 500, 400)

    plr = Player("plr", plr_hand, plr_move_sound)
    plr_counter = Counter(screen, "bottom")
    com1 = Player("com1", com1_hand, com1_move_sound)
    com1_counter = Counter(screen, "right")
    com2 = Player("com2", com2_hand, com2_move_sound)
    com2_counter = Counter(screen, "top")
    com3 = Player("com3", com3_hand, com3_move_sound)
    com3_counter = Counter(screen, "left")
    plrs = [plr, com1, com2, com3]
    counters = [plr_counter, com1_counter, com2_counter, com3_counter]

    objects = [start_button, play_button, slap_button, options_button, quit_button, exit_button, title_textbox, win_textbox, plr_counter, com1_counter, com2_counter, com3_counter]

    game = Game(plrs, counters, screen, deck, pile, burn_pile, objects, win_sound)

    timer = Timer(2)
    slaptimer = Timer(1)

    game.menu()

    while True:
        objects = [start_button, play_button, slap_button, options_button, quit_button, exit_button, title_textbox, win_textbox, plr_counter, com1_counter, com2_counter, com3_counter]

        ev = pygame.event.get()

        mouse = pygame.mouse

        if start_button.checkMouse(mouse):
            start_button.change_text_color("gold")
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.start()
                    game.makeTurn(plr)
                    refresh(screen, bg, objects, deck)
                    randomlist = random.sample(range(0, 52), 52)
                    x = 0
                    y = 0
                    for i, val in enumerate(randomlist):
                        if i % 4 == 0:
                            temp = deck[val]
                            card_move_sound.play()
                            temp.moveCard(plr.hand.x, plr.hand.y, '', game)
                            plr_hand.addCard(temp)
                            game.updateCounter()
                        elif i % 4 == 1:
                            temp = deck[val]
                            card_move_sound.play()
                            temp.moveCard(com1.hand.x, com1.hand.y, '', game)
                            com1_hand.addCard(temp)
                            game.updateCounter()
                        elif i % 4 == 2:
                            temp = deck[val]
                            card_move_sound.play()
                            temp.moveCard(com2.hand.x, com2.hand.y, '', game)
                            com2_hand.addCard(temp)
                            game.updateCounter()
                        elif i % 4 == 3:
                            temp = deck[val]
                            card_move_sound.play()
                            temp.moveCard(com3.hand.x, com3.hand.y, '', game)
                            com3_hand.addCard(temp)
                            game.updateCounter()
                    break
        else:
            start_button.change_text_color("black")

        if options_button.checkMouse(mouse):
            options_button.change_text_color("gold")
        else:
            options_button.change_text_color("black")
        
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
                    game.takeTurn()
                    timer.start()
                    break
        else:
            play_button.change_text_color("black")
        
        if slap_button.checkMouse(mouse) and slaptimer.done and len(pile) >= 2 and not plr.out:
            slap_button.change_text_color("white")
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    slap_sound.play()
                    slaptimer.start()
                    if pile.checkSlap():
                        print("Player win slap!")
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
                    exit_button.place(650, 50)
                    game.over()
                    timer.finish()
                    break
        else:
            exit_button.change_text_color("black")

        if timer.done:
            if game.started and game.check():
                timer.start()

        for event in ev:
            if event.type == pygame.QUIT: sys.exit()

        timer.checkTimer()
        slaptimer.checkTimer()

        if game.started:
            game.updateGame()
        else:
            refresh(screen, bg, objects, deck)
        await asyncio.sleep(0)

asyncio.run( main() )