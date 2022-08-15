from random_word import RandomWords 
import cs112_f19_week11_linter
import math, copy, random
import os
import string

from cmu_112_graphics import *
from tkinter import *
from PIL import Image    

def distance (x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)
 
#referenced from 
#https://www.guru99.com/reading-and-writing-files-in-python.html
#with modifications
def leaderBoard(score):
    path = "leaderboard.txt"
    fileId = open(path, 'a')
    fileId.write(f'{score}' + '\n')
    fileId.close()
    fileId = open(path, 'r')
    if fileId.mode == 'r':
        readFile = fileId.read()
    leaderboard = readFile
    return leaderboard
 
class Player():
    def __init__(self, mode, cx, cy, rotate = 0):
        self.mode = mode
        self.rotate = rotate
        self.cx = cx
        self.cy = cy
        #referenced from: 
        #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        #with modifications
        playerImage = self.mode.loadImage('TP_ships.png')
        playerStrip = self.mode.scaleImage(playerImage, 1/2)
        x0, y0 = 0, 0
        x1, y1 = 100, 150
        self.ship = playerStrip.crop((x0, y0, x1, y1))
        self.ship = self.mode.scaleImage(self.ship, 1/2)
        self.ship = self.ship.rotate(self.rotate)
        

    #referenced from: 
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    #with modifications 
    def getBounds(self):
        # returns absolute bounds, not taking scrollX into account
        (x0, y0) = (self.cx - 20, 
                    self.cy - self.mode.scrollY - 40)
        (x1, y1) = (x0 + 40, y0 + 80)
        return (x0, y0, x1, y1)
    
    #Copied from 
    #https://www.cs.cmu.edu/~112/notes/
    #notes-animations-part2.html#cachingPhotoImages
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage
        
    def draw(self, canvas):
        photoImage = self.getCachedPhotoImage(self.ship)
        canvas.create_image(self.cx, self.cy - self.mode.scrollY, 
                            image = photoImage)
 
class Enemy():
    def __init__(self, mode, cx, cy):
        self.mode = mode
        self.cx = cx
        self.cy = cy
        self.rotate = 0
        self.x0, self.y0 = 55, 1580
        self.x1, self.y1 = 115, 1650
        #referenced from: 
        #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        #with modifications
        enemyImage = self.mode.loadImage('TP_ships.png')
        enemyStrip = self.mode.scaleImage(enemyImage, 2/3)
        self.enemyShip = enemyStrip.crop((self.x0, self.y0, self.x1, self.y1))
        self.enemyShip = self.mode.scaleImage(self.enemyShip, 2/3)
        self.word = ''

    def getHashables(self):
        return (self.cx, self.cy, self.word) 
 
    def __hash__(self):
        return hash(self.getHashables())
 
    def __eq__(self, other):
        return (isinstance(other, Enemy) and 
                self.cy == other.cy and self.cx == other.cx and
                self.word == other.word) 
    
    #referenced from: 
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    #with modifications 
    def getBounds(self):
        # returns absolute bounds, not taking scrollX into account
        (x0, y0) = (self.cx - (self.x1 - self.x0) / 2, 
                    self.cy - (self.y1 - self.y0) / 2)
        (x1, y1) = (self.cx, self.cy)
        return (x0, y0, x1, y1)

    #Copied from 
    #https://www.cs.cmu.edu/~112/notes/
    #notes-animations-part2.html#cachingPhotoImages
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage
 
    def draw(self, canvas):
        #Following 1 line copied from 
        #https://www.cs.cmu.edu/~112/notes/
        #notes-animations-part2.html#cachingPhotoImage
        photoImage = self.getCachedPhotoImage(self.enemyShip)
        canvas.create_image(self.cx, self.cy - self.mode.scrollY, 
                            image = photoImage)
 
        canvas.create_text(self.cx, self.cy - self.mode.scrollY,
                            text = self.word, fill = 'light green', 
                            font = 'Times 25')
 
class Index(Enemy):
    def __init__(self, mode, cx, cy):
        super().__init__(mode, cx, cy)
        self.rotate = 0
        self.mode = mode
        self.cx = cx
        self.cy = cy
        self.x0, self.y0 = 55, 900
        self.x1, self.y1 = 115, 1050
        enemyImage = self.mode.loadImage('TP_ships.png')
        enemyStrip = self.mode.scaleImage(enemyImage, 2/3)
        self.enemyShip = enemyStrip.crop((self.x0, self.y0, self.x1, self.y1))
        self.enemyShip = self.mode.scaleImage(self.enemyShip, 2/3)
     
class Middle(Enemy):
    def __init__(self, mode, cx, cy):
        super().__init__(mode, cx, cy)
        self.rotate = 0
        self.mode = mode
        self.cx = cx
        self.cy = cy
        self.x0, self.y0 = 50, 1050
        self.x1, self.y1 = 120, 1200
        enemyImage = self.mode.loadImage('TP_ships.png')
        enemyStrip = self.mode.scaleImage(enemyImage, 2/3)
        self.enemyShip = enemyStrip.crop((self.x0, self.y0, self.x1, self.y1))
        self.enemyShip = self.mode.scaleImage(self.enemyShip, 2/3)
        
