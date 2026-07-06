"""

 The Game of Life for exhibitions

 (c) Harold Thimbleby, July 2026
 Email harold@thimbleby.net
 ----

 As configured, this code currently runs two styles of Games of Life:
 - a random set up
 - a selection of well known life forms, like Gosper's glider gun
 - it is easy to specify more life forms...

 typically you will record this program output, then put the video on a loop
 or you can modify the code to run endlessly
 (then TVs can play a USB stick MP4 just by being powered up - they don't need booting)
 
 ---
 
 You may modify and use this code in any not for profit reasonable legal way
 Acknowledgement would be appreciated
 More details, subject to the terms of the Academic Free License 3.0
 https://opensource.org/license/AFL-3.0
 
"""

import sys
import time
import random
import pygame
#import copy
#import os

from pygame.locals import *

#os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
#info = pygame.display.Info()
#screen_width, screen_height = info.current_w, info.current_h

pygame.font.init()
pygame.display.set_mode(size = (1920, 1080), flags = pygame.SCALED) #FULLSCREEN)
pygame.display.update()
screen = pygame.display.get_surface()

h = 29 # cells to display vertically
w = 49 # cells to display horizontally
border = 2 # rows/columns out of sight each side & top/bottom
fullHeight = h+2*border
fullWidth = w+2*border
# there is a half cell width/height gap all the way round the grid
cellwd = round(screen.get_width() / w)
cellht = round(2*screen.get_height() / h) # 2* to fix bug with Raspberry pi screen height half the size it should be

print(f"Resolution = {fullWidth} x {fullHeight} cells")
print(f"Resolution = {screen.get_width()} x {screen.get_height()} pixels")
print(f"Cell size = {cellwd} x {cellht} pixels")
print(f"pygame.display.get_desktop_sizes() = {pygame.display.get_desktop_sizes()}")
print(f"... as you can see I haven't worked out why the Raspberry pi seems to have a half height monitor!")
#sys.exit(0)

boldFont = pygame.font.SysFont(None, 35, bold=True) # None is "freesans"
normalFont = pygame.font.SysFont(None, 25)
titleFont = pygame.font.SysFont(None, 200, bold=True)
subtitleFont = pygame.font.SysFont(None, 80, bold=True)
sciartFont = pygame.font.SysFont(None, 60)

# NB not all colors used are defined here
whiteColor = (255, 255, 255)
blankBoardColor = (75, 75, 255)
gridColor = whiteColor
blackColor = (0, 0, 0)
explainColor = (255, 255, 200)

def screenCoords(x, y): # convert grid coordinates to screen coordinates
	""" Transform grid (x,y) coordinates to integer pygame coordinates. """
	return (int((0.5+x-border)*cellwd), int((0.5*y-border/2)*cellht))

historyDepth = 5

gridHistory = [
				[
				  [0 for col in range(fullHeight)] for row in range(fullWidth)
				] for i in range(historyDepth)
			  ]
			  
gridHistoryPointer = 0

def nextHistory():
	""" Increment gridHistoryPointer so the history list is treated as a ring. """
	global grid, ngrid, gridHistory, gridHistoryPointer
	grid = gridHistory[gridHistoryPointer]
	gridHistoryPointer += 1
	if gridHistoryPointer == historyDepth: gridHistoryPointer = 0
	ngrid = gridHistory[gridHistoryPointer]
	for x in range(fullWidth):
		for y in range(fullHeight):
			ngrid[x][y] = 0 
	 
nextHistory() # initialise the history vector

print(f"size of grid History = {len(gridHistory)}")

def equalGrids(a): # only compare what the user can see (exclude the borders)
	""" Return if the current grid is in the history list, obviously excluding itself. """
	global grid
	if a == grid: 
		return False  # don't test a==grid
	for x in range(border, fullWidth-border):
		for y in range(border, fullHeight-border):
			if (a[x][y] > 0) != (grid[x][y] > 0): return False
	return True

def isRepeated(): # NB this won't detect cycles longer than {historyDepth-1}
	""" Does the current grid appear anywhere in the gridHistory ring? """
	global gridHistory, historyDepth, gridHistoryPointer
	for i in range(historyDepth):
		if equalGrids(gridHistory[i]): 
			return True
	return False

def say(sayThis, centre, color, font=boldFont):
	""" Display text at given coordinates etc. """
	text = font.render(sayThis, True, color)
	x, y = centre
	screen.blit(text, screenCoords(x+border, y+border))

