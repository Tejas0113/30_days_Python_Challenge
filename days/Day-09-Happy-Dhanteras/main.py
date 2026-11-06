
"""
Day 09: Happy Dhanteras Animated Festival Poster
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
An animated devotional festival poster celebrating Dhanteras using Python Turtle graphics.
Features cubic Bézier curved brass Kalash and realistic clay diyas, dynamic flame flicker physics,
falling gold coins particle shower, and exploding multi-color aerial fireworks.
"""

import turtle
import random
import math

# ==================================================
# DHANTERAS FESTIVAL POSTER
# Realistic Diyas + Smooth Wind Animation
# ==================================================

screen = turtle.Screen()
screen.setup(900, 900)
screen.title("Happy Dhanteras")
screen.bgcolor("#080D25")
screen.setworldcoordinates(-450, -450, 450, 450)
screen.tracer(0, 0)

# ==================================================
# COLORS
# ==================================================

GOLD = "#FFD700"
LIGHT_GOLD = "#FFF0A6"
BRONZE = "#B87919"
DARK_GOLD = "#805000"
ORANGE = "#FF8C00"
RED = "#D62828"
WHITE = "#FFF8E7"
CYAN = "#39D5FF"
PINK = "#FF5FA2"
PURPLE = "#A78BFA"
GREEN = "#248B45"


# ==================================================
# TURTLE HELPERS
# ==================================================

def make_turtle(color="white"):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.color(color)
    return t


def draw_dot(t, x, y, size, color):
    t.penup()
    t.goto(x, y)
    t.dot(size, color)


def draw_line(t, x1, y1, x2, y2, color, width=2):
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.pencolor(color)
    t.pensize(width)
    t.goto(x2, y2)
    t.penup()


def draw_polygon(t, points, color, outline=None, width=1):
    if len(points) < 3:
        return

    t.penup()
    t.goto(points[0])
    t.pencolor(outline if outline else color)
    t.fillcolor(color)
    t.pensize(width)
    t.pendown()
    t.begin_fill()

    for point in points[1:]:
        t.goto(point)

    t.goto(points[0])
    t.end_fill()
    t.penup()


def write_text(t, x, y, message, size, color,
               font="Arial", style="bold"):
    t.penup()
    t.goto(x, y)
    t.color(color)
    t.write(
        message,
        align="center",
        font=(font, size, style)
    )


def bezier(p0, p1, p2, p3, steps=20):
    points = []

    for i in range(steps + 1):
        u = i / steps

        x = (
            (1-u)**3 * p0[0]
            + 3 * (1-u)**2 * u * p1[0]
            + 3 * (1-u) * u**2 * p2[0]
            + u**3 * p3[0]
        )

        y = (
            (1-u)**3 * p0[1]
            + 3 * (1-u)**2 * u * p1[1]
            + 3 * (1-u) * u**2 * p2[1]
            + u**3 * p3[1]
        )

        points.append((x, y))

    return points


# ==================================================
# BACKGROUND STARS
# ==================================================

stars = make_turtle()

for _ in range(85):
    x = random.randint(-430, 430)
    y = random.randint(-430, 430)

    if -190 < x < 190 and -130 < y < 230:
        continue

    draw_dot(
        stars,
        x, y,
        random.choice([2, 3, 4]),
        random.choice([GOLD, WHITE, CYAN])
    )


# ==================================================
# MAIN GREETING
# ==================================================

heading = make_turtle(GOLD)

write_text(
    heading, 0, 270,
    "THE FESTIVAL OF WEALTH",
    17, LIGHT_GOLD
)

write_text(
    heading, 0, 175,
    "HAPPY",
    42, WHITE
)

write_text(
    heading, 0, 105,
    "DHANTERAS",
    55, GOLD, "Georgia"
)

draw_line(
    heading, -190, 85, 190, 85,
    DARK_GOLD, 3
)

write_text(
    heading, 0, 25,
    "May prosperity and happiness",
    19, WHITE, "Georgia", "normal"
)

write_text(
    heading, 0, -8,
    "shine in your life.",
    19, WHITE, "Georgia", "normal"
)

write_text(
    heading, 0, -75,
    "SHUBH DHANTERAS",
    25, LIGHT_GOLD, "Georgia"
)


