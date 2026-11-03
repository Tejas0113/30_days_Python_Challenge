"""
Day 06: Cosmic Vortex Generative Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A procedural generative art piece exploring logarithmic spiral growth, asymmetric
angular divergence, and continuous HSV color cycles using Python Turtle graphics.
"""

import colorsys
import turtle as t


def draw_cosmic_vortex():
    t.bgcolor("black")
    t.tracer(3)
    t.pensize(1)
    t.hideturtle()

    # Set up screen bounds for visual centering
    t.setup(width=800, height=800)
    t.screensize(canvwidth=800, canvheight=800)
    t.title("Day 06: Cosmic Vortex Generative Art")

    h = 0.5

    for i in range(250):
        c = colorsys.hsv_to_rgb(h % 1.0, 1, 1)
        h += 0.008
        t.fillcolor(c)
        t.begin_fill()
        t.fd(i)
        t.lt(100)
        t.circle(30)
        for j in range(2):
            t.fd(i * j)
            t.rt(109)
        t.end_fill()

    t.update()


def main():
    try:
        draw_cosmic_vortex()
        t.done()
    except (t.Terminator, KeyboardInterrupt, Exception):
        pass


if __name__ == "__main__":
    main()