image = [0]*20
maxImageIndex = len(image)-1
for i in range(1, maxImageIndex + 1):
    path = f"images/blend{i}.png"
    try:
        surf = pygame.image.load(path).convert_alpha()
        surf = pygame.transform.smoothscale(surf, (int(0.8 * cellwd), int(0.8 * cellwd)))
    except Exception as e:
        print(f"Warning: failed to load image {path}: {e}. Displaying a fallback rectangle instead...")
        surf = pygame.Surface((int(0.8 * cellwd), int(0.8 * cellwd)), flags=pygame.SRCALPHA)
        surf.fill((200, 200, 255, 255))
    image[i] = surf

initialScreen = [			   
		(3, 21), # blinker
		(3, 22),
		(3, 23),
		   
		(3, 16), # block
		(4, 16),
		(3, 17),
		(4, 17),

		(40, 12), (41, 12), # beacon
		(40, 13),
									(43, 14),
						  (42, 15), (43, 15),

		(40, 21), (41, 21), (42, 21), # toad
				  (41, 22), (42, 22), (43, 22)
	]

glider = [
	(22, 8), # Gosper Glider Gun
		(12, 7),
		(36, 7),
		(17, 9),
		(11, 8),
		(1, 9),
		(25, 4),
		(2, 8),
		(16, 7),
		(25, 10),
		(21, 6),
		(23, 9),
		(14, 6),
		(36, 6),
		(22, 7),
		(14, 12),
		(17, 8),
		(11, 10),
		(25, 9),
		(35, 7),
		(1, 8),
		(18, 9),
		(22, 6),
		(21, 8),
		(23, 5),
		(12, 11),
		(17, 10),
		(11, 9),
		(35, 6),
		(25, 5),
		(2, 9),
		(13, 6),
		(13, 12),
		(15, 9),
		(16, 11),
		(21, 7)
]

pentad = [				  (11, 19), # Penta-decathlon
				  (12, 18), (12, 19), (12, 20),
		(13, 17), (13, 18), (13, 19), (13, 20), (13, 21),
		(20, 17), (20, 18), (20, 19), (20, 20), (20, 21),
				  (21, 18), (21, 19), (21, 20),
							(22, 19)
	]

