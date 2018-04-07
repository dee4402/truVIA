import pygame, sys, math, random, time, operator, os,textwrap
from pygame.locals import *
import RPi.GPIO as GPIO
import pygame.mixer
#hello
WIDTH = 1020
HEIGHT = 760
FPS = 30
BOXSIZE = 20
BOARDWIDTH = 30
BOARDHEIGHT = 50
BLANK = '.'
XMARGIN = int((WIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = HEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
NAVY        = ( 46, 64,   83)
PEACH       = (245, 183, 177)
ORANGE      = (229, 152, 102)
           
BORDERCOLOR = ( 244, 246, 247 ) 
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
XAxis = 300
YAxis = 200
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
global PLAYER1, PLAYER2, SELECTED
# initialize font object
pygame.font.init()

def main():
    global CLOCK, game_state
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pygame.init()
    CLOCK = pygame.time.Clock()   
    pygame.display.set_caption('TrueVia')
    background_color = (46, 64, 83)
    (WIDTH, HEIGHT) = (1240, 800)

    # initialize the DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Game')
    DISPLAYSURF.fill(background_color)
    pygame.display.flip()

   
        #DISPLAYSURF.fill(NAVY)
        #scoreImg = BASICFONT.render(str(score), 1, SCORECOLOR)
        #scoreRect = scoreImg.get_rect()
        #scoreRect.bottomleft = (10, WINDOWHEIGHT - 6)
        #DISPLAYSURF.blit(scoreImg, scoreRect)
   # DISPLAYSURF.fill(PEACH)
        # pygame.draw.rect(DISPLAYSURF, PEACH, (0,0,230,768))
       # pygame.draw.rect(DISPLAYSURF, ORANGE, (790,0,230,768))

    #pixObj = pygame.PixelArray(DISPLAYSURF)
    #pygame.draw.ellipse(DISPLAYSURF, RED, [300, 10, 50, 20]) 
##    pygame.display.flip() 

    running = True
    game_state = 0
    category = ""
    while running:
        if game_state == 0:
           game_state = start(game_state)
        #elif game_state == 1:
            #game_state = get_name(game_state)
        elif game_state == 1:
            game_state, SELECTED = pick_player(game_state)
        elif game_state == 2:
            game_state, category = pick_category(game_state,SELECTED)
        elif game_state == 3:
            game_state = question_screen(game_state,category);
            
        #for event in pygame.event.get():
         #   if event.type == pygame.QUIT:
          #      running = False        
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
                
        pygame.display.update()
        CLOCK.tick(FPS)
               
    #BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    #BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    
def start(game_state):
    # draw start DISPLAYSURF
    draw_title("Trivia Game")
    draw_play_button()

    # wait until button press to continue
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False

    # set game_state for next DISPLAYSURF
    game_state = 1
    return game_state


def draw_title(title):
    basicfont = pygame.font.SysFont(None, 100)
    text = basicfont.render(title, True, (255, 255, 255))
    textrect = text.get_rect()
    textrect.centerx = DISPLAYSURF.get_rect().centerx
    textrect.centery = DISPLAYSURF.get_rect().centery - HEIGHT/4

    DISPLAYSURF.blit(text, textrect)
    pygame.display.update()

def draw_play_button():
    play_box_color = (250, 128, 114)
    basicfont = pygame.font.SysFont(None, 100)
    text = basicfont.render('Play', True, (0, 0, 0), play_box_color)
    textrect = text.get_rect()
    textrect.centerx = DISPLAYSURF.get_rect().centerx
    textrect.centery = DISPLAYSURF.get_rect().centery

    rect_HEIGHT = HEIGHT/4
    rect_WIDTH = WIDTH/3

    pygame.draw.rect(DISPLAYSURF, play_box_color, (DISPLAYSURF.get_rect().centerx - rect_WIDTH/2, DISPLAYSURF.get_rect().centery - rect_HEIGHT/2, rect_WIDTH, rect_HEIGHT), 0)
    DISPLAYSURF.blit(text, textrect)
    pygame.display.update()

def draw_players(player1_color, player2_color):
    basicfont = pygame.font.SysFont(None, 75)
    text = basicfont.render('Player 1', True, (0, 0, 0), player1_color)    
    textrect = text.get_rect()
    textrect.bottomleft = tuple(map(operator.add,DISPLAYSURF.get_rect().bottomleft,(textrect.width,-5* textrect.height)))
    
    text2 = basicfont.render('Player 2', True, (0, 0, 0), player2_color) 
    textrect2 = text2.get_rect()
    textrect2.bottomright = tuple(map(operator.add,DISPLAYSURF.get_rect().bottomright,(-textrect2.width,-5 *textrect2.height)))
    
    
    pygame.draw.rect(DISPLAYSURF, player1_color, (textrect.centerx-textrect.width, textrect.centery-textrect.height, 2* textrect.width, 2* textrect.height))
    pygame.draw.rect(DISPLAYSURF, player2_color, (textrect2.centerx-textrect2.width, textrect2.centery-textrect2.height, 2* textrect2.width, 2* textrect2.height))
    DISPLAYSURF.blit(text, textrect)
    DISPLAYSURF.blit(text2, textrect2)
    
    pygame.display.update()

#A player is chosen to pick question category
def pick_player(game_state):
    DISPLAYSURF.fill(NAVY)
    draw_title("Choose Player")
    selected_button_color = (255, 39, 154)
    cur_button_color = (255, 255, 255)
    
    random_num = random.randint(2,5)
    for x in range(random_num):
        draw_players(selected_button_color,cur_button_color)
        pygame.time.delay(200)
        draw_players(cur_button_color,selected_button_color)
        pygame.time.delay(200)
    
    if random_num % 2 == 0:
        draw_players(selected_button_color,cur_button_color)
        SELECTED = 1
    else:
        draw_players(cur_button_color,selected_button_color)
        SELECTED = 2
        
    game_state = 2
    return game_state, SELECTED

def display_category(name):
    basicfont = pygame.font.SysFont(None, 90)
    rect_HEIGHT = HEIGHT/4
    rect_WIDTH = WIDTH/2
    
    if name == "MTSU": 
        category = basicfont.render(name, True, (255, 255, 255), LIGHTBLUE)
        category_rect = category.get_rect()
        category_rect.center =  DISPLAYSURF.get_rect().center
        pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (DISPLAYSURF.get_rect().centerx - rect_WIDTH/2, DISPLAYSURF.get_rect().centery - rect_HEIGHT/2, rect_WIDTH, rect_HEIGHT), 0)
    elif name == "Random":    
        category = basicfont.render(name, True, (255, 255, 255), LIGHTGREEN)
        category_rect = category.get_rect()
        category_rect.center =  DISPLAYSURF.get_rect().center
        pygame.draw.rect(DISPLAYSURF, LIGHTGREEN, (DISPLAYSURF.get_rect().centerx - rect_WIDTH/2, DISPLAYSURF.get_rect().centery - rect_HEIGHT/2, rect_WIDTH, rect_HEIGHT), 0)
    elif name == "Entertainment":    
        category = basicfont.render(name, True, (255, 255, 255), LIGHTRED)
        category_rect = category.get_rect()
        category_rect.center =  DISPLAYSURF.get_rect().center
        pygame.draw.rect(DISPLAYSURF, LIGHTRED, (DISPLAYSURF.get_rect().centerx - rect_WIDTH/2, DISPLAYSURF.get_rect().centery - rect_HEIGHT/2, rect_WIDTH, rect_HEIGHT), 0)
    elif name == "Geography":    
        category = basicfont.render(name, True, (255, 255, 255), YELLOW)
        category_rect = category.get_rect()
        category_rect.center =  DISPLAYSURF.get_rect().center
        pygame.draw.rect(DISPLAYSURF, YELLOW, (DISPLAYSURF.get_rect().centerx - rect_WIDTH/2, DISPLAYSURF.get_rect().centery - rect_HEIGHT/2, rect_WIDTH, rect_HEIGHT), 0)
    else:    
        category = basicfont.render(name, True, (255, 255, 255), PEACH)
        category_rect = category.get_rect()
        category_rect.center =  DISPLAYSURF.get_rect().center
        pygame.draw.rect(DISPLAYSURF, PEACH, (DISPLAYSURF.get_rect().centerx - rect_WIDTH/2, DISPLAYSURF.get_rect().centery - rect_HEIGHT/2, rect_WIDTH, rect_HEIGHT), 0)
 
    #category = basicfont.render('MTSU', True, (0, 0, 0), LIGHTBLUE) 
    
    DISPLAYSURF.blit(category, category_rect)
    pygame.display.update()
    
    return name

#Category of question options are picked by picked player button click
def pick_category(game_state, selected):
    DISPLAYSURF.fill(NAVY)
    players_color = (250, 128, 114)
    selected_button_color = (255, 39, 154)
    
    basicfont = pygame.font.SysFont(None, 75)
    
    if selected == 1:
        text = basicfont.render('Player 1', True, (0, 0, 0), selected_button_color)    
        textrect = text.get_rect()
        textrect.bottomleft = tuple(map(operator.add,DISPLAYSURF.get_rect().bottomleft,(textrect.width,-2* textrect.height)))
        
        text2 = basicfont.render('Player 2', True, (0, 0, 0), WHITE) 
        textrect2 = text2.get_rect()
        textrect2.bottomright = tuple(map(operator.add,DISPLAYSURF.get_rect().bottomright,(-textrect2.width,-2 *textrect2.height)))

        pygame.draw.rect(DISPLAYSURF, selected_button_color, (textrect.centerx-textrect.width, textrect.centery-textrect.height, 2* textrect.width, 2* textrect.height))
        pygame.draw.rect(DISPLAYSURF, WHITE, (textrect2.centerx-textrect2.width, textrect2.centery-textrect2.height, 2* textrect2.width, 2* textrect2.height))
     
    if selected == 2:
        text = basicfont.render('Player 1', True, (0, 0, 0), WHITE)    
        textrect = text.get_rect()
        textrect.bottomleft = tuple(map(operator.add,DISPLAYSURF.get_rect().bottomleft,(textrect.width,-2* textrect.height)))
        
        text2 = basicfont.render('Player 2', True, (0, 0, 0), selected_button_color) 
        textrect2 = text2.get_rect()
        textrect2.bottomright = tuple(map(operator.add,DISPLAYSURF.get_rect().bottomright,(-textrect2.width,-2 *textrect2.height)))
        
        pygame.draw.rect(DISPLAYSURF, WHITE, (textrect.centerx-textrect.width, textrect.centery-textrect.height, 2* textrect.width, 2* textrect.height))
        pygame.draw.rect(DISPLAYSURF, selected_button_color, (textrect2.centerx-textrect2.width, textrect2.centery-textrect2.height, 2* textrect2.width, 2* textrect2.height))
     
    
    category = basicfont.render('Choose A Category', True, (255, 255, 255), NAVY)
    category_rect = category.get_rect()
    category_rect.midtop =  tuple(map(operator.add,DISPLAYSURF.get_rect().midtop,(0,3* category_rect.height)))
   
    rect_HEIGHT = HEIGHT/4
    rect_WIDTH = WIDTH/3
        
    pygame.draw.rect(DISPLAYSURF, WHITE, (DISPLAYSURF.get_rect().centerx - rect_WIDTH/2, DISPLAYSURF.get_rect().centery - rect_HEIGHT/2, rect_WIDTH, rect_HEIGHT), 0)
   
    DISPLAYSURF.blit(text, textrect)
    DISPLAYSURF.blit(text2, textrect2)
    DISPLAYSURF.blit(category, category_rect)
    pygame.time.delay(2000)
    pygame.display.update()
    
    #random_num = random.randint(2,5)
    category_arr = ["MTSU", "Entertainment", "Geography", "Science", "Random"]
    #for x in range(20):
        #
    
    button_press = False
    while button_press != True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    button_press = True
                    
        random_index = random.randint(0,4)
        
        name = display_category(category_arr[random_index])
        pygame.time.delay(200)    
        
    
    pygame.display.update()
    game_state = 3
    return game_state, name
    
def question_screen(game_state, category):
    DISPLAYSURF.fill(NAVY)
    temp = []
    questionFile = open(category + ".txt")
    for question in questionFile:
        temp.append(question)
    
    # Shuffle Array of Questions
    random.shuffle(temp)
    LIST = []
    index = 0
    for x in range(len(temp)):
        LIST += temp[index].split("?")
        index += 1
    
    i = 0
    for x in range(len(temp)):          
        print(LIST[i])
        print(LIST[i+1])
        i += 2
    
    player_color = (250, 128, 114)
    basicfont = pygame.font.SysFont(None, 75)     
    text = basicfont.render('Player 1', True, (255, 255, 255), player_color)    
    textrect = text.get_rect()
    textrect.bottomleft = DISPLAYSURF.get_rect().bottomleft
    
    text2 = basicfont.render('Player 2', True, (255, 255, 255), player_color)    
    textrect2 = text2.get_rect()
    textrect2.bottomright = DISPLAYSURF.get_rect().bottomright 
    
    
    categoryname = basicfont.render(category, True, (255, 255, 255), player_color)
    categoryrect = categoryname.get_rect()
    categoryrect.midtop = tuple(map(operator.add,DISPLAYSURF.get_rect().midtop,(0,3.5* categoryrect.height)))
    
    pygame.draw.rect(DISPLAYSURF, player_color, (textrect.centerx-textrect.width, textrect.centery-textrect.height, 2* textrect.width, 2* textrect.height))
    pygame.draw.rect(DISPLAYSURF, player_color, (textrect2.centerx-textrect2.width, textrect2.centery-textrect.height, 2* textrect2.width, 2* textrect2.height))
     
    
    DISPLAYSURF.blit(text, textrect)
    DISPLAYSURF.blit(text2, textrect2)
    DISPLAYSURF.blit(categoryname, categoryrect)
    
    basicfont = pygame.font.SysFont(None, 35)
    
    question = basicfont.render(LIST[0], True, (255, 255, 255), NAVY)
    questionrect = question.get_rect()
    questionrect.center = DISPLAYSURF.get_rect().center
    DISPLAYSURF.blit(question, questionrect)

    pygame.time.delay(2000)    
    pygame.display.update()
    
    
def runQuiz():
    # setup variables for the start of the game
    pygame.display.flip()
    CATEGORY = ["MTSU", "FUNNY", "RANDOM"]
    random.shuffle(CATEGORY)
    print(CATEGORY[0])
    
    # Store Questions in Temp Array
    temp = []
    questionFile = open(CATEGORY[0] + ".txt")
    for question in questionFile:
        temp.append(question)
    
    # Shuffle Array of Questions
    random.shuffle(temp)
    LIST = []
    index = 0
    for x in range(len(temp)):
        LIST += temp[index].split("?")
        index += 1
    
    i = 0
    for x in range(len(temp)):          
        print(LIST[i])
        print(LIST[i+1])
        i += 2

    board = getBlankBoard()
    score = 0
    
  
    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render(textwrap, True, (255, 255, 255))
    
    textrect = text.get_rect()
    textrect.centerx = DISPLAYSURF.get_rect().centerx
    textrect.centery = DISPLAYSURF.get_rect().centery
    
    DISPLAYSURF.blit(text, textrect)
     
    pygame.display.update()

def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

main()