import time
import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Day 3: Animated Analog Clock")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)  # Turn off automatic screen updates for smooth animation

# Create the clock face drawer
clock_face = turtle.Turtle()
clock_face.hideturtle()
clock_face.speed(0)
clock_face.color("white")

# Draw clock outer circle
clock_face.penup()
clock_face.goto(0, -210)
clock_face.pendown()
clock_face.pensize(5)
clock_face.circle(210)

# Draw clock hour markings
clock_face.penup()
clock_face.goto(0, 0)
clock_face.setheading(90)

for _ in range(12):
    clock_face.forward(190)
    clock_face.pendown()
    clock_face.forward(15)
    clock_face.penup()
    clock_face.goto(0, 0)
    clock_face.right(30)

# Create turtles for clock hands
sec_hand = turtle.Turtle()
sec_hand.shape("arrow")
sec_hand.color("red")
sec_hand.pensize(2)

min_hand = turtle.Turtle()
min_hand.shape("arrow")
min_hand.color("white")
min_hand.pensize(4)

hour_hand = turtle.Turtle()
hour_hand.shape("arrow")
hour_hand.color("white")
hour_hand.pensize(6)

for hand in (sec_hand, min_hand, hour_hand):
    hand.speed(0)
    hand.penup()


def update_clock():
    # Get current local system time
    current_time = time.localtime()
    hrs = current_time.tm_hour % 12
    mins = current_time.tm_min
    secs = current_time.tm_sec

    # Calculate angles for hands (0 degrees points straight UP)
    sec_angle = 90 - (secs * 6)
    min_angle = 90 - (mins * 6 + secs * 0.1)
    hour_angle = 90 - (hrs * 30 + mins * 0.5)

    # Position Second Hand
    sec_hand.goto(0, 0)
    sec_hand.setheading(sec_angle)
    sec_hand.forward(170)

    # Position Minute Hand
    min_hand.goto(0, 0)
    min_hand.setheading(min_angle)
    min_hand.forward(140)

    # Position Hour Hand
    hour_hand.goto(0, 0)
    hour_hand.setheading(hour_angle)
    hour_hand.forward(90)

    # Refresh the screen
    screen.update()

    # Clear hands before redrawing next tick
    sec_hand.clear()
    min_hand.clear()
    hour_hand.clear()


# Main animation loop
try:
    while True:
        update_clock()
        time.sleep(0.1)  # Smooth update tick
except turtle.TerminatorError:
    pass  # Handle graceful window closure