class Ring(Enemy):
    def __init__(self, mode, cx, cy):
        super().__init__(mode, cx, cy)
        self.rotate = 0
        self.mode = mode
        self.cx = cx
        self.cy = cy
        self.x0, self.y0 = 30, 1380
        self.x1, self.y1 = 135, 1500
        enemyImage = self.mode.loadImage('TP_ships.png')
        enemyStrip = self.mode.scaleImage(enemyImage, 2/3)
        self.enemyShip = enemyStrip.crop((self.x0, self.y0, self.x1, self.y1))
        self.enemyShip = self.mode.scaleImage(self.enemyShip, 2/3)
 
class Pinky(Enemy):
    def __init__(self, mode, cx, cy):
        super().__init__(mode, cx, cy)
        self.rotate = 0
        self.mode = mode
        self.cx = cx
        self.cy = cy  
        self.x0, self.y0 = 20, 1750
        self.x1, self.y1 = 145, 1900
        enemyImage = self.mode.loadImage('TP_ships.png')
        enemyStrip = self.mode.scaleImage(enemyImage, 2/3)
        self.enemyShip = enemyStrip.crop((self.x0, self.y0, self.x1, self.y1))
        self.enemyShip = self.mode.scaleImage(self.enemyShip, 2/3)

class Spawn(Enemy):
    def __init__(self, mode, cx, cy):
        super().__init__(mode, cx, cy)
        self.rotate = 0
        self.mode = mode
        self.cx = cx
        self.cy = cy  
 
class Stars():
    def __init__(self, mode, cx, cy, r):
        self.mode = mode
        self.cx = cx
        self.cy = cy
        self.r = r
    
    def getHashables(self):
        return (self.cx, self.cy) 
 
    def __hash__(self):
        return hash(self.getHashables())
 
    def __eq__(self, other):
        return (isinstance(other, Enemy) and 
                self.cy == other.cy and self.cx == other.cx)
 
    def draw(self, canvas):
        x0, y0 = self.cx - self.r, self.cy - self.r - self.mode.scrollY
        x1, y1 = self.cx + self.r, self.cy + self.r - self.mode.scrollY
        canvas.create_oval(x0, y0, x1, y1, fill = 'white')

class Beam():
    def __init__(self, mode, cx, cy, angle = 0):
        self.mode = mode
        self.angle = angle
        self.cx = cx
        self.cy = cy
        self.color = 'red'
 
    def draw(self, canvas):
        canvas.create_oval(self.cx - 4, self.cy - 4 - self.mode.scrollY, 
                            self.cx + 4, self.cy + 4 - self.mode.scrollY,
                            fill = self.color)
 
class EnemyBeam(Beam):
     def __init__(self, mode, cx, cy, angle = 0):
        super().__init__(mode, cx, cy, angle = 0)
        self.mode = mode
        self.angle = angle
        self.cx = cx
        self.cy = cy
        self.color = 'green'

