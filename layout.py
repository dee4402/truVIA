import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO
import random, time, pygame, sys
from pygame.locals import *
#This is a sample layout of what we thought the game should look like
# We added buzzer functionality to it for each player. 
import pygame.mixer

WIDTH = 1020
HEIGHT = 768

BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'
XMARGIN = int((640 - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = 480 - (BOARDHEIGHT * BOXSIZE) - 5

#GPIO.add_event_detect(17, GPIO.FALLING)
#PIO.add_event_detect(27, GPIO.FALLING)

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
LIGHT_PINK  = (236, 240, 241)
PASTELGREEN = (46, 204, 113 )
           
BORDERCOLOR = ( 244, 246, 247 ) 
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
XAxis = 300
YAxis = 200
#Buzzer Sound 


def main():
    #Controllng buffer to prevent delay. Can keep changing buffer
    # to adjust the quality of the sound. Keeping it from running out
    #sound samples
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    
    #pygame.joystick.init()
    #joystick = pygame.joystick.Joystick(0)

    

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    buzzerObj1 = pygame.mixer.Sound('buzzer_x.wav')
    buzzerObj2 = pygame.mixer.Sound('buzzer_x.wav')
##    buzzerChannelObj = pygame.mixer.Channel('buzzer_x.wav')


    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:

        teamBButton = GPIO.input(24)
        teamAButton = GPIO.input(17)
        DISPLAYSURF.fill(NAVY)

        #scoreImg = BASICFONT.render(str(score), 1, SCORECOLOR)
        #scoreRect = scoreImg.get_rect()
        #scoreRect.bottomleft = (10, WINDOWHEIGHT - 6)
        #DISPLAYSURF.blit(scoreImg, scoreRect)
    

   # DISPLAYSURF.fill(PEACH)
        pygame.draw.rect(DISPLAYSURF, PEACH, (0,0,230,768))
        pygame.draw.rect(DISPLAYSURF, ORANGE, (790,0,230,768))
        pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)

        for event in pygame.event.get():
            if event.type == 17:
                buzzerObj1.play()

        #pygame.draw.circle(DISPLAYSURF, WHITE, 230, 50, 0)

    #For buzzer A

        if teamAButton == GPIO.LOW:
            pygame.draw.rect(DISPLAYSURF,LIGHTGREEN, (0,0,230,768))
            buzzerObj1.play()
        else:
            buzzerObj1.stop()
    #For buzzer B
        
        if teamBButton == GPIO.LOW:
            pygame.draw.rect(DISPLAYSURF,LIGHTGREEN, (790,0,230,768))
            buzzerObj2.play()
        else:
            buzzerObj2.stop()
        
    
            
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    
    
main()