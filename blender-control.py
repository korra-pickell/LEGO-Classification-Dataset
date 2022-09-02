import pyautogui as pog
import os, random, math, cv2, time
import numpy as np

number_of_renders = 5000

pog.PAUSE = 0.5

renders_save_dir = 'E:\\DATA\\Blocks-2\\DataGen\\Renders'

def get_current_render_number():
    existing_renders = os.listdir(renders_save_dir)
    if (existing_renders != []):
        existing_renders = [int(name.split('.')[0]) for name in existing_renders]
        existing_renders.sort()
        return existing_renders[-1] + 1
    else:
        return 0

time.sleep(3) # Wait for Blender Switch

for render in range(0,number_of_renders):

    t0 = time.time()

    pog.moveTo(745,64) # Run Sim Script
    pog.click(745,64)

    time.sleep(12)

    pog.moveTo(745,390) # Save metadata
    pog.click(745,390)

    time.sleep(0.5)

    pog.hotkey('f12') # Render Image

    time.sleep(60) # Wait for Render

    pog.hotkey('alt','s')

    pog.moveTo(525,70)
    pog.click(525,70)

    pog.typewrite(renders_save_dir)

    pog.moveTo(525,95)
    pog.click(525,95)
    pog.click(525,95)

    filename = str(get_current_render_number())+'.png'

    pog.typewrite(filename,interval=0.2)

    pog.moveTo(1850,70)
    pog.click(1850,70)
    pog.click(1850,70)

    pog.moveTo(1888,15)
    pog.click(1888,15)

    time.sleep(1)

    print("--- %s seconds ---" % (time.time() - t0))