# ==================================================
# REALISTIC BRASS KALASH
# ==================================================

def draw_kalash(cx, cy):

    t = make_turtle()

    left = bezier(
        (cx - 34, cy + 58),
        (cx - 45, cy + 28),
        (cx - 82, cy + 10),
        (cx - 78, cy - 28)
    )

    left += bezier(
        (cx - 78, cy - 28),
        (cx - 76, cy - 78),
        (cx - 48, cy - 111),
        (cx - 27, cy - 116)
    )[1:]

    bottom = bezier(
        (cx - 27, cy - 116),
        (cx - 12, cy - 123),
        (cx + 12, cy - 123),
        (cx + 27, cy - 116)
    )[1:]

    right = bezier(
        (cx + 27, cy - 116),
        (cx + 48, cy - 111),
        (cx + 76, cy - 78),
        (cx + 78, cy - 28)
    )[1:]

    right += bezier(
        (cx + 78, cy - 28),
        (cx + 82, cy + 10),
        (cx + 45, cy + 28),
        (cx + 34, cy + 58)
    )[1:]

    draw_polygon(
        t,
        left + bottom + right,
        "#C68A22",
        "#FFE08A",
        3
    )

    highlight = bezier(
        (cx - 55, cy + 10),
        (cx - 72, cy - 20),
        (cx - 58, cy - 75),
        (cx - 35, cy - 91)
    )

    t.penup()
    t.goto(highlight[0])
    t.pendown()
    t.pencolor("#FFE7A0")
    t.pensize(5)

    for point in highlight[1:]:
        t.goto(point)

    t.penup()

    shadow = bezier(
        (cx + 55, cy + 5),
        (cx + 75, cy - 30),
        (cx + 55, cy - 83),
        (cx + 35, cy - 99)
    )

    t.penup()
    t.goto(shadow[0])
    t.pendown()
    t.pencolor("#8A510C")
    t.pensize(4)

    for point in shadow[1:]:
        t.goto(point)

    t.penup()

    # Neck
    draw_polygon(
        t,
        [
            (cx - 34, cy + 58),
            (cx - 30, cy + 91),
            (cx + 30, cy + 91),
            (cx + 34, cy + 58)
        ],
        "#DCA83F",
        LIGHT_GOLD,
        2
    )

    # Rim
    draw_polygon(
        t,
        [
            (cx - 43, cy + 87),
            (cx - 43, cy + 98),
            (cx + 43, cy + 98),
            (cx + 43, cy + 87)
        ],
        LIGHT_GOLD,
        "#FFF5C7",
        2
    )

    draw_line(
        t, cx - 40, cy + 92,
        cx + 40, cy + 92,
        "#9A5A10", 2
    )

    # Decorative bands
    draw_line(
        t, cx - 70, cy - 15,
        cx + 70, cy - 15,
        LIGHT_GOLD, 4
    )

    draw_line(
        t, cx - 66, cy - 23,
        cx + 66, cy - 23,
        DARK_GOLD, 2
    )

    draw_line(
        t, cx - 59, cy - 88,
        cx + 59, cy - 88,
        LIGHT_GOLD, 4
    )

    draw_line(
        t, cx - 54, cy - 95,
        cx + 54, cy - 95,
        DARK_GOLD, 2
    )

    for angle in range(0, 360, 30):
        a = math.radians(angle)
        x = cx + math.cos(a) * 47
        y = cy - 48 + math.sin(a) * 12
        draw_dot(t, x, y, 5, LIGHT_GOLD)

    draw_dot(t, cx, cy - 48, 15, RED)
    draw_dot(t, cx, cy - 48, 7, GOLD)

    # Coconut
    draw_dot(t, cx, cy + 116, 44, "#89501F")
    draw_dot(t, cx - 9, cy + 125, 23, "#B97935")
    draw_dot(t, cx + 10, cy + 107, 18, "#603718")

    for offset in [-13, 0, 13]:
        draw_line(
            t,
            cx + offset, cy + 101,
            cx + offset - 4, cy + 131,
            "#E5B56B", 2
        )

    # Mango leaves
    leaves = [
        ([(cx, cy+100), (cx-35, cy+135),
          (cx-88, cy+145), (cx-54, cy+104)], "#176B37"),

        ([(cx, cy+105), (cx-15, cy+160),
          (cx-38, cy+183), (cx-24, cy+124)], "#228B45"),

        ([(cx, cy+105), (cx+15, cy+160),
          (cx+38, cy+183), (cx+24, cy+124)], "#2E9D50"),

        ([(cx, cy+100), (cx+35, cy+135),
          (cx+88, cy+145), (cx+54, cy+104)], "#14552E"),

        ([(cx-5, cy+100), (cx-75, cy+112),
          (cx-100, cy+95), (cx-38, cy+94)], "#3A9D45"),

        ([(cx+5, cy+100), (cx+75, cy+112),
          (cx+100, cy+95), (cx+38, cy+94)], "#248B45")
    ]

    for points, color in leaves:
        draw_polygon(t, points, color, "#8CCB65", 2)
        draw_line(
            t,
            points[0][0], points[0][1],
            points[2][0], points[2][1],
            "#A9D875", 1
        )

    draw_dot(t, cx, cy + 116, 7, RED)


