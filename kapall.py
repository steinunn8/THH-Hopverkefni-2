import wx, sys, os, pygame, random
import wx.animate
from pygame.locals import*
import theGame, Scores


class SpriteCard(pygame.sprite.Sprite):
    def __init__(self, pos, real_card):
        pygame.sprite.Sprite.__init__(self)

        self.orig_pos = pos
        self.real_card = real_card
        self.card_moving = False

        # set sprite image
        if (self.real_card.up):
            self.image = real_card.image
        else:
             self.image = app.frame.display.back_image

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if (not self.real_card.up):
            self.image = app.frame.display.back_image
        mouse_pos = app.frame.ScreenToClient(wx.GetMousePosition())

        # checking if any other card is on the move
        any_card_moving = False
        for card in app.frame.display.pyramid_cards:
            if (card.card_moving and card != self):
                any_card_moving = True
                
        # if the mouse clicks on the card
        if (app.frame.display.mouse_down and self.rect.collidepoint(mouse_pos)
            and not any_card_moving):
            if (self.real_card.up):
                # move the card with the mouse
                self.rect.center = mouse_pos
                #app.frame.display.card_moving = True
                self.card_moving = True
            else:
                # put front image if card is available
                self.real_card.isAvailable()
                if (self.real_card.up):
                    self.image = self.real_card.image
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

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseUp)

        # a timer to update on each frame
        self.timer = wx.Timer(self)
        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)
        
        self.deck_img_file = "cardImages/card_back.jpg"
        
        self.back_image = pygame.image.load('cardImages/card_back.jpg')

        # game stuff     
        pygame.init()
        self.screen = pygame.Surface(self.size, 0, 32)
        self.first_game = True

        # draw draw button
        self.deck_image_file = self.deck_img_file
        self.deck_image = wx.Image(self.deck_image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.draw_button = wx.BitmapButton(self, id=-1, bitmap=self.deck_image,
            pos=(700, 510), size = (self.deck_image.GetWidth()+5, self.deck_image.GetHeight()+5))
        
    def start_game(self, game):
        self.game = game
        self.start_time = 0
        self.minutes = 0
        self.mouse_down = False
        self.white = (255, 255, 255)
        self.last_bonustime = self.game.scoreThing.getBonusTime()
        self.last_time = int(self.game.getTime()) - self.start_time
        self.game_over = False

        self.background = pygame.image.load("backgrounds/panda.png")
        self.background_rect = self.background.get_rect()
        
        # groups for sprites
        self.pyramid_cards = pygame.sprite.OrderedUpdates()
        self.pile_cards = pygame.sprite.Group()

        self.generate_deck()
        self.generate_pyramid()

        app.frame.disableUndo()
        app.frame.disableRedo()

        if (self.first_game):
            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Bind(wx.EVT_TIMER, self.Update, self.timer)
            self.first_game = False


    def generate_deck(self):
         # deck to draw new card
        self.deck_image_file = self.deck_img_file
        self.deck_image = wx.Image(self.deck_image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.draw_button.SetBitmapLabel(self.deck_image)
        self.Bind(wx.EVT_BUTTON, self.drawNewCard, self.draw_button)

        # make sprite for the top card in trash pile
        self.fake_card = self.game.pyramid[0]
        self.compare_card = SpriteCard([250, 300], self.fake_card)
        self.pile_cards.add(self.compare_card)
        self.draw_card()

    def generate_pyramid(self):
        for i in range(0, len(self.game.pyramid)):
            self.card = self.game.pyramid[i]
            self.pyramid_card = SpriteCard([self.card.x, self.card.y], self.card)
            self.pyramid_cards.add(self.pyramid_card)
        
    def Update(self, event):
        # update cards
        self.pyramid_cards.update()

        # draw everything on screen
        self.Redraw()
 
    def Redraw(self):
        # to draw the screen again correctly if you resize it
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False 

        # draw background
        self.screen.blit(self.background, self.background_rect)

        # draw the cards
        # we draw them in seperate groups to make sure that pyramid cards have a higher z-level
        self.pile_cards.draw(self.screen)
        self.pyramid_cards.draw(self.screen)

        self.draw_points()
        self.draw_bonustime()
        self.draw_time()
        
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

        # check if user tried to move card to deck
        self.check_card_to_deck()

        # no card is moving anymore
        for card in self.pyramid_cards:
            card.card_moving = False
        
    def check_card_to_deck(self):
        # check if card is moved to deck
        for card in self.pyramid_cards:
            if self.compare_card.rect.colliderect(card.rect): # if colliding
                can_kill = self.game.pick(card.real_card)   # if correct card
                if (can_kill):
                    self.put_card_to_pile(card)

    def put_card_to_pile(self, card):
        # set card to deck
        self.compare_card.kill()
        self.compare_card = SpriteCard([self.last_compare_card.real_card.x, self.last_compare_card.real_card.y], card.real_card)
        self.pile_cards.add(self.compare_card)
        self.last_compare_card = self.compare_card
        
        # remove card from pyramid
        card.kill()

        # check if game is won
        self.game_won()

        # make it impossible to "undo" and "redo"
        app.frame.disableUndo()
        app.frame.disableRedo()

    def drawNewCard(self, event):
        self.draw_card()

    def draw_card(self):
        # remove last card
        self.compare_card.kill()

        if (self.game.deck.isEmpty()):
            # display a joker on the deck if it's empty
            self.deck_image_file = "joker.png"        
            self.deck_image = wx.Image(self.deck_image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.draw_button.SetBitmapLabel(self.deck_image)

            # display last card in pile
            new_card = self.game.flip()
            self.compare_card = self.last_compare_card;
            self.pile_cards.add(self.compare_card)
        else:
            # get new card from deck
            self.undo_compare_card = self.compare_card
            new_card = self.game.flip()
            new_card.up = True
            self.compare_card = SpriteCard([new_card.x, new_card.y], new_card)
            self.pile_cards.add(self.compare_card)
            self.last_compare_card = self.compare_card
            app.frame.onUndoDone()
           
    def draw_points(self):
        #self.points = Scores.getCurrentPoints(self.game)
        self.points = self.game.scoreThing.getCurrentPoints()
        black = (0,0,0)
        pos = (70, 600)
        
        # draw points
        self.points_font = pygame.font.SysFont("Arial", 30)
        self.points_image = self.points_font.render(str(self.points), 1, black)
        self.points_rect = self.points_image.get_rect()
        self.points_rect.center = pos
        self.screen.blit(self.points_image, self.points_rect)
    
    def draw_bonustime(self):
        if(self.game_over):
            self.bonustime = self.last_bonustime
        else:
            self.bonustime = self.game.scoreThing.getBonusTime()
        black = (0,0,0)
        pos = (780, 50)
        
        # draw points
        self.bonustime_font = pygame.font.SysFont("Arial", 20)
        self.bonustime_image = self.bonustime_font.render(str(self.bonustime), 1, black)
        self.bonustime_rect = self.bonustime_image.get_rect()
        self.bonustime_rect.center = pos
        self.screen.blit(self.bonustime_image, self.bonustime_rect)

    def draw_time(self):
        # get seconds
        if(self.game_over):
            self.elapsed_time = self.last_time
        else:
            self.elapsed_time = int(self.game.getTime()) - self.start_time
        
        # get minutes
        if (self.elapsed_time >= 60):
            self.start_time = int(self.game.getTime())
            self.minutes += 1
            
        # time text
        if (self.elapsed_time < 10 and self.minutes < 10):
            self.time = "Time played: 0" + str(self.minutes) + ":0" + str(self.elapsed_time)
        elif (self.elapsed_time < 10 and self.minutes >= 10):
            self.time = "Time played: " + str(self.minutes) + ":0" + str(self.elapsed_time)
        elif (self.elapsed_time >= 10 and self.minutes < 10):
            self.time = "Time played: 0" + str(self.minutes) + ":" + str(self.elapsed_time)
        elif (self.elapsed_time >= 10 and self.minutes >= 10):
            self.time = "Time played: " + str(self.minutes) + ":" + str(self.elapsed_time)

        # display time
        black = (0,0,0)
        pos = (100, 50)
        
        self.time_font = pygame.font.SysFont("Arial", 20)
        self.time_image = self.time_font.render(str(self.time), 1, black)
        self.time_rect = self.time_image.get_rect()
        self.time_rect.center = pos
        self.screen.blit(self.time_image, self.time_rect)

    def game_won(self):
        if len(self.pyramid_cards.sprites()) == 0:
            self.last_bonustime = self.game.scoreThing.getBonusTime()
            self.last_time = int(self.game.getTime()) - self.start_time
            self.game_over = True
            total = str(self.game.scoreThing.getScore())
            divided = self.game.scoreThing.getDivided()
            self.post_score_frame = PostHighScoreFrame(parent = None, total = total, divided = divided, won = True)
            self.post_score_frame.Show()  
    
    def undo_draw(self):
        # put card back in pile
        self.game.undoDraw(self.compare_card.real_card)

        # save card for redo option
        self.future_card = self.compare_card

        # remove current card
        self.compare_card.kill()

        # get last card
        self.compare_card = SpriteCard([self.undo_compare_card.real_card.x, self.undo_compare_card.real_card.y], self.undo_compare_card.real_card)
        self.pile_cards.add(self.compare_card)

    def redo_draw(self):
        # draw card again
        self.draw_card()
         
class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size = (900, 750))
        wx.Frame.CenterOnScreen(self)
        self.display = PygameDisplay(self, -1)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)
        self.undoClicked = True

        # menu bar
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menuBar.Append(menu, "&File")
        # NEW GAME
        m_new_game = menu.Append(wx.ID_ABOUT, "&New Game", "Start a new game.")
        self.Bind(wx.EVT_MENU, self.OnNewGame, m_new_game)
        # HIGH SCORE
        m_show_highscore = menu.Append(wx.ID_PREVIEW, "&High Score", "See top 5 scores.")
        self.Bind(wx.EVT_MENU, self.getHighScores, m_show_highscore)
        # HELP
        m_help = menu.Append(wx.ID_HELP, "&Help", "Get help.")
        self.Bind(wx.EVT_MENU, self.getHelp, m_help)
        # GIVE UP
        m_give_up = menu.Append(wx.ID_ABORT, "&Give Up", "Give up and save score")
        self.Bind(wx.EVT_MENU, self.onGiveUp, m_give_up)
        # EXTI
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.Kill, m_exit)

        # change looks
        looks = wx.Menu()
        menuBar.Append(looks, "&Looks")
        # change background
        backgrounds = wx.Menu()
        background1 = backgrounds.Append(wx.NewId(), "Panda")
        self.Bind(wx.EVT_MENU, self.choose_background1, background1)
        background2 = backgrounds.Append(wx.NewId(), "Dog")
        self.Bind(wx.EVT_MENU, self.choose_background2, background2)
        background3 = backgrounds.Append(wx.NewId(), "Pyramids")
        self.Bind(wx.EVT_MENU, self.choose_background3, background3)
        background4 = backgrounds.Append(wx.NewId(), "Bender")
        self.Bind(wx.EVT_MENU, self.choose_background4, background4)
        background5 = backgrounds.Append(wx.NewId(), "Unicorn")
        self.Bind(wx.EVT_MENU, self.choose_background5, background5)
        looks.AppendMenu(wx.NewId(), "Choose background", backgrounds)
        
        #change card image
        cardImages = wx.Menu()
        cardImage1 = cardImages.Append(wx.NewId(), "Linux")
        self.Bind(wx.EVT_MENU, self.choose_cardImage1, cardImage1)
        cardImage2 = cardImages.Append(wx.NewId(), "Classic red")
        self.Bind(wx.EVT_MENU, self.choose_cardImage2, cardImage2)
        cardImage3 = cardImages.Append(wx.NewId(), "Aces")
        self.Bind(wx.EVT_MENU, self.choose_cardImage3, cardImage3)
        cardImage4 = cardImages.Append(wx.NewId(), "Panda love")
        self.Bind(wx.EVT_MENU, self.choose_cardImage4, cardImage4)
        cardImage5 = cardImages.Append(wx.NewId(), "Wat")
        self.Bind(wx.EVT_MENU, self.choose_cardImage5, cardImage5)
        looks.AppendMenu(wx.NewId(), "Choose card image", cardImages)
        
        self.toolbar = self.CreateToolBar()
        tundo = self.toolbar.AddLabelTool(wx.ID_UNDO, '', wx.Bitmap('tundo.png'))
        tredo = self.toolbar.AddLabelTool(wx.ID_REDO, '', wx.Bitmap('tredo.png'))
        self.toolbar.EnableTool(wx.ID_REDO, False)
        self.toolbar.Realize()

        self.Bind(wx.EVT_MENU, self.onUndo, tundo)
        self.Bind(wx.EVT_MENU, self.onRedo, tredo)

        self.SetMenuBar(menuBar)       
        self.SetTitle("Pyramid")

        self.Bind(wx.EVT_SIZE, self.OnSize)
       
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

    def OnNewGame(self, event):
        app.level_frame = LevelFrame(parent = None)
        app.level_frame.Show()

    def getHighScores(self, event):
        global dummy_game
        temp = dummy_game.scoreThing.getHighScoreString()
        self.high_score_frame = HighScoreFrame(parent = None, temp = temp)
        self.high_score_frame.Show()

    def getHelp(self, event):
        global dummy_game
        temp = dummy_game.scoreThing.getHelp()
        self.help_frame = HelpFrame(parent = None, temp = temp)
        self.help_frame.Show()

    def onGiveUp(self, event):
        self.display.last_bonustime = self.display.game.scoreThing.getBonusTime()
        self.display.last_time = int(self.display.game.getTime()) - self.display.start_time
        self.display.game_over = True
        self.game = self.display.game
        score = self.game.scoreThing
        total = str(score.getScore())
        divided = score.getDivided()
        self.post_score_frame = PostHighScoreFrame(parent = None, total = total, divided = divided, won = False)
        self.post_score_frame.Show()

    # When Undo is clicked we disable it and get last card
    def onUndo(self, event):
        card = self.display.game.trash.show()
        if card.fromDeck == True:
            self.toolbar.EnableTool(wx.ID_UNDO, False)
            self.toolbar.EnableTool(wx.ID_REDO, True)
            self.undoClicked = True
            self.display.undo_draw()            #Get last card
        else:
            self.toolbar.EnableTool(wx.ID_UNDO, False)

    # Function for checking if undo should be enabled or disabled
    def onUndoDone(self):
        card = self.display.game.trash.show()
        if card.fromDeck == True:
            self.toolbar.EnableTool(wx.ID_UNDO, True)
            self.toolbar.EnableTool(wx.ID_REDO, False)
        else:
            self.toolbar.EnableTool(wx.ID_UNDO, False)

    def disableUndo(self):
        self.toolbar.EnableTool(wx.ID_UNDO, False)
        self.undoClicked = False

    # When Redo is clicked, we redraw the card that we drew before
    def onRedo(self, event):
        if self.undoClicked:
            self.toolbar.EnableTool(wx.ID_REDO, False)
            self.toolbar.EnableTool(wx.ID_UNDO, True)
            self.undoClicked = False
            self.display.redo_draw()    #Redraw

    def disableRedo(self):
        self.toolbar.EnableTool(wx.ID_REDO, False)
        self.undoClicked = False


    # Functions for choosing backgrounds
    def choose_background1(self, event):
        self.display.background = pygame.image.load("backgrounds/panda.png")
        self.display.background_rect = self.display.background.get_rect()

    def choose_background2(self, event):
        self.display.background = pygame.image.load("backgrounds/dog.jpg")
        self.display.background_rect = self.display.background.get_rect()

    def choose_background3(self, event):
        self.display.background = pygame.image.load("backgrounds/pyramids.jpg")
        self.display.background_rect = self.display.background.get_rect()

    def choose_background4(self, event):
        self.display.background = pygame.image.load("backgrounds/bender.jpg")
        self.display.background_rect = self.display.background.get_rect()

    def choose_background5(self, event):
        self.display.background = pygame.image.load("backgrounds/unicorn.png")
        self.display.background_rect = self.display.background.get_rect()
       

    # Functions for choosing backgrounds
    def choose_cardImage1(self, event):
        self.display.deck_img_file = 'cardImages/card_back.jpg'
        self.display.deck_image = wx.Image(self.display.deck_img_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.display.draw_button.SetBitmapLabel(self.display.deck_image)
        self.display.back_image = pygame.image.load("cardImages/card_back.jpg")
        
    def choose_cardImage2(self, event):
        self.display.deck_img_file = 'cardImages/classic_red.png'
        self.display.deck_image = wx.Image(self.display.deck_img_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.display.draw_button.SetBitmapLabel(self.display.deck_image)
        self.display.back_image = pygame.image.load("cardImages/classic_red.png")
        
    def choose_cardImage3(self, event):
        self.display.deck_img_file = 'cardImages/aces.png'
        self.display.deck_image = wx.Image(self.display.deck_img_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.display.draw_button.SetBitmapLabel(self.display.deck_image)
        self.display.back_image = pygame.image.load("cardImages/aces.png")

    def choose_cardImage4(self, event):
        self.display.deck_img_file = 'cardImages/pandalove.jpeg'
        self.display.deck_image = wx.Image(self.display.deck_img_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.display.draw_button.SetBitmapLabel(self.display.deck_image)
        self.display.back_image = pygame.image.load("cardImages/pandalove.jpeg")

    def choose_cardImage5(self, event):
        self.display.deck_img_file = 'cardImages/wat.jpeg'
        self.display.deck_image = wx.Image(self.display.deck_img_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.display.draw_button.SetBitmapLabel(self.display.deck_image)
        self.display.back_image = pygame.image.load("cardImages/wat.jpeg")


# The frame that you see when you choose new game
class LevelFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Choose level')
        wx.Frame.CenterOnScreen(self)

        self.Bind(wx.EVT_CLOSE, self.Kill)
        
        self.grid = wx.GridBagSizer(hgap=3, vgap=3)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetBackgroundColour('#a4dba3')
		
        self.fyrirsogn = wx.StaticText(self, label="Choose a level") #pos = (140,20)
        self.fyrirsognFont = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.fyrirsogn.SetFont(self.fyrirsognFont)
        self.sizer.Add(self.fyrirsogn, flag=wx.ALL|wx.EXPAND, border=20)
        
        self.level1 = wx.RadioButton(self, 1, "Level 1 : 5 rows and color doesn't matter")
        self.grid.Add(self.level1, pos=(0,0), span=(1,2))
        self.Bind(wx.EVT_RADIOBUTTON, self.Levels, self.level1)
        
        self.level2 = wx.RadioButton(self, 2, "Level 2 : 6 rows and color doesn't matter")
        self.grid.Add(self.level2, pos=(1,0))
        self.Bind(wx.EVT_RADIOBUTTON, self.Levels, self.level2)
        
        self.level3 = wx.RadioButton(self, 3, "Level 3 : 7 rows and color doesn't matter")
        self.grid.Add(self.level3, pos=(2,0))
        self.Bind(wx.EVT_RADIOBUTTON, self.Levels, self.level3)
        
        self.level4 = wx.RadioButton(self, 4, "Level 4 : 5 rows and color matters")
        self.grid.Add(self.level4, pos=(0,3))
        self.Bind(wx.EVT_RADIOBUTTON, self.Levels, self.level4)
        
        self.level5 = wx.RadioButton(self, 5, "Level 5 : 6 rows and color matters")
        self.grid.Add(self.level5, pos=(1,3))
        self.Bind(wx.EVT_RADIOBUTTON, self.Levels, self.level5)
        
        self.level6 = wx.RadioButton(self, 6, "Level 6 : 7 rows and color matters")
        self.grid.Add(self.level6, pos=(2,3))
        self.Bind(wx.EVT_RADIOBUTTON, self.Levels, self.level6)
        
        self.sizer.Add(self.grid, flag=wx.ALL|wx.EXPAND, border=10)
        
        self.start_game_button = wx.Button(self, label="Start game", size= (100, 50))
        self.Bind(wx.EVT_BUTTON, self.start_game, self.start_game_button)
        self.sizer.Add(self.start_game_button, 0, wx.ALIGN_CENTER, 20)

        self.height = 7
        self.sortsOn = True
        
        self.SetSizerAndFit(self.sizer)        

    def start_game(self, event):
        if (app.first_game):
            app.frame.Show()
            app.first_game = False
            
        game = theGame.theGame(self.height, self.sortsOn)
        app.frame.display.start_game(game)
        self.Destroy()
    
    def Levels(self, event):
        if(event.Id == 1):
            self.height = 5
            self.sortsOn = False
        if(event.Id == 2):
            self.height = 6
            self.sortsOn = False
        if(event.Id == 3):
            self.height = 7
            self.sortsOn = False
        if(event.Id == 4):
            self.height = 5
            self.sortsOn = True
        if(event.Id == 5):
            self.height = 6
            self.sortsOn = True
        if(event.Id == 6):
            self.height = 7
            self.sortsOn = True

    def Kill(self, event):
        # if user doesn't pick level he get's level 1
        game_level_1 = theGame.theGame(5, False)
        app.frame.display.start_game(game_level_1)
        self.Destroy()

#Frame for help text from menu
class HelpFrame(wx.Frame):
    def __init__(self, parent, temp):
        wx.Frame.__init__(self, parent, -1, 'Help', size = (500, 700))
        wx.Frame.CenterOnScreen(self)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetBackgroundColour('#eefaa8')

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, -1, temp, style=wx.ALIGN_LEFT, size=(500, 500))
        self.ok_button = wx.Button(self, label="Ok, got it!", pos = (200,500), size= (100, 50))
        self.Bind(wx.EVT_BUTTON, self.okClicked, self.ok_button )
        self.sizer.Add(self.ok_button , 0, wx.ALIGN_BOTTOM, 5)

    def okClicked(self, event):
        self.Destroy()
        
    def OnSize(self, event):
        self.Layout()
 
# Frame for showing High Score from menu        
class HighScoreFrame(wx.Frame):
    def __init__(self, parent, temp):
        wx.Frame.__init__(self, parent, -1, 'High Score', size = (200, 200))
        wx.Frame.CenterOnScreen(self)
        self.SetBackgroundColour('#FF99CC')

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.head = wx.StaticText(self, -1, '\n    High Score: Top 5 scores \n \n' + temp)
        
    def OnSize(self, event):
        self.Layout()

#Frame for showing users score when he wins
class PostHighScoreFrame(wx.Frame):
    def __init__(self, parent, total, divided, won = False):
        wx.Frame.__init__(self, parent, -1, 'Your score', size = (509, 700))
        wx.Frame.CenterOnScreen(self)
        self.total = total
        self.divided = divided
        self.won = won
        self.initFrame()
        self.Bind(wx.EVT_CLOSE, self.Kill)

    def OnSize(self, event):
        self.Layout()

    def Kill(self, event):
        app.level_frame = LevelFrame(parent = None)
        app.level_frame.Show()
        self.Destroy()

    #   calls methods that make panels to hold buttons, texts and pictures
    def initFrame(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#4f5049')
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.makeGif(self.won)        
        self.makeScorePan(self.total, self.divided)
        self.makeName()
        self.makeGamePan()

        self.panel.SetSizer(self.vbox)

    def makeGif(self, won):
        self.gifPan = wx.Panel(self.panel, size = (499,335))
        self.gifPan.SetBackgroundColour('#001100')
        self.pos = (-1,-1)
        # Gif part
        if (won):
            gif_file = "panda.gif"
            #self.pos = (-1,-1)
        else:
            gif_file = "pandagiveup.gif"
            self.pos = (200,50)
        self.gif = wx.animate.GIFAnimationCtrl(self.gifPan, -1, gif_file, pos = self.pos)
        # clears the background
        self.gif.GetPlayer().UseBackgroundColour(True)
        # continuously loop through the frames of the gif file (default)
        self.gif.Play()
        self.vbox.Add(self.gifPan, 1, wx.EXPAND | wx.ALL, 5)

    def makeScorePan(self, total, divided):
        self.scorePan = wx.Panel(self.panel, size = (510,140))
        # mint color = #a4dba3
        self.scorePan.SetBackgroundColour('#a4dba3')
        score_text = '\n     You got ' + total + ' points \n     Your points divide like this:\n'+ divided
        self.text = wx.StaticText(self.scorePan, -1, score_text, style=wx.ALIGN_LEFT, pos = (50,5))
        self.text.Wrap(1000)
        self.vbox.Add(self.scorePan, 1, wx.EXPAND | wx.ALL, 5)

    #   creates the options to end game or start new
    def makeGamePan(self):
        self.gamePan = wx.Panel(self.panel)
        #   cosy pink color = #FF99CC
        self.gamePan.SetBackgroundColour('#FF99CC')
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.quitgame = wx.Button(self.gamePan, label="Quit game")
        #self.quitgame = wx.Button(self.gamePan, label="Quit game", pos = (230,0))
        self.quitgame.Bind(wx.EVT_BUTTON, self.quitGame)
        self.hbox.Add(self.quitgame,1, wx.EXPAND | wx.ALL)

        #self.newgame = wx.Button(self.gamePan, label="New game", pos = (120,0))
        self.newgame = wx.Button(self.gamePan, label="New game")
        self.hbox.Add(self.newgame,1, wx.EXPAND | wx.ALL)
        self.newgame.Bind(wx.EVT_BUTTON, self.newGame)


        self.gamePan.SetSizer(self.hbox)
        self.vbox.Add(self.gamePan, 1, wx.EXPAND | wx.ALL, 5)

    def newGame(self, event):
        self.Destroy()
        app.level_frame = LevelFrame(parent = None)
        app.level_frame.Show()
        
    def quitGame(self, event):
        self.Destroy()
        app.frame.Kill(app.frame)

    def makeName(self):
        self.namePan = wx.Panel(self.panel)
        # yellow cream = #eefaa8
        self.namePan.SetBackgroundColour('#eefaa8')
        #self.name_panel = wx.Panel(self, -1, size = (500,700))
        self.name = ""
        self.lblname = wx.StaticText(self.namePan, label="Enter name:", pos = (60, 5))
        self.lblscore = wx.StaticText(self.namePan, label="Score:", pos = (60, 45))
        self.theScore = wx.StaticText(self.namePan, label=str(self.total), pos = (200, 45))
        self.editname = wx.TextCtrl(self.namePan, size=(140, -1), pos = (200,5))
        self.button = wx.Button(self.namePan, label="Save score", pos = (300,35))
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        self.vbox.Add(self.namePan, 1, wx.EXPAND | wx.ALL, 5)
    
    def OnButton(self, event):
        self.name = self.editname.GetValue()
        global dummy_game
        self.game = dummy_game
        nameStr = self.name + '\t'
        scoreStr = str(self.total) + '\n'
        self.game.scoreThing.addName(nameStr)
        self.game.scoreThing.addScore(scoreStr)
        self.button.Disable()

class App(wx.App):
    def OnInit(self):

        self.first_game = True
        
        # game window
        self.frame = Frame(parent = None)
        #self.frame.Show()
        self.SetTopWindow(self.frame)

        # level window
        self.level_frame = LevelFrame(parent = None)
        self.level_frame.Show()

        return True

    
if __name__ == "__main__":
    dummy_game = theGame.theGame(4)  # used to get access to help.txt and allScores.txt
    app = App()
    app.MainLoop()
