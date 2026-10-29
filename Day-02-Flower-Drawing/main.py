import math
import random
import turtle

random.seed(7)

screen = turtle.Screen()
screen.setup(800, 480)
screen.bgcolor("#12001c")
screen.title("Python Turtle: Flower Drawing")
screen.setworldcoordinates(-400, -240, 400, 240)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()


def stars():
    t.penup()
    for _ in range(70):
        x = random.randint(-390, 390)
        y = random.randint(-230, 230)
        t.goto(x, y)
        t.dot(random.randint(2, 4), "white")


def stem():
    t.penup()
    t.goto(0, 60)
    t.setheading(-72)
    t.pendown()
    t.color("green")
    t.pensize(7)
    t.circle(-420, 34)


def leaf(x, y, angle):
    t.penup()
    t.goto(x, y)
    t.setheading(angle)
    t.color("#1e6b3c", "#2e9e5b")
    t.pensize(2)
    t.begin_fill()
    t.pendown()
    t.circle(70, 70)
    t.left(110)
    t.circle(70, 70)
    t.end_fill()


def draw_petal(length, angle_span, fill_color, border_color):
    t.color(border_color, fill_color)
    t.begin_fill()
    for _ in range(2):
        t.circle(length, angle_span)
        t.left(180 - angle_span)
    t.end_fill()


def flower():
    center_x, center_y = 0, 60

    # Outer petals (deep magenta / rose)
    petals_outer = 16
    for i in range(petals_outer):
        t.penup()
        t.goto(center_x, center_y)
        t.setheading(i * (360 / petals_outer))
        t.pendown()
        t.pensize(1)
        draw_petal(110, 60, "#c2185b", "#ff4081")

    # Middle petals (bright pink / coral)
    petals_mid = 12
    for i in range(petals_mid):
        t.penup()
        t.goto(center_x, center_y)
        t.setheading(i * (360 / petals_mid) + 15)
        t.pendown()
        draw_petal(85, 60, "#e91e63", "#ff80ab")

    # Inner petals (soft peach)
    petals_inner = 8
    for i in range(petals_inner):
        t.penup()
        t.goto(center_x, center_y)
        t.setheading(i * (360 / petals_inner) + 30)
        t.pendown()
        draw_petal(55, 60, "#ff6e40", "#ffab91")

    # Glowing center core
    t.penup()
    t.goto(center_x, center_y - 20)
    t.setheading(0)
    t.color("#ffd54f", "#ffca28")
    t.begin_fill()
    t.pendown()
    t.circle(20)
    t.end_fill()

    # Center spiral dots
    t.penup()
    for i in range(35):
        r = 3 * math.sqrt(i)
        theta = math.radians(i * 137.508)
        x = center_x + r * math.cos(theta)
        y = center_y + r * math.sin(theta)
        t.goto(x, y)
        t.dot(3, "#5f4037")


def main():
    stars()
    stem()
    flower()
    leaf(16, -130, 25)
    leaf(11, -160, 155)
    turtle.done()


if __name__ == "__main__":
    main()