class GameMode(Mode):
    def appStarted(mode):
        mode.scrollY = 0
        mode.scrollMargin = 20
        mode.margin = 30
        mode.score = 0
        mode.pressedKeys = []
        mode.visibleMargin = 480
        mode.player = Player(mode, mode.width/2, 
                            mode.height - mode.scrollMargin)
        mode.currEnemies = dict()
        mode.enemies = dict()
        mode.num = 1
        mode.dict = dict()
 
    #Cited from:
    #https://pypi.org/project/Random-Word/
        randomWords = RandomWords()
        mode.wordBank = randomWords.get_random_words(hasDictionaryDef="true")
        
        mode.vocabs = {"index": ['night', 'thought', 'huh', 'guess', 'jeff'],
                "middle": ['buu', 'kid', 'imagine', 'eat', 'caesar'],
                "ring": ['loss', 'walk', 'sweet', 'oyster', 'xerus'],
                "pinky": ['zack', 'pizzazz', 'apple', 'queue', '0101']}
        
        mode.keyMap = {
        '1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (0, 3), '5': (0, 4), 
        '6': (0, 5), '7': (0, 6), '8': (0, 7), '9': (0, 8), '0': (0, 9), 
        'q': (1, 0), 'w': (1, 1), 'e': (1, 2), 'r': (1, 3), 't': (1, 4), 
        'y': (1, 5), 'u': (1, 6), 'i': (1, 7), 'o': (1, 8), 'p': (1, 9), 
        'a': (2, 0), 's': (2, 1), 'd': (2, 2), 'f': (2, 3), 'g': (2, 4), 
        'h': (2, 5), 'j': (2, 6), 'k': (2, 7), 'l': (2, 8), ';': (2, 9),
        'z': (3, 0), 'x': (3, 1), 'c': (3, 2), 'v': (3, 3), 'b': (3, 4), 
        'n': (3, 5), 'm': (3, 6), ',': (3, 7), '.': (3, 8), '?': (3, 9),
        ' ': (3, 2), '-': (0, 9)}
        
        mode.initLeft = {0: (2, 0), 1: (2, 1), 2: (2, 2), 3: (2, 3), 4: (2, 4)}
        mode.initRight = {5: (2, 5), 6: (2, 6), 7: (2, 7), 8: (2, 8), 9: (2, 9)}
 
        mode.currEnemy = None
        mode.currBeam = None
        mode.wave = -1
        mode.weakPoints = dict()
        mode.practice = []
        mode.weakest = None
        mode.hand = None
        mode.finger = None
        mode.seen = []
        mode.currWord = None
        mode.angle = 0
        mode.timer = 0
        bgImage = ("Game BG.jpg")
        mode.bgImage = mode.loadImage(bgImage)
        mode.beam = set()
        mode.enemyBeam = set()
        mode.regenerateEnemies()
 
        mode.stars = set()
        for star in range(30):
            mode.stars.add(Stars(mode, 
            random.randint(mode.margin, mode.width - mode.margin), 
            random.randint(mode.margin, mode.height), 
            random.randint(1, 6)))
 
    def weakestPoint(mode, weakPoints):
        weakest = None
        if len(weakPoints) > 0:
            for elem in weakPoints:
                curr = elem
                if (weakest == None or 
                weakPoints[curr] >= weakPoints[weakest]):
                    weakest = curr
            return weakest
        return None
    
    def regenerateEnemies(mode):
        mode.wave += 1
        mode.temp = []
        mode.weakest = mode.weakestPoint(mode.weakPoints)
 
        if mode.wave >= 1:
            mode.num += 1
            if mode.num > 5:
                mode.num -= 1
            
        for finger in mode.vocabs:
            mode.dict[finger] = mode.vocabs[finger]
 
        if mode.weakest != None:
            if mode.weakest in mode.initLeft: 
                mode.hand = 'left hand'
                if mode.weakest == 0:
                    mode.finger = "pinky"
                elif mode.weakest == 1:
                    mode.finger = "ring"
                elif mode.weakest == 2:
                    mode.finger = "middle"
                else:
                    mode.finger = "index"
            elif mode.weakest in mode.initRight:
                mode.hand = 'right hand'
                if mode.weakest == 7:
                    mode.finger = "middle"
                elif mode.weakest == 8:
                    mode.finger = "ring"
                elif mode.weakest == 9:
                    mode.finger = "pinky"
                else:
                    mode.finger = "index"
 
        for key in mode.keyMap:
            if mode.keyMap[key][1] == mode.weakest:
                mode.temp.append(key)
 
        if mode.wave > len(mode.vocabs) and mode.finger != None:
            for word in mode.wordBank:
                tempCount = 0
                for letter in word:
                    if (letter in mode.temp):
                        tempCount += 1
                        if (tempCount >= 3 and 
                        word not in mode.vocabs[mode.finger]):
                            if len(word) <= mode.wave + 5:
                                mode.vocabs[mode.finger].append(word)

        while len(mode.enemies) < mode.num:
            mode.createEnemy()

        temp = []
        posWords = []
        for word in mode.wordBank:
            if (len(word) <= mode.wave + 5 and
                word not in temp and word not in mode.seen):
                    posWords.append(word)

        for enemy in mode.enemies:
            #make sure no words repeat per generation 
            if (mode.enemies.get(enemy) not in temp and 
                mode.enemies.get(enemy) not in mode.seen):
                enemy.word = mode.enemies.get(enemy)
            else:
                word = random.choice(posWords)
                mode.enemies[enemy] = word
                enemy.word = word
            temp.append(enemy.word)
            mode.seen.append(enemy.word)
            
    def createEnemy(mode):
        fingers = dict()
        possibilities = ["index", "middle", "ring", "pinky"]

        fingers["index"] = Index(mode,
            random.randint(2 * mode.margin, 
            mode.width - mode.margin),
            mode.margin + mode.scrollY)
        fingers["middle"] = Middle(mode,
            random.randint(2 * mode.margin, 
            mode.width - mode.margin),
            mode.margin + mode.scrollY)
        fingers["ring"] = Ring(mode,
            random.randint(2 * mode.margin, 
            mode.width - mode.margin),
            mode.margin + mode.scrollY)
        fingers["pinky"] = Pinky(mode,
            random.randint(2 * mode.margin, 
            mode.width - mode.margin),
            mode.margin + mode.scrollY)
 
        if mode.finger == None:
            finger = random.choice(possibilities)
        else:
            finger = mode.finger
 
        if mode.wave == 0:
            mode.enemies[fingers["index"]] = (mode.dict["index"]
            [random.randint(0, len(mode.dict["index"]) - 1)])
        elif mode.wave == 1:
            mode.enemies[fingers["middle"]] = (mode.dict["middle"]
            [random.randint(0, len(mode.dict["middle"]) - 1)])
        elif mode.wave == 2:
            mode.enemies[fingers["ring"]] = (mode.dict["ring"]
            [random.randint(0, len(mode.dict["ring"]) - 1)])
        elif mode.wave == 3:
            mode.enemies[fingers["pinky"]] = (mode.dict["pinky"]
            [random.randint(0, len(mode.dict["pinky"]) - 1)])
        else:
            mode.enemies[fingers[finger]] = (mode.dict[finger]
            [random.randint(0, len(mode.dict[finger]) - 1)])
    
    #referenced from:
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    #with modifications
    def makePlayerVisible(mode):
        #scroll to make player visible as needed
        if (mode.player.cy - mode.visibleMargin <
            mode.scrollY):
            mode.scrollY = mode.player.cy - mode.visibleMargin
        elif mode.player.cx - mode.scrollMargin <= 0:
            mode.player.cx = mode.scrollMargin
        elif mode.player.cx + mode.scrollMargin >= mode.width:
            mode.player.cx = mode.width - mode.scrollMargin
 
    def timerFired(mode):
        mode.timer += 1
        mode.player.cy -= 2
        mode.makePlayerVisible()
        for enemy in mode.enemies:
            speed = ((len(enemy.word) + 
                    abs(ord(enemy.word[0]) - ord(enemy.word[-1])) % 6) 
                    / len(mode.enemies))
            if mode.app.multi:
                x, y = enemy.cx, enemy.cy
                px, py = mode.player.cx, mode.player.cy
                opp = abs(px - x)
                adj = abs(py - y)
                dy = adj / ((opp + 1) / 5)
                if dy > 4:
                    dy = 4
                hyp = distance(x, y, px, py)

                if x < px - 10:
                    
                    enemy.cy += dy / 2 + speed / 5
                    enemy.cx += 5
                    deltaY = 4 * speed
                elif x >= px - 10 and x <= px + 10:
                    if mode.timer % 10 == 0:
                        mode.enemyBeam.add(EnemyBeam(mode, enemy.cx, 
                                                    enemy.cy))
                    enemy.cy += dy / 2 + speed / 5
                    enemy.cx += 0
                    deltaY = 4 * speed
                elif x > px + 10:
                    
                    enemy.cy += dy / 2 + speed / 5
                    enemy.cx -= 5
                    deltaY = 4 * speed
                    
                for beam in mode.enemyBeam:
                    beam.cy += deltaY
                    beamBound = (beam.cx - 4, beam.cy - 4, 
                                 beam.cx + 4, beam.cy + 4)
                    if mode.boundsIntersect(beamBound, mode.player.getBounds()):
                        mode.app.list.append(leaderBoard(mode.score))
                        mode.app.setActiveMode(mode.app.endGame)      
            #enemy goes faster the more player kills
            #this is an alternative to overlapping words
            else:
                enemy.cy += speed
            #if enemy not killed by the time it crosses the player
            #player lose
            if enemy.cy >= mode.height + mode.scrollY:
                mode.app.list.append(leaderBoard(mode.score))
                mode.app.setActiveMode(mode.app.endGame)
            
            elif (mode.app.multi and 
                mode.boundsIntersect(mode.player.getBounds(), 
                                     enemy.getBounds())):
                mode.app.list.append(leaderBoard(mode.score))
                mode.app.setActiveMode(mode.app.endGame)

        if mode.currEnemy != None:
            x, y = mode.currEnemy.cx, mode.currEnemy.cy
            px, py = mode.player.cx, mode.player.cy
            hyp = distance(x, y, px, py)
            opp = abs(px - x)
            dx = 20
            adj = abs(py - y)
            #slope, rise over run
            dy = adj / ((opp + 1) / dx) 
            if dy >= 250:
                dy = 250
            tempBeam = copy.copy(mode.beam)
            if mode.currEnemy.cx <= mode.player.cx:
                for beam in mode.beam:
                    beam.cy -= dy 
                    beam.cx -= dx
                    beamBound = (beam.cx - 4, beam.cy - 4, 
                                 beam.cx + 4, beam.cy + 4)
                    if beam.cy <= mode.currEnemy.cy:
                        tempBeam.remove(beam)
            else:
                for beam in mode.beam:
                    beam.cy -= dy 
                    beam.cx += dx 
                    beamBound = (beam.cx - 4, beam.cy - 4, 
                                 beam.cx + 4, beam.cy + 4)
                    if beam.cy <= mode.currEnemy.cy:
                        tempBeam.remove(beam) 
            mode.beam = tempBeam
            
                        
    def rotate(mode):
        if mode.currEnemy != None:
            x, y = mode.currEnemy.cx, mode.currEnemy.cy
            px, py = mode.player.cx, mode.player.cy
            hyp = distance(x, y, px, py)
            opp = abs(px - x)
            if x <= px:
                mode.angle = math.asin(opp / hyp) * (180 / math.pi)
            elif x > px:
                mode.angle = - math.asin(opp / hyp) * (180 / math.pi)
            mode.player = Player(mode, px, py, mode.angle)
    
    #uses bounds of each object class to test for collisions in order to 
    #minues health from player and enemies as well as remove coins
    #copied from: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html 
    def boundsIntersect(mode, boundsA, boundsB):
        (ax0, ay0, ax1, ay1) = boundsA
        (bx0, by0, bx1, by1) = boundsB
        return ((ax1 >= bx0) and (bx1 >= ax0) and
                (ay1 >= by0) and (by1 >= ay0))
        

