# -*- coding: utf-8 -*-
"""
Updated Gear Math Python

@author: Sam Ettinger
EttingerSam@gmail.com
May 19, 2016

TODO:
Add a GUI?
"""

''''''''''''''''''''''''''
'''IMPORTANT PARAMETERS'''
''''''''''''''''''''''''''
# Define the gear ratio, which is the number of rotations the input gear com-
# pletes for each one rotation of the output gear. Must be a positive integer.
gearRatio = 2

# Define the gear overlap. This should be a decimal value between 0 and 1.
# This is analogous to tooth size on a spur gear, with 0.0 being "no teeth"
# and 1.0 being "pretty big teeth."
gearOverlap = 1.0

# Define the number of computation steps. This is how many tiny rotations the
# program performs to compute the final bitmap. Higher numbers produce better
# gear profiles, with a tradeoff in speed. Must be an integer.
computationSteps = 1000

''''''''''''''''''''''''''
'''   END PARAMETERS   '''
''''''''''''''''''''''''''

import Image
import numpy as np
import tkFileDialog

def loadGearImage():
    '''Loads image, converts to a B/W array.'''
    filename = tkFileDialog.askopenfilename()
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
    return coords, size

def outputGearImage(image, coords, size, ratio):
    '''Draws coordinates as pixels on image'''
    newImage = image
    for (x,y) in coords:
        row = np.floor((y+ratio)*size/(2*ratio))
        col = np.floor((x+ratio)*size/(2*ratio))
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

def outputCleanup(image):
    '''Remove the 'halo' around output image; maybe apply median filter?'''
    newImage = image
    size = len(image) # Should be same number of rows/columns
    radius = size/2.
    for row in range(size):
        for col in range(size):
            if dist(row-radius, col-radius) >= radius-.5:
                newImage[row][col] = 255.0
    return newImage

def doThings(ratio=gearRatio, overlap=gearOverlap, steps=computationSteps):
    inputGear = loadGearImage()
    offset = (ratio+1-overlap, 0)
    inputCoords, inputImageSize = getBlackPixels(inputGear, offset)
    outputImageSize = inputImageSize*ratio
    outputGear = np.zeros([outputImageSize, outputImageSize])
    theta = 2*np.pi/steps
    phi = 2*np.pi/(steps*ratio)
    # Rotation math
    for step in range(steps):
        coords = rotatePts(inputCoords, offset, theta*step)
        addPoints = []
        for coord in coords:
            if dist(*coord)<(ratio+1-overlap):
                addPoints += [coord]
        # Rotate the points that contribute to the output gear's profile
        for extraRotation in range(ratio):
            rotateBy = phi*step + 2*np.pi*extraRotation/ratio
            addPointsRot = rotatePts(addPoints, (0,0), rotateBy)
            # Convert those points into pixels, draw on output gear
            outputGear = outputGearImage(outputGear, addPointsRot, outputImageSize, ratio)
        print('Progress: {}/{}'.format(step, steps)) # Debug
    # Clean up image
    outputGear = outputCleanup(outputGear)
    # Should also make little marks for centroids and distances
    # Animate?
    # Save image
    outFilename = tkFileDialog.asksaveasfilename(defaultextension='.png')
    writeOutputGear(outputGear, outFilename)
    #return inputGear, outputGear
    
if __name__ == '__main__':
    doThings()