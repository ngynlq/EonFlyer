import pygame
from pygame.locals import *
import Menu
from sys import exit
WHITE = (255,255,255)
BLACK = (0,0,0)
def joyToKey(joystick,keys):
    temp = {}
    temp[K_z] = False
    temp[K_x] = False
    temp[K_DOWN] = False
    temp[K_UP] = False
    temp[K_RIGHT] = False
    temp[K_LSHIFT] = False
    temp[K_LEFT] = False
    temp[K_ESCAPE] = False
    horiz_axis_pos = joystick.get_axis(0)
    vert_axis_pos = joystick.get_axis(1)
    if vert_axis_pos < 0:
        temp[K_UP] = True
    if vert_axis_pos > 0:
        temp[K_DOWN] = True
    if horiz_axis_pos > 0:
        temp[K_RIGHT] = True
    if horiz_axis_pos <0:
        temp[K_LEFT] = True
    if joystick.get_button(0):
        temp[K_z] = True
    if joystick.get_button(1):
        temp[K_x] = True
    if joystick.get_button(2):
        temp[K_LSHIFT] = True
    if keys[K_UP]:
        temp[K_UP] = True
    if keys[K_DOWN]:
        temp[K_DOWN] = True
    if keys[K_LEFT]:
        temp[K_LEFT] = True
    if keys[K_RIGHT]:
        temp[K_RIGHT] = True
    if keys[K_z]:
        temp[K_z] = True
    if keys[K_x]:
        temp[K_x] = True
    if keys[K_LSHIFT]:
        temp[K_LSHIFT] = True
    if keys[K_ESCAPE]:
        temp[K_ESCAPE] = True
    horiz_axis_pos = (0,0)
    vert_axis_pos = (0,0)
    return temp
def main():
    screen = pygame.display.set_mode((1024,768),0,32)
    pygame.init()
    pygame.display.set_caption("EON FLYER")
    onGoing = True
    error = False
    window = Menu.Menu()
    joystick_count = pygame.joystick.get_count()
    if joystick_count > 0:
        my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()
        
    while onGoing:
            keys = pygame.key.get_pressed()
            if joystick_count > 0:
                keys = joyToKey(my_joystick,keys)
            window.control(keys)
            window.update(screen)
            pygame.display.flip()
            if window.newControl(keys):
                if window.nextControl() == False:
                    onGoing = False
                else:
                    window = window.nextControl()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    onGoing = False
    pygame.quit()
    exit()   
if __name__ == "__main__":
    main()

        
