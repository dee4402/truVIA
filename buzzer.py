import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO
import random, time, pygame, sys
from pygame.locals import *
import pygame.mixer

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT =768
#Color set

#               R    G    B
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

##Setting up pins 
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT ))
pygame.display.set_caption('Buzzers!')
BLACK= (0, 0, 0)
BLUE = ( 77, 162, 183  )


boyImage= pygame.image.load('boy.png')
boxx = 10
boyy = 10

buzzerObj = pygame.mixer.Sound('buzzer_x.wav')

while True: # main game loop
    
    boxx = 200
    boyy = 150
    
    DISPLAYSURF.fill(BLUE)
    
    
        
    DISPLAYSURF.blit(boyImage, (boxx, boyy))
    
    teamAButton = GPIO.input(17)
    if teamAButton == GPIO.LOW:
        buzzerObj.play(loops=-1)
        time.sleep(1)
        #while (teamAButton == GPIO.LOW):
        #   time.sleep(.1)
        buzzerObj.stop()
        
        
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update() 

