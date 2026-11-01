from turtle import *
import colorsys

# Set up canvas size
setup(800, 800)

# Set (0,0) to be the exact visual center of the window
setworldcoordinates(-450, -450, 450, 450)

bgcolor("black")
hideturtle()

def draw_flower(start_angle):
    """Draws the complete flower starting from the centered (0, 0) origin."""
    penup()
    goto(0, 0)
    setheading(start_angle)
    pendown()
    
    h = 0
    for i in range(16):
        for j in range(18):
            c = colorsys.hsv_to_rgb(h, 1, 1)
            color(c)
            h += 0.005
            rt(90)
            circle(150 - j * 6, 90)
            lt(90)
            circle(150 - j * 6, 90)
            rt(180)
        circle(40, 24)

# Step 1: Initial draw at normal speed
tracer(1, 1)
draw_flower(0)

# Step 2: Set up smooth rotation
current_angle = 0
tracer(0, 0)

def rotate():
    global current_angle
    clear()
    current_angle -= 1
    draw_flower(current_angle)
    update()
    ontimer(rotate, 20)

# Step 3: Start rotation loop centered via setworldcoordinates
rotate()
done()