#a few bugs-ish features
    #if word contains capital P or H, will perform action rather
    #than deleting enemy
    def keyPressed(mode, event):
        mode.count = 0
        temp = []
        #start = []
        shortestDistance = []
        if event.key == 'Escape':
            mode.app.count += 1
            mode.app.setActiveMode(mode.app.pauseScreen)
        elif event.key == 'Tab':
            mode.app.list.append(leaderBoard(mode.score))
            mode.app.setActiveMode(mode.app.endGame)
 
        mode.currEnemies = dict()
        mode.pressedKeys.append(event.key.lower())
        #print(mode.pressedKeys)

        if mode.app.multi:
            if event.key == 'Right':
                mode.player.cx += 5
                mode.makePlayerVisible()
            elif event.key == 'Left':
                mode.player.cx -= 5
                mode.makePlayerVisible()

        #gets which enemy is currently being typed on
        for enemy in mode.enemies:
            #start.append(enemy.word[0])
            #shortestDistance.append(mode.player.cy - enemy.cy)
            mode.currEnemies[enemy] = enemy.word
            if (event.key == enemy.word[0] and len(mode.pressedKeys) == 1):
                #else:
                    #if mode.player.cy - enemy.cy <= min(shortestDistance):
                mode.currEnemy = enemy 
                mode.currWord = enemy.word
        mode.rotate()
 
        #if no enemy starts with the letter typed, don't crash
        if mode.currEnemy != None:
            #if wrong letter typed, don't add to the current keys pressed list
            if event.key != mode.currEnemy.word[len(mode.pressedKeys) - 1]:
                mode.pressedKeys.pop()
                if event.key != 'Escape' and event.key != 'Tab':
                #write a generic curr vs best function that keeps track of 
                #which col (aka finger) is popped the most
                #then set the difficulty to that col
                    if event.key in mode.keyMap:
                        mode.weakPoints[mode.keyMap[event.key][1]] = (
                        mode.weakPoints.get(mode.keyMap[event.key][1], 0) + 1)
                        mode.score -= 2
            elif event.key == mode.currEnemy.word[len(mode.pressedKeys) - 1]:
                mode.beam.add(Beam(mode, mode.player.cx, mode.player.cy))
 
            #if right word is typed, reset the keys pressed list 
            #and delete the enemy that has been killed
            if len(mode.pressedKeys) == len(mode.currEnemy.word):
                if ''.join(mode.pressedKeys) == mode.currEnemy.word.lower():
                    for letter in mode.currEnemy.word:
                        if mode.keyMap[letter.lower()][1] == mode.weakest:
                            mode.score += 1
                            mode.count += 1
                            if mode.count > 3:
                                mode.weakest = None
 
                    for i in range(1, len(mode.pressedKeys)):
                        row, col = mode.keyMap[mode.pressedKeys[i]]
                        #if the same letter, add 1 point
                        if (mode.keyMap[mode.pressedKeys[i]] == 
                            mode.keyMap[mode.pressedKeys[i - 1]]):
                            mode.score += 1
                        
                        #account for when the first keys are init pos
                        elif (mode.keyMap[mode.pressedKeys[i]] == 
                        mode.initLeft.get(col) or 
                        mode.keyMap[mode.pressedKeys[i]] == 
                        mode.initRight.get(col)):
                            mode.score += 1
 
                        #if the same col (finger moving up and down)
                        elif col == mode.keyMap[mode.pressedKeys[i - 1]][1]:
                            #if left hand
                            if col < 5:
                                mode.score += (
                            abs(4 - mode.keyMap[mode.pressedKeys[i - 1]][1]) + 
                            abs(mode.keyMap[mode.pressedKeys[i - 1]][0] - row))
                            #if right hand
                            else:
                                mode.score += (
                            abs(5 - mode.keyMap[mode.pressedKeys[i - 1]][1]) + 
                            abs(mode.keyMap[mode.pressedKeys[i - 1]][0] - row))
                        
                        #if the same row (moving left and right)
                        elif row == mode.keyMap[mode.pressedKeys[i - 1]][0]:
                            #if prev and curr both left hand:
                            if (col < 5 and 
                                mode.keyMap[mode.pressedKeys[i - 1]][1] < 5):
                                mode.score += (
                                abs(row - mode.initLeft[col][0]) + 
                                abs(
                                abs(4 - mode.keyMap[mode.pressedKeys[i]][1])
                                - mode.keyMap[mode.pressedKeys[i - 1]][1]))
                            #if both right hand
                            elif (col >= 5 and 
                                mode.keyMap[mode.pressedKeys[i - 1]][1] >= 5):
                                mode.score += (
                                abs(row - mode.initRight[col][0]) + 
                                abs(
                                abs(5 - mode.keyMap[mode.pressedKeys[i]][1]) 
                                - mode.keyMap[mode.pressedKeys[i - 1]][1]))
                            
                            #if both diff hands
                            else:
                                prevCol = (
                                mode.keyMap[mode.pressedKeys[i - 1]][1])
                                prevRow = (
                                mode.keyMap[mode.pressedKeys[i - 1]][0])
                                if col < 5:
                                    mode.score += (
                                    abs(row - mode.initLeft[col][0]) + 
                                    abs(prevRow
                                    - mode.initRight[prevCol][0]))
                                else:
                                    mode.score += (
                                    abs(row - mode.initRight[col][0]) + 
                                    abs(prevRow
                                    - mode.initLeft[prevCol][0]))
                                    
                        #diff row and col
                        else:
                            #calculate score for right and left hand separately
                            #by getting the distance from curr key to finger's
                            #init pos
                            if col < 5:
                                mode.score += int(distance(
                                mode.keyMap[mode.pressedKeys[i]][1], 
                                mode.keyMap[mode.pressedKeys[i]][0],
                                4, mode.initLeft[col][0]
                                ))
                            else:
                                mode.score += int(distance(
                                mode.keyMap[mode.pressedKeys[i]][1], 
                                mode.keyMap[mode.pressedKeys[i]][0],
                                5, mode.initRight[col][0]
                                ))
 
                    mode.pressedKeys = []
                    if mode.currWord != None:
                        if mode.wave > 1 and len(mode.currWord) > 6:
                            cx = mode.currEnemy.cx
                            cy = mode.currEnemy.cy
                            word = mode.currWord[len(mode.currWord) - 1].lower()
                            key = mode.keyMap[word][1]
                            tempList = []
                            for printable in mode.keyMap:
                                if mode.keyMap[printable][1] == key:
                                    if printable != ' ':
                                        tempList.append(printable)
                            #if mode.currBeam.cy == mode.currEnemy.cy:
                            
                            del mode.currEnemies[mode.currEnemy]
                            spawn = Spawn(mode, cx, cy)
                            letter = random.choice(tempList)
                            mode.currEnemies[spawn] = spawn
                            spawn.word = str(letter)
                            if (event.key == spawn.word and 
                                len(mode.pressedKeys) == 1):
                                
                                del mode.currEnemies[spawn]  
                                mode.currWord = None 
                        else:
                            
                            del mode.currEnemies[mode.currEnemy]
                            mode.currWord = None
                else: 
                    mode.pressedKeys = []
        else:
           mode.pressedKeys = []
 
        mode.enemies = mode.currEnemies
        if len(mode.enemies) <= 0:
            mode.regenerateEnemies()
 
 
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width//2, mode.height//2, 
                            image = ImageTk.PhotoImage(mode.bgImage))
        
        for star in mode.stars:
            star.draw(canvas)
            if star.cy >= mode.scrollY + mode.height:
                mode.stars.remove(star)
                mode.stars.add(Stars(mode, 
                random.randint(mode.margin, mode.width - mode.margin), 
                mode.scrollY, 5))
        
        for beam in mode.beam:
            beam.draw(canvas)
        
        for beam in mode.enemyBeam:
            beam.draw(canvas)

        mode.player.draw(canvas) 
 
        for enemy in mode.enemies:
            enemy.draw(canvas)
 
        canvas.create_text(mode.width - 45, 
                            mode.scrollMargin, 
                            text = f'score: {mode.score}', 
                            fill = 'white',
                            font = 'Times 10')
 
        canvas.create_text(mode.width - 70, 
                            mode.scrollMargin + 20, 
                            text = f'current word: {mode.currWord}', 
                            fill = 'white',
                            font = 'Times 10')
 
        canvas.create_text(mode.width - 80, 
        mode.scrollMargin + 40,
        text = f'weakness: {mode.hand} {mode.finger}', 
        fill = 'white', 
        font = 'Times 10')

        canvas.create_text(mode.width / 2, mode.height - 50,
                            text = mode.pressedKeys,
                            fill = 'white', 
                            font = 'Times 20')

