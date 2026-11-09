import colorsys as sm
import turtle as r

# Maximize render speed
r.tracer(0, 0)
r.speed(0)
r.hideturtle()
r.bgcolor("black")
r.pensize(2)

h = 0
n = 400  # Number of overlapping layers

for i in range(n):
  for j in range(4):
    # Keep 'h' strictly between 0.0 and 1.0 using modulo
    c = sm.hsv_to_rgb(h % 1.0, 1, 1)
    h += 0.0025  # Smooth, gradual color shift
    r.color(c)

    # Scale the shapes outward to create the expanding overlap
    r.circle(30 + (i * 0.3) + (j * 4), 90)
    r.forward(80 + (i * 0.1))
    r.left(90)

  # Adjust rotation to form the tight, curved loop
  r.right(11)

  if i % 5 == 0:
    r.update()

r.update()
r.done()
