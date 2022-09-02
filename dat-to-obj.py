import pyautogui as pog
import time, random

pog.PAUSE = 0.3
import_wait_time = 1
export_wait_time = 1

blocks_file = open('E:\\Documents\\PRGM\\NEURAL\\Blocks\\parts-popular.txt','r')

blocks = [block.replace('\n','') for block in blocks_file.readlines()]
time.sleep(2)

for block in blocks:
    t0 = time.time()

    pog.moveTo(43,36) # File Menu
    pog.click(43,36)

    pog.moveTo(43,300) # Import
    pog.moveTo(315,525)
    time.sleep(0.2)
    pog.click(315,525) # LDraw Import
    pog.moveTo(850,55) #File Path Text Field
    pog.click(850,55) #File Path Text Field

    pog.typewrite('E:\\DATA\\blocks\\ldraw\\parts\\'+block+'.dat')

    #s = input('...')
    pog.click(1275,1010) #Finish Import
    pog.click(1275,1010) #Finish Import

    time.sleep(import_wait_time)

    #Delete Camera

    pog.moveTo(1690,147)
    pog.click(1690,147)
    pog.hotkey('x')

    #Delete Ground Plane

    pog.click(1690,147)
    pog.hotkey('x')

    #Delete Light

    pog.click(1690,147)
    pog.hotkey('x')

    pog.moveTo(43,36) # File Menu
    pog.click(43,36) 

    pog.moveTo(43,327) # Export

    pog.moveTo(278,525) #.OBJ
    pog.click(278,525)
    

    pog.moveTo(1100,55) #File Path Text Field
    pog.click(1100,55) #File Path Text Field

    pog.typewrite('E:\\DATA\\Blocks-2\\part-objs') # File Path


    pog.moveTo(860,1010) # Name Bar
    pog.click(860,1010)
    pog.click(860,1010)
    pog.typewrite(block+'.obj')
    pog.hotkey('enter')

    pog.moveTo(1240,1010) # Export Button
    pog.click(1240,1010)

    time.sleep(0.4)

    pog.hotkey('ctrl','n') # New Workspace

    #s = input('...')
    pog.moveTo(1145,935) 
    pog.click(1145,935)

    pog.moveTo(1000,570) #Do Not Save Button
    pog.click(1000,570)

    print("--- %s seconds ---" % (time.time() - t0))