class EndGame(Mode):
    def appStarted(mode):
        mode.boxLeft = mode.width / 2 - 40
        mode.boxTop = mode.height - 65
        mode.boxRight = mode.boxLeft + 80
        mode.boxBottom = mode.boxTop + 25
        mode.startColor = 'white'

        bgImage = ("End BG.jpg")
        mode.bgImage = mode.loadImage(bgImage)

        mode.list = []
        
    def inRange(mode, x0, y0, x1, y1, x2, y2):
        return (x0 <= x1 <= x2 and y0 <= y1 <= y2)
        
    def mouseMoved(mode, event):
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.startColor = 'gold'
        else:
            mode.startColor = 'white'
        
    def mousePressed(mode, event):
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.app.started = True
            mode.app.gameMode.appStarted()
            mode.app.setActiveMode(mode.app.splashScreen)

    def redrawAll(mode, canvas):
        for i in mode.app.list[len(mode.app.list) - 1].split('\n'):
            if len(i) != 0 and (int(i) not in mode.list):
                mode.list.append(int(i))
        
        mode.list = sorted(mode.list)[::-1]
        mode.list = mode.list[:8]
        text = ''
        for i in range(len(mode.list)):
            text += f'{mode.list[i]}\n'

        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill = 'black')
        canvas.create_image(mode.width//2, mode.height//2, 
                            image = ImageTk.PhotoImage(mode.bgImage))
        canvas.create_text(mode.width / 2, mode.height - 50, 
                    text = "RETRY", font = 'Times 25', fill = mode.startColor)
        canvas.create_text(mode.width / 2, 75,
                            text = 'You Lost!', font = 'Times 50', 
                            fill = 'white')
        canvas.create_text(mode.width / 2, mode.height * 3 / 5,
                        text = text,
                        font = 'Times 20',
                        fill = 'black')
    
