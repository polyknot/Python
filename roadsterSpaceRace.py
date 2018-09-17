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
while True:
        aIndex = lineLength*0.4
        aIndex2 = lineLength - lineLength*0.4
        aIndex3 = -1
        aIndex4 = 1000
        rIndex = aIndex + (aIndex2-aIndex)/2
        counter = 0
        roadster = chr(165)
        isSplit = False
        launchRoadster()
        again = input("Press any key to play again, or press 'q' to quit: ")
        if again == 'q': break
################### END --------------------------------------------------------