draw_kalash(0, -300)


# ==================================================
# REALISTIC DIYAS
# ==================================================

# The bowl is drawn once.
# Only the flame is redrawn during animation.

diya_positions = [-330, 330]

diya_flames = turtle.Turtle()
diya_flames.hideturtle()
diya_flames.speed(0)
diya_flames.penup()

diya_glow = turtle.Turtle()
diya_glow.hideturtle()
diya_glow.speed(0)
diya_glow.penup()


def draw_diya_bowl(cx, cy):

    t = make_turtle()

    # Pedestal/base
    draw_polygon(
        t,
        [
            (cx - 42, cy - 20),
            (cx - 35, cy - 29),
            (cx + 35, cy - 29),
            (cx + 42, cy - 20)
        ],
        "#8D4D15",
        GOLD,
        2
    )

    # Curved bowl silhouette
    bowl = []

    bowl += bezier(
        (cx - 58, cy + 4),
        (cx - 45, cy - 10),
        (cx - 26, cy - 24),
        (cx, cy - 24),
        18
    )

    bowl += bezier(
        (cx, cy - 24),
        (cx + 26, cy - 24),
        (cx + 45, cy - 10),
        (cx + 58, cy + 4),
        18
    )[1:]

    bowl += bezier(
        (cx + 58, cy + 4),
        (cx + 28, cy + 15),
        (cx - 28, cy + 15),
        (cx - 58, cy + 4),
        18
    )[1:]

    draw_polygon(
        t,
        bowl,
        "#A95719",
        "#FFD16B",
        3
    )

    # Metallic outer rim
    rim = bezier(
        (cx - 58, cy + 4),
        (cx - 25, cy + 19),
        (cx + 25, cy + 19),
        (cx + 58, cy + 4),
        20
    )

    t.penup()
    t.goto(rim[0])
    t.pendown()
    t.pencolor(LIGHT_GOLD)
    t.pensize(4)

    for point in rim[1:]:
        t.goto(point)

    t.penup()

    # Inner oil surface
    draw_dot(t, cx, cy + 1, 47, "#5D3215")
    draw_dot(t, cx, cy + 2, 34, "#A66B21")

    # Oil reflection
    draw_line(
        t,
        cx - 19, cy + 5,
        cx + 5, cy + 7,
        "#FFE09A", 2
    )

    # Decorative engraved pattern
    for offset in [-34, -17, 0, 17, 34]:
        draw_dot(
            t,
            cx + offset,
            cy - 12,
            4,
            LIGHT_GOLD
        )

    # Decorative band
    draw_line(
        t,
        cx - 33, cy - 23,
        cx + 33, cy - 23,
        "#FFD16B", 2
    )

    # Wick holder
    draw_dot(t, cx, cy + 10, 9, DARK_GOLD)

    # Cotton wick
    draw_line(
        t,
        cx, cy + 9,
        cx + 2, cy + 22,
        WHITE, 4
    )

    # Wick tip
    draw_dot(t, cx + 2, cy + 22, 5, "#F5D7A2")


# Draw both stationary diya bowls
for x in diya_positions:
    draw_diya_bowl(x, -350)


