#PolyDwarf Blog

# Introduction #

In this blog I like to write down short notes, maybe some links if something interesting ocurred to me while implementing PolyDwarf


# Details #

## 20. Jan 2013 ##
Solved the flickering. http://wiki.wxpython.org/DoubleBufferedDrawing proved to be useful. I've implemented flickering free onPaint methods using wx under C++ but could not quite remember the details. First I was a bit irritated by the suggested solutions, but now it seems very reasonable. BTW, it works!

## 05. Feb 2013 ##
Finally I got this stupid direction arrow issue solved. I'm drawing stupid vectors to indicate the direction of a segment by rotating in 2D by myself. First I wanted to rotate an image (I would have had support for that by wxPython), but than I had to learn that wxPython does not support transparency on images. It really sucked without transparency. So I did the rotation stuff using NumPy. That was fun! Learned something new...