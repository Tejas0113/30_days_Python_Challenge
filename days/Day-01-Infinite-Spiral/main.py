"""
Day 01: Infinite Rainbow Spiral
30 Days Python Challenge by Tejas (@Tejas0113)

A high-performance dynamic generative art project built with Python's Turtle
graphics and colorsys module. Uses HSV color wheel theory and manual frame
buffering (tracer/update) to achieve smooth 60 FPS spinning neon geometry.
"""

import colorsys
import turtle


def main():
    # 1. Screen setup
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Day 01 - Infinite Rainbow Spiral | 30 Days Python Challenge")
    screen.setup(width=680, height=720)
    screen.tracer(0)  # Turn off automatic updates for clean, tearing-free frame rendering

    # 2. Pen configuration
    t = turtle.Turtle()
    t.hideturtle()
    t.width(1.8)

    angle_offset = 0

    print("🌀 Day 01: Infinite Rainbow Spiral running...")
    print("👉 Close the turtle window or press Ctrl+C in terminal to exit.")

    # 3. Infinite Rotation Loop with graceful exit handling
    try:
        while True:
            t.clear()  # Clear previous frame

            # Reset position to compensated center
            t.penup()
            t.goto(60, -80)
            t.setheading(angle_offset)
            t.pendown()

            # Draw one frame of the geometric spiral
            n = 220  # Optimized line count for high FPS rotation
            for i in range(n):
                hue = i / n
                rgb = colorsys.hsv_to_rgb(hue, 0.95, 1.0)
                t.pencolor(rgb)

                t.forward(i * 0.8)
                t.left(59)

            screen.update()  # Push completed buffer to display
            angle_offset += 1.5  # Increment rotation angle
    except (turtle.Terminator, KeyboardInterrupt):
        print("\n✨ Spiral closed gracefully. Great start to Day 01!")


if __name__ == "__main__":
    main()
