#IBM Plex Mono Text, Menlo, Consolas, DejaVu Sans Mono, monospace,
import time
import keyboard
import pynput
import numpy
import pyperclip
import subprocess
from datetime import datetime
import easygui

mousecont = pynput.mouse.Controller()

secondDelayDefault = 0.08
secondDelay = secondDelayDefault

time_list = []
last_state = ''




def key_happened(event_object):
    #this function is called whenever a key is pressed, held down, or released
    #

    # print(event_object.__dict__)
    global caps_down_time
    global last_state

    #keyboard.hook cannot distinguish between a just-pressed or held down button
    #work around: if state (up,down) or name of key have changed since last
    #time, it is a rising edge
    #if the state is up, falling edge is assured
    if (event_object.name + event_object.event_type) != last_state:
        rising_edge = True
    else:
        rising_edge = False

    # change tab shortcuts in firefox adapted to caps+r,e,f
    if keyboard.is_pressed('caps lock'):
        if event_object.event_type == 'down':
            if event_object.name == 'r':
                keyboard.press_and_release('ctrl+tab')
            elif event_object.name == 'e':
                keyboard.press_and_release('ctrl+shift+tab')
            elif event_object.name == 'f':
                keyboard.press_and_release('ctrl+w')
            elif event_object.name == 'alt':
                time.sleep(0.75)
                keyboard.press_and_release('ctrl+c')
                time.sleep(0.75)
                with open('/home/main/.clip.txt','a') as clipfile:
                    clipfile.write(pyperclip.paste() + '\n' + str(datetime.now()) + '\n')
                easygui.msgbox('copied ' + pyperclip.paste(), title="real good stuff")
            #elif event_object.name == 'v':
            #    subprocess.run('mousepad /home/main/.clip.txt', shell=True)

    #tapping caps without hitting anything else sends 'enter'
    if event_object.name == 'caps lock':
        if event_object.event_type == 'down':
            if rising_edge:
                caps_down_time = event_object.time
            else:
                caps_down_time = 2
        if event_object.event_type == 'up':
            if (event_object.time - caps_down_time) < 0.15:
                keyboard.press_and_release('enter')

    if keyboard.is_pressed(185) or \
        keyboard.is_pressed(186) or \
        keyboard.is_pressed(187) or \
        keyboard.is_pressed(191):
        # print('yes')
        pass


    last_state = event_object.name + event_object.event_type


# This function is called every time a key is presssed
keyboard.hook(key_happened)
# Create a loop to keep the application running
while True:

    if keyboard.is_pressed(185) or keyboard.is_pressed(187): #G8 button
        # print('g8 pressed')
        scrollCoeff = 0.5
        secondDelay = 0.040

        scrollDiffTuple = tuple(numpy.subtract(mousePosLast,mousecont.position))
        dx = scrollDiffTuple[0]
        dy = scrollDiffTuple[1]

        #mouse gestures
        if keyboard.is_pressed(187):
            # print(dx)
            if dx > 10:
                keyboard.press_and_release('ctrl+shift+tab')
                time.sleep(.3)
            elif dx < -10:
                keyboard.press_and_release('ctrl+tab')
                time.sleep(.3)
            elif dy < -10:
                keyboard.press_and_release('ctrl+w')
                time.sleep(.3)
            elif dy > 10:
                keyboard.press_and_release('ctrl+shift+t')
                time.sleep(.3)

        if keyboard.is_pressed(185):
            #drag to scroll
            dx = -0.5*scrollDiffTuple[0]*scrollCoeff
            dy = scrollDiffTuple[1]*scrollCoeff
            mousecont.scroll(dx,dy)



        mousecont.position = mousePosLast

    else:
        mousePosLast = mousecont.position
        secondDelay = secondDelayDefault

    time.sleep(secondDelay) # run every secondDelay ms
