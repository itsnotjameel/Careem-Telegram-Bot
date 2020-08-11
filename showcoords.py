import pylab as plt
import pyautogui
import numpy as np
from matplotlib.text import OffsetFrom
from PIL import Image, ImageChops


def rounddown(x):
    return x / 100


def showcoords(click_x=None, click_y=None):
    '''Shows coordinates, possibly with red dots. click_x and click_y are arrays'''
    global mouseclickfile
    mouseclickfile = 'Careem-Bot-Screenshots/mouseclickscreenshot.png'  # screenshot name
    global mousechartfile
    mousechartfile = 'Careem-Bot-Screenshots/mouseclickchart.png'  # edited chart name
    pyautogui.screenshot(mouseclickfile)  # take screenshot
    screenshotwidth, screenshotheight = Image.open(
        mouseclickfile).size  # getting screenshot size
    # should've been fig, ax = plt.subplots() but trying this
    ax = plt.subplots()[1]
    if click_x is not None and click_y is not None:
        plt.scatter(x=click_x, y=click_y, c='r', s=30)
    separation = 100
    for i in range(
            0, int(
            (((screenshotwidth // separation) * separation) + separation)), separation):
        plt.text(i,
                 0,
                 int(i / 100) if separation == 100 else i / 100,
                 color="yellow",
                 fontsize=5,
                 horizontalalignment='center',
                 bbox=dict(fill=True,
                           edgecolor='red',
                           linewidth=1))

    for i in range(
            0, int(
            (((screenshotheight // separation) * separation) + separation)), separation):
        plt.text(0,
                 i,
                 int(i / 100) if separation == 100 else i / 100,
                 color="yellow",
                 fontsize=5,
                 verticalalignment='center',
                 bbox=dict(fill=True,
                           edgecolor='red',
                           linewidth=1))
    image = plt.imread(mouseclickfile)  # matplotlib reading screenshot
    # arranging (idk, length of width, interval)
    major_ticks = np.arange(0, screenshotwidth, separation)
    plt.tick_params(labelsize=3.5)  # font size
    ax.set_xticks(major_ticks)  # setting major ticks
    ax.set_yticks(major_ticks)
    ax.grid(which='both')  # you need this to make a full grid
    ax.imshow(image, extent=[0, screenshotwidth, 0, screenshotheight])
    plt.imshow(image)
    plt.savefig(mousechartfile, dpi=300)  # saving figure
    image = Image.open(mousechartfile)

    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.convert('RGB').getbbox()
        if bbox:
            return im.crop(bbox)
        elif bbox is None:
            raise AttributeError(
                "bbox value == None, try converting image into RGB if you haven't already done so.")

    im = Image.open(mousechartfile)
    im = trim(im)
    im.save(mousechartfile)