byflops = [						 (4, 1),
					(2, 2),		 (4, 2),
													(6, 3),
			(1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
													(6, 5),
					(2, 6),		 (4, 6),
									(4, 7)
	]

beehive = [
			(2, 1), (3, 1),
	 (1, 2),				(4, 2),
			(2, 3), (3, 3)
	]

plotcount = 0
explainSteps = [0 for i in range(8)]

def lifeForm(life, xoffset, yoffset):
	""" Initialise grid[] with a life form, offset in x and y directions as necessary. """
	for i in life:
		x, y = i
		grid[x+border+xoffset][y+border+yoffset] = 1
		plot()
		pygame.display.flip()
		time.sleep(.02)

def prePlanned():
	""" Initialise grid[] with defined life forms. """
	# all the numbers were defined before I thought of the invisible borders
	# hence the x and y offsets...
	lifeForm(initialScreen, 0, -3)
	lifeForm(pentad, -2, +2)
	lifeForm(glider, +2, -2)
	lifeForm(byflops, +24, +20)
	lifeForm(beehive, +41, +3)

def randomise():
	""" Initialise grid[] with random living cells. """
	# Why the 37.5% Density is the Sweet Spot
	# Maximized Lifespan: Simulations show that randomly generated boards peak
	# in both average lifespan and total population size when initial density
	# sits within the 37%-38% range. The "Edge of Chaos": If the density is too
	# low (<10%), the board quickly dies out. If the density is too high (>90%),
	# it quickly chokes itself into a dense, unchanging block. The 37.5%
	# threshold sits perfectly at the boundary — allowing complex interactions
	# to build, merge, and propagate. Emergent Gliders: This density produces
	# the perfect balance of empty space and active cells required for
	# spaceships, glider guns, and puffers to form naturally.
	for y in range(fullHeight-1, -1, -1):
		for x in range(fullWidth):
			r = random.random() # 0-1 real
			if r < 0.375:
				grid[x if y%2 == 0 else w-1-x][y] = 1
				plot()
				pygame.display.flip()
				time.sleep(.0001)

def round_rect(surf, rect, rad, color, edge):
	""" Display a round rectangle with a border to display a banner on the screen. """
	if rad > rect.width/2 or rad > rect.height/2:
		rad = min(rect.width/2, rect.height/2)

	r = rect.inflate(-rad*2, -rad*2)
	for corner in (r.topleft, r.topright, r.bottomleft, r.bottomright):
		pygame.draw.circle(surf, color, corner, rad)
	pygame.draw.rect(surf, color, r.inflate(rad*2, 0))
	pygame.draw.rect(surf, color, r.inflate(0, rad*2))
	if edge: # helpful when smaller explanations overlap (eg glider on top of Gosper gun)
		edgeColor = whiteColor #blankBoardColor
		pygame.draw.circle(surf, edgeColor, r.topleft, rad, width=2, draw_top_left=True)
		pygame.draw.circle(surf, edgeColor, r.topright, rad, width=2, draw_top_right=True)
		pygame.draw.circle(surf, edgeColor, r.bottomleft, rad, width=2, draw_bottom_left=True)
		pygame.draw.circle(surf, edgeColor, r.bottomright, rad, width=2, draw_bottom_right=True)
		pygame.draw.line(surf, edgeColor, (r.left, r.top-rad), (r.right, r.top-rad), width=2)
		pygame.draw.line(surf, edgeColor, (r.left, r.bottom+rad), (r.right, r.bottom+rad), width=2)
		pygame.draw.line(surf, edgeColor, (r.left-rad, r.top), (r.left-rad, r.bottom), width=2)
		pygame.draw.line(surf, edgeColor, (r.right+rad, r.top), (r.right+rad, r.bottom), width=2)

def explain(sayThis, topleft, widthheight, font=boldFont, edge=True):
	""" Provide (typically) the name of a life form on the screen. """
	round_rect(screen, pygame.Rect(screenCoords(topleft[0]-.7+border, topleft[1]+border),
								   screenCoords(widthheight[0]+border, widthheight[1]+.2+border)),
								   cellwd/2,
								   (0.95*blankBoardColor[0], 0.95*blankBoardColor[1], 0.95*blankBoardColor[2]),
								   edge=edge)
	say(sayThis, (topleft[0]-.5, topleft[1]+.3), explainColor, font=font)

def drawblankboard():
	screen.fill(blankBoardColor)

def drawgrid():
	""" Draw the gridColor grid. """
	for x in range(border, fullWidth-border):
		pygame.draw.line(screen, gridColor,
						 screenCoords(x, border), screenCoords(x, h+border))
	for y in range(border, fullHeight-border+1):
		pygame.draw.line(screen, gridColor,
						 screenCoords(border-0.5, y-0.5), screenCoords(w+border, y-0.5))

def explainGlider(xo, yo):
	""" If there are enough live cells in a 3x4 matrix, label the location as a glider. """
	global grid
	n = 0
	for x in range(xo, xo+3):
		for y in range(yo, yo+4):
			if grid[x][y]:
				n += 1
	if n == 5:
		explain("Glider", (xo-border, yo-border-1), (3, 5))
		return True
	return False

def exp(n, theExplanation):
	""" Provide the nth explanation. """
	# explainSteps[] counts how long each explanation stays up
	# explainCount[] counts how many times each explanation has been used
	global explainSteps, explainCount
	if explainSteps[n]:
		explainSteps[n] = explainSteps[n]-1
		explainCount[n] = explainCount[n]+1
		theExplanation()

which = 0
def explanations():
	global plotcount

	# there are 6 explanations, plus 2 glider explanations
	global explainSteps # how many steps to display this explanation for
	global explainCount # how many times this explanation has been used
	global which # take explanations in turn

	displayFor = 7
	plotcount += 1
	
	defaultEdge = True

	if plotcount%7 == 0:
		explainSteps[which] = displayFor
		which += 1
		if which >= len(explainSteps): which = 0

	exp(0, lambda:  explain("Penta-decathlon", (7, 17), (16, 9)))
	exp(1, lambda:  explain("Block", (3, 12), (2, 3)))
	exp(2, lambda:  explain("Beacon", (40, 8), (4, 5)))
	exp(3, lambda: (explain("Traffic", (2, 16), (3, 5)),
					explain("lights", (2.1, 17), (2.8, 3), edge=False)))
	exp(4, lambda: (explain("Bill Gosper's glider gun", (3, 1), (36, 10)),
					explain("Gliders are fired out of the bottom", (3.1, 2), (24, 8), font=normalFont, edge=False)))
	exp(5, lambda:  explain("Toad", (40, 16), (4, 5)))
	exp(6, lambda:  explain("Byflops", (25, 20), (6, 8)))		 
	exp(7, lambda:  explain("Beehive", (42, 3), (4, 4)))
	
	if explainGlider(28, 13): 
		explainCount[8] = explainCount[8]+1	   
	if explainGlider(32, 17): 
		explainCount[9] = explainCount[9]+1
	if explainGlider(38, 23): 
		explainCount[10] = explainCount[10]+1
	
def plot(doExplanations=False):
	drawblankboard()
	drawgrid()
	if( doExplanations ): 
		explanations()
	for y in range(border, fullHeight-border):
		for x in range(border, fullWidth-border):
			if grid[x][y]:
				screen.blit(image[grid[x][y]], screenCoords(x+.6-1, y+.2-.1))
				
def nextgrid():
	global maxImageIndex
	for y in range(1, fullHeight-1):
		for x in range(1, fullWidth-1):
			n = 1 if grid[x-1][y-1] else 0
			if grid[x][y-1]: n += 1
			if grid[x+1][y-1]: n += 1
			if grid[x-1][y]: n += 1
			if grid[x+1][y]: n += 1
			if grid[x-1][y+1]: n += 1
			if grid[x][y+1]: n += 1
			if grid[x+1][y+1]: n += 1

			if grid[x][y]:
				if n < 2 or n > 3:
					ngrid[x][y] = 0
				else:
					ngrid[x][y] = grid[x][y]+1
					if ngrid[x][y] > maxImageIndex: ngrid[x][y] = maxImageIndex
			else: 
				ngrid[x][y] = 1 if n == 3 else 0

def blend(f, c1, c2): # blend two colors c1 & c2 in proportions f and 1-f respectively
	return (f*c1[0]+(1-f)*c2[0], f*c1[1]+(1-f)*c2[1], f*c1[2]+(1-f)*c2[2])
   
fadeSteps = 100

def start(randomised):
	for x in range(fullWidth):
		for y in range(fullHeight):
			grid[x][y] = 0
			
	screen.fill(blackColor)
	pygame.display.flip()
	time.sleep(1)
	
	for i in range(fadeSteps, -1, -1):
		f = i/fadeSteps
		screen.fill(blend(f, blackColor, blankBoardColor))
		say("The Game of Life", (10, 5),
				blend(f, (255, 255, 0), blankBoardColor), font=titleFont)
		say("Science + Art  =", (18, 27),
				blend(f, (100, 255, 100), blankBoardColor), font=sciartFont)
		say("Sciart", (26.5, 27),
				blend(f, (255, 255, 200), blankBoardColor), font=sciartFont)
		if randomised:
			say("Starting life with a random world", (13.5, 13),
				blend(f, (230, 230, 230), blankBoardColor), font=subtitleFont)
		else:
			say("Starting life with a few pre-planned life forms", (9.5, 13),
				blend(f, (230, 230, 230), blankBoardColor), font=subtitleFont)
		pygame.draw.line(screen, blend(f, (255, 155, 155), blankBoardColor),
						 screenCoords(28.15, 16.5) if randomised else screenCoords(26.9, 16.75),
						 screenCoords(33.15, 16.5) if randomised else screenCoords(34.9, 16.75),
						 width = 6)
		pygame.display.flip()
		time.sleep(5 if i == fadeSteps else .02)
 
	if False: # to check screen typography
		pygame.quit()
		sys.exit(0)

	drawgrid()
	pygame.display.flip()
	if randomised:
		randomise()
	else:
		prePlanned()
	
def end():
	for i in range(fadeSteps):
		screen.fill(blend(i/fadeSteps, blackColor, blankBoardColor))
		pygame.display.flip()
		time.sleep(.02)
	
def main():	
	global explainCount
	pygame.mouse.set_visible(False)
	counter = 0
	demoSchedule = [False, True] # True means random game; False means preplanned game
	for randomised in demoSchedule:
		explainCount = [0 for i in range(11)]
		start(randomised)
		repeatCountDown = 0
		try:
			fullbreak = False
			limit = 300 # limit max iterations as isRepeated() can't detect cycles longer than {historyDepth-1}
			while True:
				limit -= 1
				if limit <= 0:
					print("Stopped by hitting max limit of iterations")
					break;
				counter += 1
				plot(doExplanations = not randomised)
				nextgrid()
				nextHistory()
				pygame.display.flip()
				events = pygame.event.get()
				for event in events:
					if event.type == pygame.KEYDOWN:
						print("Stopped by keydown event")
						fullbreak = True
						break
				if fullbreak: 
					break
				if randomised:
					if not repeatCountDown and isRepeated():
						repeatCountDown = 10
				else:
					stopAfterExplanations = True
					limit = 5
					for i in explainCount:
						if i < limit:
							stopAfterExplanations = False
							break
					if stopAfterExplanations:   
						print(f"Stopped by all life forms explained at least {limit} time(s)")
						print(f"explainCount={explainCount}")
						break
				if repeatCountDown:
					repeatCountDown -= 1
					if not repeatCountDown: 
						print("Stopped by repeating pattern")
						break;
				time.sleep(0.1 if randomised else 0.5)

			end()
			
		except KeyboardInterrupt:
			print("Interrupted run!")
	
	pygame.display.flip()
	time.sleep(.0) # set it to >0 to make it easy to trim if necessary
	pygame.quit()
	print(f"{counter} runs, averaging {counter/len(demoSchedule)} runs per demo")
	print(f"Full game size = {fullHeight*fullWidth} cells")
	sys.exit(0)
	
main()