class PauseScreen(Mode):
    def appStarted(mode):
        mode.boxLeft = mode.width / 2 - 50
        mode.boxTop = mode.height / 2 - 15
        mode.boxRight = mode.boxLeft + 100
        mode.boxBottom = mode.boxTop + 30
        mode.startColor = 'white'

        mode.helpLeft = mode.width / 2 - 30
        mode.helpRight = mode.boxLeft + 60
        mode.helpTop = 2 * mode.height / 3 - 15
        mode.helpBottom = mode.helpTop + 30
        mode.helpColor = 'white'
    
    def inRange(mode, x0, y0, x1, y1, x2, y2):
        return (x0 <= x1 <= x2 and y0 <= y1 <= y2)
        
    def mouseMoved(mode, event):
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.startColor = 'gold'
        elif mode.inRange(mode.helpLeft, mode.helpTop, 
                        event.x, event.y, mode.helpRight, mode.helpBottom):
            mode.helpColor = 'gold'
        else:
            mode.startColor = 'white'
            mode.helpColor = 'white'
        
    def mousePressed(mode, event):
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.app.setActiveMode(mode.app.gameMode)
        elif mode.inRange(mode.boxLeft, mode.helpTop, 
                          event.x, event.y, mode.boxRight, mode.helpBottom):
            mode.app.setActiveMode(mode.app.helpMode)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill = 'black')
        canvas.create_text(mode.width / 2, mode.height / 2, 
                    text = "RESUME", font = 'Times 25', fill = mode.startColor)
        canvas.create_text(mode.width / 2, 2 * mode.height / 3, text = 'HELP',
                           font = 'Times 25', fill = mode.helpColor)
        canvas.create_text(mode.width / 2, 75,
                            text = f'PAUSED', font = 'Times 50', 
                            fill = 'white')
        
