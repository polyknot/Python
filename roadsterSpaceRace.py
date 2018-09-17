import signal, sys, os, random, tty, termios, time

# LISTEN FOR ROADSTER MOVEMENT INPUT
def getUserInput():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
        finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# THROW A TIMEOUTERROR - TO BE USED WITH KEYBOARD LISTENER
def continuePlay(signum, Frame):
        raise TimeoutError

# FUNCTION TO CREATE THE LIST
def buildLineList():
        global lineList, randomList, counter, lineLength, aIndex, aIndex2, aIndex3, aIndex4, space
        lineList = []
        while True:
                if counter == lineLength:
                        break
                elif (counter < aIndex or aIndex2 < counter) and not isSplit:
                        lineList.extend(debris)
                elif (counter < aIndex or aIndex4 < counter) and isSplit:
                        lineList.extend(debris)
                elif aIndex2 < counter < aIndex3: lineList.extend('x')
                elif counter == aIndex or counter == aIndex2 or counter == aIndex3 or counter == aIndex4:
                        lineList.extend(asteroid)
                elif counter == rIndex: lineList.extend(roadster)
                else: lineList.extend(space)
                counter += 1
        counter = 0

# FUNCTION TO CRETE A LINE TO PRINT FROM LIST
def buildLineString():
        global lineList, lineString
        lineString = ''
        for i in lineList:
                lineString += i
        if score % 10 == 0: 
                lineString += '\t SCORE: ' + str(score)
        return lineString

# FUNCTION TO CHECK IF THE ROADSTER HAS HIT AN ASTEROID
def hasCrashed():
        global aIndex, aIndex2, aIndex3, aIndex4, rIndex
        # if path is not split, check two sides
        if not isSplit:
                if rIndex <= aIndex or aIndex2 <= rIndex:
                        return True
                else: return False
        # if path is split, check both path's sides
        else: 
                if rIndex <= aIndex or (aIndex2 <= rIndex <= aIndex3) or aIndex4 <= rIndex:
                        return True
                else: return False

# FUNCTION TO CHECK IF THE ASTEROIDS ARE TOO CLOSE
def asteroidsTooClose():
        global dBetweenA, aIndex, aIndex2
        dBetweenA = aIndex2 - aIndex
        if dBetweenA <= getMinDistance(): return True
        else: return False

# FUNCTION TO CALCULATE THE MIN ALLOWED DISTANCE BASED ON SCORE
def getMinDistance():
        global score, minDistance, lineLength
        if score > 1000: minDistance = 7
        else: minDistance = lineLength*0.3 - int(score/50)
        return minDistance

# FUNCTION TO CHECK IF THE ASTEROIDS ARE TO FAR AWAY
def asteroidsTooFar():
        global dBetweenA, aIndex, aIndex2
        dBetweenA = aIndex2 - aIndex
        if dBetweenA >= getMaxDistance(): return True
        else: return False

# FUNCTION TO CALCULATE THE MAX ALLOWED DISTANCE BASED ON SCORE
def getMaxDistance():
        global score, maxDistance, lineLength
        if score > 1000: maxDistance = 10
        else: maxDistance = lineLength*0.4 - int(score/50)
        return maxDistance

# FUNCTION TO MOVE ROADSTER BASED ON DETECTED INPUT
def moveRoadster(char):
        global rIndex
        if char == 'j':
                rIndex -= 1
        elif char == 'k':
                rIndex += 1

# FUNCTION TO MOVE LEFT ASTEROID
def moveLeftA():
        global aIndex
        # move right if at left end or to far away
        if aIndex <= 1 or asteroidsTooFar(): aIndex += 1
        # move left if randomly selected and not breaking rules
        elif random.randrange(2) == 0 or asteroidsTooClose():
                aIndex -= 1
        # move right otherwise
        else: aIndex += 1

# FUNCTION TO MOVE RIGHT ASTEROID
def moveRightA():
        global aIndex2, lineLength
        # move left if at the end of the line or too far away
        if aIndex2 >= lineLength-1 or asteroidsTooFar(): aIndex2 -= 1
        # move left if randomly selected and not breaking rules
        elif random.randrange(2) == 0 and not asteroidsTooClose():
                aIndex2 -= 1
        # move right otherwise
        else: aIndex2 += 1

# FUNCTION TO MOVE CENTERPOINT
def moveCP():
        global aIndex, aIndex2, score, moveCPVal
        if score % (lineLength) == 0: aIndex2 + moveCPVal
        else: aIndex2 + moveCPVal

# SPLIT PATH
def split():
        global isSplit, aIndex,aIndex2, aIndex3, aIndex4
        gap = aIndex2 - aIndex
        aIndex4 = aIndex2
        aIndex2 = aIndex + gap/2
        aIndex3 = aIndex2+1
        isSplit = True

# MERGE PATH
def merge():
        global isSplit, aIndex2, aIndex3, aIndex4
        aIndex2 = aIndex4
        aIndex3 = -1
        aIndex4 = 1000
        isSplit = False

