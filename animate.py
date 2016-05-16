# -*- coding: utf-8 -*-
"""
THIS PART IS LESS GOOD THAN THE OTHER PART

@author: Sam
"""

import Image
import numpy as np
import matplotlib.pyplot as plt
import time
from main import getBlackPixels, rotatePts, writeOutputGear

def outputGearImage(image, coords, scale, ratio):
    '''Draws coordinates as pixels on image'''
    newImage = image
    for (x,y) in coords:
        row = np.floor((y+ratio)*ratio/(2.*scale))
        col = np.floor((x+ratio)*ratio/(2.*scale))
        newImage[row][col] = 255.0
    return newImage

def colorfulArray(inGear, outGear, inScale, ratio):
    image = 255*np.ones([1500,1500,3], 'uint8')
    for (x,y) in inGear:
        row = int(np.floor((y+ratio)*ratio/(2.*inScale)))
        col = int(np.floor((x+ratio)*ratio/(2.*inScale)))
        image[row][col][0] = 0.0
        image[row][col][1] = 0.0
    for (x,y) in outGear:
#        row = int(np.floor((y+ratio)*ratio/(2.*inScale)))
#        col = int(np.floor((x+ratio)*ratio/(2.*inScale)))
        row = np.floor((y+ratio)*ratio/(2.*inScale/ratio))
        col = np.floor((x+ratio)*ratio/(2.*inScale/ratio))
        image[row][col][2] = 0.0
        image[row][col][1] = 0.0
    return image

def animate(inputGear, outputGear, ratio, overlap):
    '''Take two arrays and overlap, draw the animation, blah'''
    # Is overlap give in pixels or as a scaling factor?
    inRows = len(inputGear)
    inCols = len(inputGear[0])
    outRows = len(outputGear)
    outCols = outRows # Output gear should be square
    size = inRows*(inRows>=inCols) + inCols*(inCols>inRows) # Get largest dimension
    #overlap = round(overlap*size/2.0)
    
    offset = (ratio+1-overlap, 0)
    inCoords, inScale = getBlackPixels(inputGear, offset)
    outCoords, outScale = getBlackPixels(outputGear, (0,0))
    outCoords = [(ratio*x, ratio*y) for (x,y) in outCoords]
    
    frames = 60
    for frame in range(frames):
        theta = 2*np.pi*frame/frames
        phi = -theta*ratio
        inGearRot = rotatePts(inCoords, offset, phi)
        outGearRot = rotatePts(outCoords, (0,0), theta)
        # allCoords = inGearRot + outGearRot
        image = colorfulArray(inGearRot, outGearRot, inScale, ratio)
        #plt.imshow(image)
        #time.sleep(1)
        writeOutputGear(image, str(frame)+'.png')