class SplashScreen(Mode):
    def appStarted(mode):
        mode.boxLeft = mode.width / 2 - 40 - 70
        mode.boxTop = mode.height / 2 - 20 + 15
        mode.boxRight = mode.boxLeft + 80
        mode.boxBottom = mode.boxTop + 30 + 10
        mode.startColor = 'white'

        mode.helpTop = 2 * mode.height / 3 - 20
        mode.helpLeft = mode.width / 2 - 40
        mode.helpRight = mode.helpLeft + 80
        mode.helpBottom = mode.helpTop + 30
        mode.helpColor = 'white'

        mode.multiTop = mode.height / 2 - 20 + 15
        mode.multiBottom = mode.boxTop + 30 + 10
        mode.multiLeft = mode.width / 2 - 40 + 70
        mode.multiRight = mode.multiLeft + 80
        mode.multiColor = 'white'
    
        bgImage = ("Splash BG.png")
        mode.bgImage = mode.loadImage(bgImage)
        

    def inRange(mode, x0, y0, x1, y1, x2, y2):
        return (x0 <= x1 <= x2 and y0 <= y1 <= y2)
        
    def mouseMoved(mode, event):
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.startColor = 'gold'
        elif mode.inRange(mode.helpLeft, mode.helpTop, 
                        event.x, event.y, mode.helpRight, mode.helpBottom):
            mode.helpColor = 'gold'
        elif mode.inRange(mode.multiLeft, mode.multiTop, 
                        event.x, event.y, mode.multiRight, mode.multiBottom):
            mode.multiColor = 'gold'
        else:
            mode.startColor = 'white'
            mode.helpColor = 'white'
            mode.multiColor = 'white'

    def mousePressed(mode, event):
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.app.multi = False
            mode.app.started = True
            mode.app.setActiveMode(mode.app.gameMode)
        elif mode.inRange(mode.helpLeft, mode.helpTop, 
                        event.x, event.y, mode.helpRight, mode.helpBottom):
            mode.app.started = False
            mode.app.setActiveMode(mode.app.helpMode)
        elif mode.inRange(mode.multiLeft, mode.multiTop, 
                        event.x, event.y, mode.multiRight, mode.multiBottom):
            mode.app.multi = True
            mode.app.started = True
            mode.app.setActiveMode(mode.app.gameMode)

    def redrawAll(mode, canvas):
        text = "Welcome To The Typing Game!"
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'black')
        canvas.create_image(mode.width//2, mode.height//2, 
                            image = ImageTk.PhotoImage(mode.bgImage))
        canvas.create_text(mode.width / 2, 75, text = text, font = 'Times 33', 
                           fill = "white")
        canvas.create_text(mode.width / 2 - 70, mode.height / 2 + 20, 
                            text = "SINGLE", 
                            font = 'Times 25', fill = mode.startColor)
        canvas.create_text(mode.width / 2, 2 * mode.height / 3, text = 'HELP',
                           font = 'Times 25', fill = mode.helpColor)
        canvas.create_text(mode.width / 2 + 70, mode.height / 2 + 20, 
                            text = 'MULTI',
                            font = 'Times 25', fill = mode.multiColor)
        
