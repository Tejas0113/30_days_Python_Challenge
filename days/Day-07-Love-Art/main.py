"""
Day 07: Love Art - Parametric Mathematical Heart Curve
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A generative mathematical art visualizer rendering a parametric cardioid heart curve
via radial ray-tracing and integer angular stepping using Python Turtle graphics.
"""

import math
import turtle as t


def hearta(k: float) -> float:
    """Calculate the x-coordinate factor of the parametric heart curve."""
    return 15 * math.sin(k) ** 3


def heartb(k: float) -> float:
    """Calculate the y-coordinate factor of the parametric heart curve."""
    return (
        12 * math.cos(k)
        - 5 * math.cos(2 * k)
        - 2 * math.cos(3 * k)
        - math.cos(4 * k)
    )


def draw_love_art():
    """Renders the parametric neon heart curve with radial chord string-art lines."""
    t.setup(width=800, height=800)
    t.setworldcoordinates(-450, -450, 450, 450)
    t.title("Day 07: Love Art (Parametric Heart Curve)")

    t.speed(0)
    t.tracer(200)
    t.hideturtle()
    t.bgcolor("black")
    t.color("#f73487")

    for i in range(6000):
        t.goto(hearta(i) * 20, heartb(i) * 20)
        t.goto(0, 0)

    t.update()


def main():
    try:
        draw_love_art()
        t.done()
    except (t.Terminator, KeyboardInterrupt, Exception):
        pass


if __name__ == "__main__":
    main()