# ==================================================
# ANIMATED DIYA FLAME
# ==================================================

# Each flame has a slightly different phase and sway.
# This creates a natural breeze effect.

flame_data = [
    {
        "x": -330,
        "y": -328,
        "phase": 0.0,
        "speed": 0.075,
        "strength": 5.0
    },
    {
        "x": 330,
        "y": -328,
        "phase": 2.2,
        "speed": 0.068,
        "strength": 4.2
    }
]


def draw_curved_flame(t, x, y, height, width,
                      sway, color):

    # The flame bends gently at its tip.
    tip_x = x + sway

    left = bezier(
        (x - width / 2, y),
        (x - width * 0.8, y + height * 0.35),
        (tip_x - width * 0.4, y + height * 0.75),
        (tip_x, y + height),
        14
    )

    right = bezier(
        (tip_x, y + height),
        (tip_x + width * 0.65, y + height * 0.7),
        (x + width * 0.9, y + height * 0.25),
        (x + width / 2, y),
        14
    )

    draw_polygon(
        t,
        left + right,
        color
    )


def animate_diya_flames(frame):

    diya_flames.clear()
    diya_glow.clear()

    for flame in flame_data:

        flame["phase"] += flame["speed"]

        phase = flame["phase"]

        # Gentle continuous wind movement
        sway = (
            math.sin(phase) * flame["strength"]
            + math.sin(phase * 0.55) * 1.5
        )

        # Subtle natural flame height variation
        height = (
            42
            + math.sin(phase * 1.7) * 3
            + math.sin(phase * 0.7) * 2
        )

        width = 17 + math.sin(phase * 1.2) * 1.5

        x = flame["x"]
        y = flame["y"]

        # Soft outer glow
        diya_glow.goto(x + sway * 0.3, y + 14)
        diya_glow.dot(43, "#542D19")

        diya_glow.goto(x + sway * 0.3, y + 18)
        diya_glow.dot(28, "#8A471A")

        # Outer orange flame
        draw_curved_flame(
            diya_flames,
            x, y,
            height,
            width,
            sway,
            "#FF7A18"
        )

        # Inner golden flame
        draw_curved_flame(
            diya_flames,
            x + 1, y + 2,
            height * 0.72,
            width * 0.62,
            sway * 0.65,
            "#FFD23F"
        )

        # Bright central flame
        draw_curved_flame(
            diya_flames,
            x + 1, y + 3,
            height * 0.42,
            width * 0.32,
            sway * 0.35,
            "#FFF4BC"
        )

        # Bright core
        diya_glow.goto(
            x + sway * 0.2,
            y + 12
        )
        diya_glow.dot(5, WHITE)


# ==================================================
# CONTINUOUS FIREWORKS
# ==================================================

firework_colors = [
    GOLD, ORANGE, PINK, CYAN,
    PURPLE, RED, WHITE
]

rockets = []
particles = []
rocket_trails = []

rocket_pen = make_turtle()
particle_pen = make_turtle()
trail_pen = make_turtle()

launch_counter = 0
next_launch = random.randint(18, 30)


def launch_rocket():

    possible_x = [
        random.randint(-410, -235),
        random.randint(235, 410)
    ]

    x = random.choice(possible_x)

    start_y = random.randint(-420, -250)
    target_y = random.randint(240, 410)

    rockets.append({
        "x": float(x),
        "y": float(start_y),
        "target_y": target_y,
        "speed": random.uniform(5.0, 8.0),
        "color": random.choice(firework_colors)
    })


def explode(x, y, color):

    ring_count = random.choice([2, 3])

    for ring in range(ring_count):

        count = random.randint(22, 34)
        base_speed = random.uniform(2.2, 4.8)
        offset = random.uniform(0, 360)

        for i in range(count):

            angle = math.radians(
                offset + i * (360 / count)
            )

            speed = base_speed * random.uniform(0.75, 1.2)

            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            particle_color = (
                color if random.random() < 0.7
                else random.choice(firework_colors)
            )

            particles.append({
                "x": float(x),
                "y": float(y),
                "vx": vx,
                "vy": vy,
                "life": random.randint(35, 65),
                "max_life": 65,
                "color": particle_color,
                "size": random.choice([2, 3, 4]),
                "gravity": random.uniform(0.035, 0.065)
            })

    # Central sparkle
    for _ in range(12):

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)

        particles.append({
            "x": float(x),
            "y": float(y),
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": 20,
            "max_life": 20,
            "color": LIGHT_GOLD,
            "size": 4,
            "gravity": 0.04
        })


