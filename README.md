# pygear

Let's make gears that look like whatever we want!

## Dependencies

Requires numpy and PIL. Written in Python 2.7

## Operation

For now, run the function `doThings(filename, overlap, ratio, steps)`.
* `filename` is the input gear image source (for now, the output is always `agear.png`)
* `overlap` controls how close the gears' axes are. 1.0 is a good value to start with.
* `ratio` is the gear ratio. For example, a ratio of 2 means the input gear completes two rotations in the time it takes the output gear to complete one rotation. Right now, this has to be an integer value.
* `steps` is the number of steps in the image processing process. 1000 is good.

## TODO:

* Set up animation (there is an aborted attempt in the file `animate.py`)
* Add better documentation