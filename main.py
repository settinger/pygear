# -*- coding: utf-8 -*-
"""
Updated Gear Math Python

@author: Sam Ettinger
"""

'''
TODO:
* Add support for non-integer gear ratios (e.g. 3:2, 5:3)
'''

import Image
import numpy as np
pi = np.pi # Because I always forget

def loadGearImage(filename):
    '''Loads image, converts to a B/W array.'''
    img = Image.open(filename)
    img.load()
    data = np.asarray(img)
    # Convert to a 2-D array
    newArray = np.array([[np.median(j) for j in i] for i in data])
    return newArray

def getBlackPixels(image, offset):
    '''Get the location of black pixels (zeros in an array).
       Scales result to [-1, 1] and then adds an offset.'''
    rows = len(image)
    cols = len(image[0])
    size = rows*(rows>=cols) + cols*(cols>rows) # Get largest dimension
    scale = 2./size
    coords =  []
    for row in range(rows):
        for col in range(cols):
            if image[row][col] == 0:
                x = scale*(col - (cols-1)/2.) + offset[0]
                y = scale*(row - (rows-1)/2.) + offset[1]
                coords += [(x, y)]
    return coords, scale

def outputGearImage(image, coords, scale, ratio):
    '''Draws coordinates as pixels on image'''
    newImage = image
    for (x,y) in coords:
        row = np.floor((y+ratio)*ratio/(2.*scale))
        col = np.floor((x+ratio)*ratio/(2.*scale))
        newImage[row][col] = 255.0
    return newImage
    

def rotatePts(points, axis, theta):
    '''rotates all coordinates in an array by angle theta, around axis'''
#    centered = [(x-axis[0], y-axis[1]) for (x,y) in points]
#    rotated = [(x*np.cos(theta)-y*np.sin(theta), x*np.sin(theta)+y*np.cos(theta)) for (x,y) in centered]
#    uncentered = [(x+axis[0], y+axis[1]) for (x,y) in rotated]
    uncentered = [(((x - axis[0])*np.cos(theta) - (y - axis[1])*np.sin(theta)) + axis[0], ((x - axis[0])*np.sin(theta) + (y-axis[1])*np.cos(theta)) + axis[1]) for (x,y) in points]
    return uncentered

def writeOutputGear(gear,filename):
    img = Image.fromarray(gear)
    img = img.convert('RGB')
    img.save(filename)
    return None

def dist(x, y):
    return np.sqrt(x*x+y*y)

# Get size of gear from size of image

def doThings(filename, ratio, toothsize, steps):
    inputGear = loadGearImage(filename)
    offset = (ratio+1-toothsize, 0)
    inputCoords, imageScale = getBlackPixels(inputGear, offset)
    inputImageSize = int(np.round(2./imageScale))
    outputImageSize = int(np.ceil(inputImageSize*ratio))
#    outputCoords = []
    outputGear = np.zeros([outputImageSize, outputImageSize])
    theta = 2*np.pi*ratio/steps    # TODO: Change these two lines in order...
    phi = 2*np.pi/steps            # ...to accommodate non-integer gear ratios
    # Rotation math
    for step in range(steps):
        coords = rotatePts(inputCoords, offset, theta*step)
        addPoints = []
        for coord in coords:
            if dist(*coord)<(ratio+1-toothsize):
                addPoints += [coord]
        # Rotate the points that will contribute to the output gear's profile
        addPoints = rotatePts(addPoints, (0,0), phi*step)
        # Convert those points back into pixels for output gear
        outputGear = outputGearImage(outputGear, addPoints, imageScale, ratio)
        # Animate output gear?
        print step
    # Save image
    writeOutputGear(outputGear, 'agear.png')
    # Should also make little marks for centroids and distances