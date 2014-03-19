import wx, sys, os, pygame, random
from pygame.locals import*
import theGame

# card displayed as a picture of a card
# to use later with a card sprite
class Card(pygame.sprite.Sprite):
    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       self.image = pygame.image.load("card.png")
       self.rect = self.image.get_rect()
       self.width, self.height = self.image.get_size()

    def update(self):
        return

# temporary cards - cards displayed as numbers
class TempCard(pygame.sprite.Sprite):
    # common for all TempCards
    black = (0,0,0)
    red = (255,0,0)
    
    def __init__(self, pos, num, real_card):
        pygame.sprite.Sprite.__init__(self)

        self.num = num
        self.orig_pos = pos
        self.real_card = real_card
        
        # set color to red if card is "facing up"
        if (self.real_card.up):
            self.color = self.red
        else:
            self.color = self.black
            
        # "draw card"
        self.font = pygame.font.SysFont("Arial", 70)
        self.image = self.font.render(str(self.num), 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        mouse_pos = app.frame.ScreenToClient(wx.GetMousePosition())
        
        # if the mouse clicks on the card
        if (app.frame.display.mouse_down and self.rect.collidepoint(mouse_pos)
            and not app.frame.display.card_moving):
            if (self.real_card.up):
                # move the card with the mouse
                self.rect.center = mouse_pos
                app.frame.display.card_moving = True
            else:
                self.real_card.isAvailable()
                if (self.real_card.up):
                    # change color of card
                    self.color = self.red
                    self.image = self.font.render(str(self.num), 1, self.color)
        else:
            # move the card to it's original position
            self.rect.center = self.orig_pos

    
class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
       
        self.size = self.GetSizeTuple()
        self.size_dirty = True

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseUp)
       
        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        # -------- game stuff begin ----------
        
        pygame.init()
        self.screen = pygame.Surface(self.size, 0, 32)
        self.mouse_down = False
        self.card_moving = False
        self.white = (255, 255, 255)

        self.start_game(game)
        
        # button to draw new card
        self.draw_button = wx.Button(self, label="Draw new card", pos = (700, 500))
        self.Bind(wx.EVT_BUTTON, self.drawNewCard, self.draw_button)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        # -------- game stuff end ----------
        

    def Update(self, event):
        self.card_moving = False

        # update cards
        self.tempCards.update()

        # draw everything on screen
        self.Redraw()
 
    def Redraw(self):
        # to draw the screen again correctly if you resize it
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False 

        # set background white
        self.screen.fill(self.white)

        # draw the cards
        self.allCards.draw(self.screen)

        # stuff to draw everything with wx/pygame combined
        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.ImageFromData(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc
        
        
    def OnPaint(self, event):
        self.Redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well
 
    def OnSize(self, event):
        self.size = self.GetSizeTuple()
        self.size_dirty = True
 
    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)

    def start_game(self, game):
        self.game = game
        
        # groups for sprites
        self.tempCards = pygame.sprite.Group()
        self.allCards = pygame.sprite.Group()

        self.generate_pyramid()
        self.generate_deck()
        
    def onMouseDown(self, event):
        self.mouse_down = True

    def onMouseUp(self, event):
        self.mouse_down = False

        # check if card is moved to deck
        for card in self.tempCards:
            if self.compareCard.rect.colliderect(card.rect):
                can_kill = self.game.pick(card.real_card)
                if (can_kill):
                    # set card to deck
                    self.compareCard.kill()
                    self.compareCard = TempCard([450, 500], str(card.real_card), card.real_card)
                    self.allCards.add(self.compareCard)
                    # remove card from pyramid
                    card.kill()

    def generate_pyramid(self):
        # make sprites for cards
        for i in range(0, len(self.game.pyramid)):
            self.card = self.game.pyramid[i]
            self.tempCard = TempCard([self.card.x, self.card.y], str(self.card), self.card)
            self.tempCards.add(self.tempCard)
            self.allCards.add(self.tempCard)

    def generate_deck(self):
        # make sprite for top card in trash pile/last card drawn
        self.compare_num = random.randint(0, 6)
        self.compareCard = TempCard([250, 300], self.compare_num, self.card)
        self.allCards.add(self.compareCard)
        self.draw_card()

    def drawNewCard(self, event):        
        self.draw_card()

    def draw_card(self):
        # remove last card
        self.compareCard.kill()

        # get new card from deck
        newCard = self.game.flip()
        self.compareCard = TempCard([newCard.x, newCard.y], str(newCard), newCard)
        self.allCards.add(self.compareCard)
        
         
class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size = (900, 700))      
        self.display = PygameDisplay(self, -1)
       
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)

        # menu bar
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.Kill, m_exit)
        menuBar.Append(menu, "&File")
        m_new_game = menu.Append(wx.ID_ABOUT, "&New Game", "Start a new game.")
        self.Bind(wx.EVT_MENU, self.OnNewGame, m_new_game)

        self.SetMenuBar(menuBar)       
        self.SetTitle("Pyramid: First edition")
       
        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
       
        self.timer.Start((1000.0 / self.display.fps))
       
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.display, 1, flag = wx.EXPAND)
       
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
 
    def Kill(self, event):
        self.display.Kill(event)
        self.Destroy()
 
    def OnSize(self, event):
        self.Layout()

    def Update(self, event):
        # has no activity yet
        return

    def OnNewGame(self, event):
        self.game = theGame.theGame(4)
        self.display.start_game(self.game)
           
     
class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
       
        return True

    
if __name__ == "__main__":
    game = theGame.theGame(4)
    
    app = App()
    app.MainLoop()
