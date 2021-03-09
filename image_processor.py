import os
import cv2
import numpy as np
from PIL import Image

def openImg(imgPath):
    return Image.open(imgPath)

def emptyFolder(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    print("[emptyFolder] "+ dir + " cleaned")

def splitImg(filename, chopsize):
    print("[splitImg] initializing")
    chopsize = chopsize
    img = openImg(filename)
    width, height = img.size
    # Save Chops of original image
    for x0 in range(0, width, chopsize):
        for y0 in range(0, height, chopsize):
            box = (x0, y0,
                   x0 + chopsize if x0+chopsize < width else width - 1,
                   y0 + chopsize if y0+chopsize < height else height - 1)
            img.crop(box).save('%s.x%03d.y%03d.jpg' % (f"cropped_img/tile", x0, y0))
    print("[splitImg] completed")


def getAvrColor(chopsize):
    print("[getAvrColor] initializing")
    # loop through the files in a folder
    for filename in os.listdir("cropped_img"):
        if filename.endswith(".jpg"):
            croppedImg = Image.open(f"cropped_img\{filename}")
            width, height = croppedImg.size
            r_total = 0
            g_total = 0
            b_total = 0
            count = 0
            # get rgb for everly picture
            for x in range(0, width):
                for y in range(0, height):
                    r, g, b = croppedImg.getpixel((x, y))
                    r_total += r
                    g_total += g
                    b_total += b
                    count += 1
            #create a solid block with the rgb we got earlier
            solid_block = Image.new('RGB', (chopsize, chopsize), color = (round(r_total/count), round(g_total/count), round(b_total/count)))
            new_filename = filename.replace(".jpg", "")
            solid_block.save('%s.jpg' % (f"solid_blocks/{new_filename}"))
    print("[getAvrColor] completed")


def stackImages(chopsize, filename):
    print("[stackImages] initializing")
    imgArr = []
    origImg = openImg(filename)
    # loop through the files in a folder
    for filename in sorted(os.listdir("cropped_img"), key=len):
        imgArr.append(filename)
    width, height = origImg.size
    rows = round(width / chopsize)
    cols = round(height / chopsize)
    horizontalStack = []
    storeX = 0
    currArr = []
    i = 0
    # fill stack arr
    for x in range( 0, rows):
        for y in range(0, cols):
            if(len(currArr) == cols):
                horizontalStack.append(cv2.hconcat(currArr))
                currArr = []
            img = cv2.imread(f"solid_blocks/{imgArr[i]}")
            currArr.append(img)
            i += 1
            storeX = x

    # empty cropped_img
    emptyFolder("cropped_img")
    # empty solid_blocks
    emptyFolder("solid_blocks")
    # concatenate
    img = cv2.vconcat(horizontalStack)
    #final edits
    img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img, 1)
    cv2.imshow("mosaic.jpg",img)
    cv2.waitKey()
    print("[stackImages] completed")
    
            

def makeMosaic(chopsize, filename):
    # empty cropped_img
    emptyFolder("cropped_img")
    # empty solid_blocks
    emptyFolder("solid_blocks")
    splitImg(filename, chopsize)
    getAvrColor(chopsize)
    stackImages(chopsize, filename)

makeMosaic(10, "res\cat.jpg")