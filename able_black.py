from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard
from pynput import mouse
import time
import numpy

keyboardcont = KeyboardController()
mousecont = MouseController()

# secondDelay = 0.040
secondDelay = 0.001 #default script period

capsdown = 0
capstimer = 0
G8Down = 0
G5Down = 0
ctrlDown = 0


def on_press(key):
	global G8Down
	global G5Down
	global capsdown
	global capstimer
	global ctrlDown
	# print(key.__dict__)
	try:

		# if key.vk == 269025095: # F15 or g8 g602 mouse button
		# 	print("debug")
		# 	keyboardcont.press(Key.ctrl)
		# 	keyboardcont.press(Key.alt)
		# 	keyboardcont.press('d')
		# 	keyboardcont.release('d')
		# 	keyboardcont.release(Key.alt)
		# 	keyboardcont.release(Key.ctrl)

		if key == Key.alt_gr: #capslock which is remapped to alt_gr by xmodmap
			capsdown = 1

		if key != Key.alt_gr:
			capstimer = 9e9 #disable enter function
		if key.vk == 269025094: # F15 or g8 g602 mouse button
			G8Down = 1
		if key.vk == 269025096: # F17 g5 g602 mouse button
			G5Down = 1
		if capsdown:
			# print("debug")
			if key.vk == 114: # r
				# print("debug")
				keyboardcont.press(Key.ctrl)
				keyboardcont.press(Key.tab)
				keyboardcont.release(Key.tab)
				keyboardcont.release(Key.ctrl)
			if key.vk == 101: # e
				# print("debug")
				keyboardcont.press(Key.ctrl)
				keyboardcont.press(Key.shift)
				keyboardcont.press(Key.tab)
				keyboardcont.release(Key.tab)
				keyboardcont.release(Key.shift)
				keyboardcont.release(Key.ctrl)
			if key.vk == 102: # f
				# print("debug")
				keyboardcont.press(Key.ctrl)
				keyboardcont.press('w')
				keyboardcont.release('w')
				keyboardcont.release(Key.ctrl)

	except AttributeError:
		a=5
		if key == Key.ctrl:
			ctrlDown = 1

def on_release(key):
	global G8Down
	global G5Down
	global capsdown
	global capstimer
	global ctrlDown
	try:

		a=5
		if key == Key.alt_gr: #capslock which is remapped to alt_gr by xmodmap
			capsdown = 0
			if capstimer*secondDelay < 0.150:
				keyboardcont.press(Key.enter)
				keyboardcont.release(Key.enter)
				# print(secondDelay)
		if key.vk == 269025094:
			G8Down = 0
		if key.vk == 269025096:
			G5Down = 0

	except AttributeError:
		if key == Key.ctrl:
			ctrlDown = 0
		a=5




listener = keyboard.Listener(
	on_press=on_press,
	on_release=on_release)
listener.start()


while True:

	# print(ctrlDown)
	if capsdown == 1: #if caps is held down, increment timer variable
		capstimer += 1
	else:
		capstimer = 0 #reset timer variable



	if G8Down:
		scrollCoeff = 0.5
		secondDelay = 0.040
		if G5Down:
			scrollCoeff = 5
			secondDelay = 0.001
		# scaleLimit = 1000

		# print(tuple(numpy.subtract(mousecont.position, mousePosLast)))
		scrollDiffTuple = tuple(numpy.subtract(mousePosLast,mousecont.position))
		# dx = -1*numpy.clip(scrollDiffTuple[0]/scrollCoeff,-scaleLimit,scaleLimit)
		# dy = numpy.clip(scrollDiffTuple[1]/scrollCoeff,-scaleLimit,scaleLimit)
		dx = -0.5*scrollDiffTuple[0]*scrollCoeff
		dy = scrollDiffTuple[1]*scrollCoeff
		mousecont.scroll(dx,dy)
		# print(dy)

		mousecont.position = mousePosLast

	else:
		mousePosLast = mousecont.position
		secondDelay = 0.001


	# capsdownlast = capsdown
	# print(capsdown)
	# print("LOOP")
	time.sleep(secondDelay) # run every secondDelay ms
	# mousecont.move(30, -30)

	#Read pointer position
	# print('The current pointer position is{0}'.format(mousecont.position))
	# print(mousecont.position)





	# listener.stop()