def update_rockets():

    for rocket in rockets[:]:

        rocket["y"] += rocket["speed"]

        x = rocket["x"]
        y = rocket["y"]

        rocket_trails.append({
            "x": x,
            "y": y - 12,
            "life": 12,
            "max_life": 12,
            "color": random.choice([GOLD, ORANGE, WHITE])
        })

        rocket_pen.goto(x, y)
        rocket_pen.dot(9, rocket["color"])

        rocket_pen.goto(x, y - 7)
        rocket_pen.dot(5, WHITE)

        rocket_pen.goto(x, y + 5)
        rocket_pen.dot(4, LIGHT_GOLD)

        if y >= rocket["target_y"]:

            explode(x, y, rocket["color"])
            rockets.remove(rocket)


def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["vy"] -= particle["gravity"]

        particle["vx"] *= 0.985
        particle["vy"] *= 0.985

        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)
            continue

        ratio = particle["life"] / particle["max_life"]

        size = max(
            1,
            int(particle["size"] * ratio)
        )

        particle_pen.goto(
            particle["x"],
            particle["y"]
        )

        particle_pen.dot(
            size,
            particle["color"]
        )


def update_rocket_trails():

    for trail in rocket_trails[:]:

        trail["life"] -= 1

        if trail["life"] <= 0:
            rocket_trails.remove(trail)
            continue

        ratio = trail["life"] / trail["max_life"]

        trail_pen.goto(
            trail["x"],
            trail["y"]
        )

        trail_pen.dot(
            max(1, int(5 * ratio)),
            trail["color"]
        )


def animate_fireworks():

    global launch_counter, next_launch

    rocket_pen.clear()
    particle_pen.clear()
    trail_pen.clear()

    launch_counter += 1

    if launch_counter >= next_launch:
        launch_rocket()
        launch_counter = 0
        next_launch = random.randint(18, 30)

    update_rockets()
    update_rocket_trails()
    update_particles()


# Initial rockets
for _ in range(3):
    launch_rocket()


# ==================================================
# FALLING GOLD COINS
# ==================================================

coins = []

for _ in range(28):

    coin = turtle.Turtle()
    coin.shape("circle")
    coin.color(GOLD)
    coin.shapesize(
        random.uniform(0.45, 0.8),
        random.uniform(0.45, 0.8)
    )
    coin.penup()
    coin.speed(0)

    if random.random() < 0.5:
        x = random.randint(-430, -250)
    else:
        x = random.randint(250, 430)

    y = random.randint(-100, 450)

    coin.goto(x, y)

    coins.append({
        "turtle": coin,
        "x": x,
        "y": y,
        "speed": random.uniform(2, 5)
    })


def animate_coins():

    for item in coins:

        item["y"] -= item["speed"]

        if item["y"] < -460:

            item["y"] = random.randint(440, 650)

            if random.random() < 0.5:
                item["x"] = random.randint(-430, -250)
            else:
                item["x"] = random.randint(250, 430)

            item["speed"] = random.uniform(2, 5)

        item["turtle"].goto(
            item["x"],
            item["y"]
        )


# ==================================================
# FOOTER
# ==================================================

footer = make_turtle(LIGHT_GOLD)

write_text(
    footer,
    0, -425,
    "WEALTH  |  HEALTH  |  HAPPINESS",
    13, LIGHT_GOLD
)


# ==================================================
# MAIN ANIMATION LOOP
# ==================================================

animation_frame = 0


def main_animation():

    global animation_frame

    animation_frame += 1

    animate_coins()
    animate_fireworks()

    # Smooth diya flame animation
    animate_diya_flames(animation_frame)

    screen.update()

    # Approximately 40 FPS
    screen.ontimer(main_animation, 25)


# ==================================================
# START
# ==================================================

def main():
    try:
        main_animation()
        turtle.done()
    except (turtle.Terminator, KeyboardInterrupt, Exception):
        pass


if __name__ == "__main__":
    main()