class HelpMode(Mode):
    def appStarted(mode):
        mode.boxLeft = mode.width / 2 - 100
        mode.boxTop = 3 * mode.height / 4 - 15
        mode.boxRight = mode.boxLeft + 200
        mode.boxBottom = mode.boxTop + 25
        mode.color = 'white'

        mode.resumeLeft = mode.width / 2 - 50
        mode.resumeRight = mode.resumeLeft + 100
        mode.resumeTop = 3 * mode.height / 4 + 40
        mode.resumeBottom = mode.resumeTop + 25
        mode.resumeColor = 'white'

    def inRange(mode, x0, y0, x1, y1, x2, y2):
        return (x0 <= x1 <= x2 and y0 <= y1 <= y2)
        
    def mouseMoved(mode, event):
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.color = 'gold'
        elif mode.inRange(mode.resumeLeft, mode.resumeTop, 
                        event.x, event.y, mode.resumeRight, mode.resumeBottom):
            mode.resumeColor = 'gold'
        else:
            mode.resumeColor = 'white'
            mode.color = 'white'
        
    def mousePressed(mode, event):
        #Back to title
        if mode.inRange(mode.boxLeft, mode.boxTop, 
                        event.x, event.y, mode.boxRight, mode.boxBottom):
            mode.app.started = False
            if mode.app.count == 0:
                mode.app.setActiveMode(mode.app.splashScreen)
            else:
                mode.app.gameMode.appStarted()
                mode.app.setActiveMode(mode.app.splashScreen)
        #Resume
        elif (mode.app.started and mode.inRange(mode.boxLeft, mode.resumeTop, 
                        event.x, event.y, mode.boxRight, mode.resumeBottom)):
            mode.app.setActiveMode(mode.app.gameMode)

    def redrawAll(mode, canvas):
        text = """
                Can You Beat The Highscore? \n 
                Work On Your Weakpoints And Get Better At Typing! \n
                Type The Word On Each Enemy To Eliminate Them! \n
                Watch Out For Those Speed Boost And Surprise Spawns!\n
                
                In MULTI Mode, You Must Collaborate With Your Friend \n
                To Dodge Those Bullets Using Left And Right Arrow Keys \n
                And Type Away Those Enemies!"""

        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill = 'black')
        canvas.create_text(mode.width / 2, 3 * mode.height / 4, 
                           text = "BACK TO TITLE", 
                           font = 'Times 25', fill = mode.color)
        if mode.app.started:
            canvas.create_text(mode.width / 2, 3 * mode.height / 4 + 50, 
                            text = "RESUME", 
                            font = 'Times 25', fill = mode.resumeColor)
        canvas.create_text(mode.width / 2, 2 * mode.height / 5,
                           text = text, fill = 'white')
 
def runTypingGame():
    class TypingGame(ModalApp):
        def appStarted(app):
            app.list = []
            app.count = 0
            app.gameMode = GameMode()
            app.endGame = EndGame()
            app.pauseScreen = PauseScreen()
            app.splashScreen = SplashScreen()
            app.helpMode = HelpMode()
            app.started = False
            app.multi = False
            app.setActiveMode(app.splashScreen)
    app = TypingGame(width = 500, height = 500)
 
#################################################
# testAll and main
#################################################
def testAll():
    runTypingGame()
 
def main():
    cs112_f19_week11_linter.lint()
    testAll()
 
if __name__ == '__main__':
    main()
 

