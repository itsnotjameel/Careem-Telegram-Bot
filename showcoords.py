import pylab as plt
import pyautogui
import numpy as np
from matplotlib.text import OffsetFrom
from pilkit.lib import Image
from pilkit.processors import TrimBorderColor
from secret_tokens import screenshotpath
from back_or_forward_slash import back_or_forward_slash
def showcoords(click_x=None, click_y=None):
    '''Shows coordinates, possibly with red dots. click_x and click_y are arrays'''
    global mouseclickfullpath
    mouseclickfullpath = back_or_forward_slash(screenshotpath, 'mouseclickscreenshot.png') #full screenshot path
    global mousechartfullpath
    mousechartfullpath = back_or_forward_slash(screenshotpath, 'mouseclickchart.png') #full edited chart path
    pyautogui.screenshot(mouseclickfullpath) #take screenshot
    screenshotwidth, screenshotheight = Image.open(mouseclickfullpath).size #getting screenshot size
    ax = plt.subplots()[1] #should've been fig, ax = plt.subplots() but trying this
    if click_x != None and click_y != None:
        plt.scatter(x=click_x, y=click_y, c='r', s=30)
    for i in range(0, round(screenshotwidth/100)+1):
        plt.text(i*100, 0, i, color="yellow", fontsize=5, horizontalalignment='center',bbox=dict(fill=True, edgecolor='red', linewidth=1))

    for i in range(0, round(screenshotheight/100)):
        plt.text(0, i*100, i, color="yellow", fontsize=5, verticalalignment='center', bbox=dict(fill=True, edgecolor='red', linewidth=1))
    image = plt.imread(mouseclickfullpath) #matplotlib reading screenshot
    major_ticks = np.arange(0, screenshotwidth, 100) #arranging (idk, length of width, interval)
    plt.tick_params(labelsize=3.5) #font size
    ax.set_xticks(major_ticks) #setting major ticks
    ax.set_yticks(major_ticks)
    ax.grid(which='both') #you need this to make a full grid
    ax.imshow(image, extent=[0, screenshotwidth, 0, screenshotheight])
    plt.imshow(image)
    plt.savefig(mousechartfullpath, dpi=300) #saving figure
    image = Image.open(mousechartfullpath)
    processor = TrimBorderColor() #automatically trimming until there is content
    new_img = processor.process(image)
    new_img.save(mousechartfullpath)