# CALCULATE MAX DISTANCE FOR A3/4
def a34TooClose():
        global aIndex3, aIndex4
        gap = aIndex4 - aIndex3
        if gap <= getMinDistance(): return True
        else: return False

# CALCULATE MIN DISTANCE FOR A3/4
def a34TooFar():
        global aIndex3, aIndex4
        gap = aIndex4 - aIndex3
        if gap >= getMaxDistance(): return True
        else: return False

# FUNCTION TO FIND OUT IF A2/3 ARE TO CLOSE
def a23TooClose():
        global aIndex2, aIndex3
        gap = aIndex3 - aIndex2
        if gap <= getMinDistance()/2: return True
        else: return False

# FUNCTION TO FIND OUT IF A3/4 ARE TO FAR AWAY
def a23TooFar():
        global aIndex2, aIndex3
        gap = aIndex3 - aIndex2
        if gap >= getMaxDistance()/2: return True
        else: return False

# MOVE LEFT PATH
def moveLPath():
        global aIndex, aIndex2, aIndex3
        if aIndex <= 1 or asteroidsTooFar(): aIndex += 1
        elif random.randrange(2) == 0 or asteroidsTooClose():
                aIndex -= 1
        else: aIndex += 1

        if aIndex2 >= aIndex3 or a34TooFar() or a23TooClose(): aIndex2 -= 1
        elif random.randrange(2) == 0 and not asteroidsTooClose():
                aIndex2 -= 1
        else: aIndex2 += 1

# MOVE RIGHT PATH
def moveRPath():
        global aIndex2, aIndex3, aIndex4
        if aIndex3 <= aIndex2 or a34TooFar() or a23TooClose(): aIndex3 += 1
        elif random.randrange(2) == 0 or a34TooClose():
                aIndex3 -= 1
        else: aIndex3 == 1

        if aIndex4 >= lineLength-1 or a34TooFar(): aIndex4 -= 1
        elif random.randrange(2) == 0 and not a34TooClose():
                aIndex4 -= 1
        else: aIndex4 += 1

# WRITING LINES TO CONSOLE
def launchRoadster():
        global keyInput, speed, score
        wait = 0 
        if speed == 1: wait = 0.2
        elif speed == 2: wait = 0.1
        elif speed == 3: wait = 0.08
        else: wait = 0.01

        # create starting line
        buildLineList()
        os.system('clear')
        print('\n\n\n\n\t\t\t\t******************************************************')
        print('\t\t\t\t\tUse "j" to move left and "k" to move right.')
        print('\t\t\t\t------------------ PREPARE TO LAUNCH! -------------------')
        print('\t\t\t\t*******************************************************')
        print(buildLineString())
        counter = 3
        while counter > 0:
                print('\t\t\tT-' + str(counter) + ' seconds')
                time.sleep(1)
                counter -= 1
        counter = 0

        # loop through lines
        while True:
                # split/merge path every 100 rows
                if score > 100:
                        if not isSplit and random.randrange(80) == 0: split()
                        elif random.randrange(50) == 0 and isSplit: merge()

                # get user input
                try:
                        signal.signal(signal.SIGALRM, continuePlay)
                        signal.setitimer(signal.ITIMER_REAL, wait)
                        keyInput = getUserInput()
                        signal.alarm(0)
                except TimeoutError:
                        roadsterMove = ' '
                        signal.signal(signal.SIGALRM, signal.SIG_IGN)
                        pass

                # move roadster if input is detected
                moveRoadster(keyInput)
                keyInput = ' '

                # move centerpoint and left/right asteroids
                if not isSplit:
                        moveLeftA()
                        moveRightA()
                        moveCP()
                # move two paths if split is true
                else: 
                        moveLPath()
                        moveRPath()

                # detect crash
                if hasCrashed(): 
                        roadster = '*'
                        buildLineList()
                        print(buildLineString())
                        print('\n\n\t\t***************************** YOU HAVE CRASHED **********************************')
                        print('\t\t\t\t\t\t Your Score: ' + str(score))
                        break

                # print line if not crashed
                buildLineList()
                print(buildLineString())
                # increase score by 1 each line
                score += 1
                # time.sleep(wait)

############################### VARS ##########################################
lineLength = 200
aIndex = lineLength*0.4
aIndex2 = lineLength - lineLength*0.4
aIndex3 = -1
aIndex4 = 1000
rIndex = aIndex + (aIndex2-aIndex)/2
counter = 0
score = 0
moveCPVal = 1
minDistance = 0
maxDistance = 0
lineList = []
lineString = ''
randomList = []
debris = '.' 
space = ' '
roadster = chr(165)
asteroid = '0'
keyInput = ''
isSplit = False
while counter < lineLength:
        if random.randrange(2) == 0:
                randomList.extend(debris)
        else: randomList.extend(space)
        counter += 1
counter = 0
###############################################################################

# MAIN RUNNING CODE
os.system('clear')
speed = input('\n\n\t\t* how fast would you like to go? (1=slow, 2=fast, 3=faster, 4=ludacrous): ')
while True:
        try:
                speed = int(speed)
                break
        except:
                pass

launchRoadster()

################### END --------------------------------------------------------
