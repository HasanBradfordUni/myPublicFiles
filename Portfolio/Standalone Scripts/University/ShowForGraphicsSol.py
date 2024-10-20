# ShowForGraphics.py
""" Module for practicing for-loops in a graphics setting"""

from SimpleGraphics import *

m = 5
MakeWindow(m,bgcolor=WHITE,labels=True)

# Definition: the endpoints of horizontal line segment k
#       are (-m,k) and (m,k).
# This loop draws horizontal line segments -m through m...
for k in range(-m,m+1):
    # Draw line segment k...
    DrawLineSeg(-m,k,m,k,LineColor=RED,LineWidth=5)

# Definition: the endpoints of vertical line segment k
#       are (k,-m) and (k,m).
# This loop draws vertical line segments -m through m...

# Put solution to 5.1 here
for k in range(-m,m+1):
    # Draw line segment k...
    DrawLineSeg(k,-m,k,m,LineColor=RED,LineWidth=3)

# Definition: An edge star has radius .5 and is centered
# in a box that is on the edge of the window.
# This loop draws all possible edge stars.

# Put solution to 5.2 here
for k in range(-m,m):
    # Right edge...
    DrawStar(m-.5,k+.5,.5,FillColor=BLUE)
    # Left edge..
    DrawStar(-m+.5,k+.5,.5,FillColor=BLUE)
    # Top edge...
    DrawStar(k+.5,m-.5,.5,FillColor=BLUE)
    #  Bottom edge...
    DrawStar(k+.5,-m+.5,.5,FillColor=BLUE)

ShowWindow()

