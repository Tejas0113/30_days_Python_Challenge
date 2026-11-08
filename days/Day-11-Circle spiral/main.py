from turtle import setworldcoordinates
from turtle import *

# Set up the screen dimensions (width, height)
setworldcoordinates(450, -450,450,-450)

# Initialize settings
speed(0)  # Maximum drawing speed
bgcolor("white")  # Optional background color

# Draw the spiral pattern
for i in range(50):
    circle(100, 360)
    left(5)

# Keep the window open until clicked
done()