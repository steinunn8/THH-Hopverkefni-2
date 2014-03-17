import wx, sys, os, pygame, random
from pygame.locals import*
import theGame

# a simple Card to test movement
# card displayed as a picture of a card
class Card(pygame.sprite.Sprite):
    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       self.image = pygame.image.load("card.png")
       self.rect = self.image.get_rect()
       self.width, self.height = self.image.get_size()

    def update(self):
        mouse_pos = app.frame.ScreenToClient(wx.GetMousePosition())
        if (app.frame.display.mouse_down and self.rect.collidepoint(mouse_pos)):
            self.rect.center = mouse_pos
            app.frame.display.card_moving = True


# cards displayed as numbers
class TempCard(pygame.sprite.Sprite):
    # common for all TempCards
    black = (0,0,0)
    red = (255,0,0)
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    width = 50
    height = 100
    
    def __init__(self, pos, num):
       pygame.sprite.Sprite.__init__(self)

       self.num = num
       self.orig_pos = pos

       '''
       # draw box
       self.image = pygame.Surface((self.width,self.height)) # created on the fly
       #self.image.set_colorkey(self.white) # white transparent
       self.rect = self.image.get_rect()
       self.rect.center = pos
       '''

       # draw text
       self.font = pygame.font.SysFont("Arial", 80)
       self.image = self.font.render(str(self.num), 1, self.black)
       self.rect = self.image.get_rect()
       self.rect.center = pos

       
    def update(self):
        mouse_pos = app.frame.ScreenToClient(wx.GetMousePosition())
        
        # if the mouse clicks on the card
        if (app.frame.display.mouse_down and self.rect.collidepoint(mouse_pos)
            and not app.frame.display.card_moving):
            # move the card with the mouse
            self.rect.center = mouse_pos
            app.frame.display.card_moving = True
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

        # -------- game stuff begin ----------
        
        pygame.init()
        self.screen = pygame.Surface(self.size, 0, 32)
        #self.card = Card()
        self.mouse_down = False
        self.card_moving = False
        self.white = (255, 255, 255)

        # groups for sprites
        self.tempCards = pygame.sprite.Group()
        self.allCards = pygame.sprite.Group()

        # positions and number of the cards
        self.x = 100
        self.y = 100
        self.num_card = 0

        # make cards in pyramid
        for i in range(7):
            tempCard = TempCard([self.x, self.y], self.num_card)
            self.tempCards.add(tempCard)
            self.allCards.add(tempCard)
            self.x += 60
            self.num_card += 1 

        # make card in deck to compare to
        self.compare_num = random.randint(0, 6)
        self.compareCard = TempCard([250, 300], self.compare_num)
        self.allCards.add(self.compareCard)
        

        # -------- game stuff end ----------

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseUp)
       
        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        # button to draw new card
        self.draw_button = wx.Button(self, label="Draw new card", pos = (400, 400))
        self.Bind(wx.EVT_BUTTON, self.drawNewCard, self.draw_button)
        
    def drawNewCard(self, event):
        # remove last card
        self.compareCard.kill()

        # make new card
        self.compare_num = random.randint(0, 6)
        self.compareCard = TempCard([250, 300], self.compare_num)
        self.allCards.add(self.compareCard)      

    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        app.frame.display.card_moving = False

        # update cards
        self.tempCards.update()

        # check if card is moved to deck
        for card in self.tempCards:
            if self.compareCard.rect.colliderect(card.rect) and self.compareCard.num == card.num:
                card.kill()

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
        #self.screen.blit(self.card.image, self.card.rect)
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

    def onMouseDown(self, event):
        self.mouse_down = True

    def onMouseUp(self, event):
        self.mouse_down = False
         
class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size = (600, 600))
       
        self.display = PygameDisplay(self, -1)
       
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-3, -4, -2])
        self.statusbar.SetStatusText("wxPython", 0)
        self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)
       
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
       
        self.curframe = 0
       
        self.SetTitle("Pyramid: First edition")
       
        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
       
        self.timer.Start((1000.0 / self.display.fps))
       
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer2, 0, flag = wx.EXPAND)
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
        self.curframe += 1
        self.statusbar.SetStatusText("Frame %i" % self.curframe, 2)

    def OnNewGame(self, event):
        # has no activity
        return
 
class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
       
        return True
 
if __name__ == "__main__":
    app = App()
    app.MainLoop()
