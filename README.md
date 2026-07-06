# Game-of-Life-Python-exhibit-
A Python program to run Game of Life exhibits/demos


When I was 15 I got interested in John Conway's Game of Life reading an article about it in the October 1970 issue of the *Scientific American* magazine.

This project is Python code designed to run Game of Life exhibits endlessly running on TV monitors. (I used a Raspberry Pi with HDMI to the monitor.)

## There are two exhibits:

- A pre-planned collection of named life forms

- A random initial grid, which changes every time it is run

- Plus a trifold flyer

## Configuring

The code includes hard-wired design decisions:

- Size of grid
- Size of invisible border (e.g., so gliders can run off the visible part of the screen and not fall apart at the edges)
- Font to use
- Detectable cycle length (automatically stop when pattern repeats)
- Maximum iterations (may have long repeat cycles or not repeat at all)
- Sequence of pre-planned and random exhibits
- Mathematica code to generate life cell images

It is perhaps easiest to configure it to have a single run and record to MP4 file on a USB stick, then put the USB in the back of a suitable monitor.
