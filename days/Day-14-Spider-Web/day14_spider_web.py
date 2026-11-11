"""
Day 14: Interactive Spider Web on a Building Corner
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A visually stunning, realistic, and interactive architectural artwork entirely in Python:
1. Architectural Scene:
   - Realistic exterior outside corner of a modernist concrete building.
   - Two intersecting walls meeting at a vertical corner seam with perspective recession.
   - Subtle concrete texture, architectural formwork seams, tie-rod holes, and light shadows.
2. Realistic Spider Web Construction:
   - Natural radial silk threads anchored to both walls and along the corner crease.
   - Curved connecting spiral threads modeled with catenary sagging arcs (Bézier tension).
   - Natural irregular spacing, piriform attachment pads, and fine variations in thread weight.
   - Monochromatic, minimal, and premium architectural aesthetic.
3. Interactive Mouse Dynamics:
   - Initially almost invisible (barely a whisper of light reflecting off silk).
   - Approaching the building corner gradually reveals delicate web strands.
   - Moving directly over the web reveals the complete, intricate spider web.
   - Moving away causes the web to smoothly fade out.
   - Subtle aerodynamic breeze & air tension physics: mouse motion disturbs air currents,
     causing silk strands to gently flutter and vibrate with damped wave physics.
   - Smooth continuous response without requiring clicking.

Controls:
  Mouse Movement  - Proximity reveal & aerodynamic air disturbance
  [SPACE]         - Trigger a sudden breeze gust
  [W]             - Toggle ambient wind drift (On / Off)
  [S]             - Save high-resolution screenshot
  [F]             - Toggle fullscreen mode
  [ESC/Q]         - Exit application
"""

import math
import os
import random
import sys
import numpy as np
import pygame

# 1. Canvas & Architectural Configuration
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 750
FPS = 60

# Architectural Dimensions
CORNER_X = 420      # Vertical corner line position (X)
Y_ROOF_L = 115      # Left wall roofline top-left Y
Y_ROOF_C = 75       # Corner vertex roofline Y
Y_ROOF_R = 125      # Right wall roofline top-right Y

# Architectural Palette (Monochromatic Minimalist Concrete)
COLOR_SKY = (245, 246, 249)           # Architectural overcast sky
COLOR_WALL_LEFT = (236, 238, 241)     # Left wall (lit concrete face)
COLOR_WALL_RIGHT = (222, 226, 231)    # Right wall (shadowed concrete face)
COLOR_CORNER_LINE = (185, 192, 200)   # Vertical corner crease seam
COLOR_CORNER_HILITE = (252, 253, 255) # Vertical corner edge highlight
COLOR_PARAPET_L = (165, 172, 180)     # Parapet roof coping left
COLOR_PARAPET_R = (150, 156, 165)     # Parapet roof coping right
COLOR_SEAM_SHADOW = (212, 216, 222)   # Formwork horizontal seam shadow
COLOR_SEAM_HILITE = (248, 250, 252)   # Formwork horizontal seam highlight
COLOR_TIEROD = (175, 182, 190)        # Tie-rod formwork anchor impressions

# Spider Silk Palette
COLOR_SILK_CORE = (38, 42, 48)        # Charcoal black silk fiber core
COLOR_SILK_HILITE = (225, 230, 238)   # Translucent specular silk glint
COLOR_SILK_SHADOW = (20, 24, 30)      # Ambient cast shadow on concrete


def create_architectural_background(width, height):
    """
    Renders a realistic modernist concrete building corner with perspective recession,
    board-formed concrete casting seams, tie-rod holes, and parapet coping.
    """
    bg = pygame.Surface((width, height)).convert()
    bg.fill(COLOR_SKY)

    # 1. Left Wall (Direct ambient light)
    pts_left = [(0, Y_ROOF_L), (CORNER_X, Y_ROOF_C), (CORNER_X, height), (0, height)]
    pygame.draw.polygon(bg, COLOR_WALL_LEFT, pts_left)

    # 2. Right Wall (Directional shadow side)
    pts_right = [(CORNER_X, Y_ROOF_C), (width, Y_ROOF_R), (width, height), (CORNER_X, height)]
    pygame.draw.polygon(bg, COLOR_WALL_RIGHT, pts_right)

    # 3. Horizontal Board-Formed Concrete Casting Seams
    seam_spacing = 85
    for y_c in range(Y_ROOF_C + seam_spacing, height - 30, seam_spacing):
        # Left wall seam (perspective slope towards corner)
        y_l = int(y_c + (Y_ROOF_L - Y_ROOF_C) * (1.0 - 0.0 / CORNER_X))
        pygame.draw.line(bg, COLOR_SEAM_SHADOW, (0, y_l), (CORNER_X, y_c), 1)
        pygame.draw.line(bg, COLOR_SEAM_HILITE, (0, y_l + 1), (CORNER_X, y_c + 1), 1)

        # Right wall seam (perspective slope away from corner)
        y_r = int(y_c + (Y_ROOF_R - Y_ROOF_C) * (1.0))
        pygame.draw.line(bg, (208, 212, 218), (CORNER_X, y_c), (width, y_r), 1)
        pygame.draw.line(bg, (235, 239, 244), (CORNER_X, y_c + 1), (width, y_r + 1), 1)

        # Tie-rod formwork holes (classic architectural concrete casting discs)
        # Left wall tie-rods (two per panel)
        for fx in [0.28, 0.68]:
            tx = int(CORNER_X * fx)
            ty = int(y_c - seam_spacing * 0.5 + (Y_ROOF_L - Y_ROOF_C) * (1.0 - fx))
            pygame.draw.circle(bg, COLOR_TIEROD, (tx, ty), 4)
            pygame.draw.circle(bg, (200, 205, 212), (tx, ty), 3)
            pygame.draw.circle(bg, (155, 162, 170), (tx, ty), 2)
            pygame.draw.circle(bg, (255, 255, 255), (tx - 1, ty - 1), 1)

        # Right wall tie-rods
        for fx in [0.32, 0.72]:
            tx = int(CORNER_X + (width - CORNER_X) * fx)
            ty = int(y_c - seam_spacing * 0.5 + (Y_ROOF_R - Y_ROOF_C) * fx)
            pygame.draw.circle(bg, (195, 200, 208), (tx, ty), 4)
            pygame.draw.circle(bg, (180, 185, 192), (tx, ty), 3)
            pygame.draw.circle(bg, (140, 146, 155), (tx, ty), 2)
            pygame.draw.circle(bg, (245, 248, 252), (tx - 1, ty - 1), 1)

    # 4. Vertical Corner Crease Seam (Crisp architectural bevel)
    pygame.draw.line(bg, COLOR_CORNER_LINE, (CORNER_X, Y_ROOF_C), (CORNER_X, height), 2)
    pygame.draw.line(bg, COLOR_CORNER_HILITE, (CORNER_X - 1, Y_ROOF_C), (CORNER_X - 1, height), 1)

    # 5. Roofline Parapet Coping
    pygame.draw.line(bg, COLOR_PARAPET_L, (0, Y_ROOF_L), (CORNER_X, Y_ROOF_C), 3)
    pygame.draw.line(bg, COLOR_PARAPET_R, (CORNER_X, Y_ROOF_C), (width, Y_ROOF_R), 3)
    pygame.draw.line(bg, (255, 255, 255), (0, Y_ROOF_L - 1), (CORNER_X, Y_ROOF_C - 1), 1)
    pygame.draw.line(bg, (250, 252, 255), (CORNER_X, Y_ROOF_C - 1), (width, Y_ROOF_R - 1), 1)

    # 6. Procedural Subtle Concrete Surface Noise (High-frequency fine grain)
    np.random.seed(42)
    noise_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    noise_arr = np.random.randint(-5, 6, size=(height, width), dtype=np.int16)
    # Apply subtle grain
    pixels = pygame.surfarray.pixels3d(noise_overlay)
    alphas = pygame.surfarray.pixels_alpha(noise_overlay)
    # Mask to wall area
    for y in range(Y_ROOF_C, height, 2):
        for x in range(0, width, 2):
            if (x < CORNER_X and y >= Y_ROOF_L + (Y_ROOF_C - Y_ROOF_L) * (x / CORNER_X)) or \
               (x >= CORNER_X and y >= Y_ROOF_C + (Y_ROOF_R - Y_ROOF_C) * ((x - CORNER_X) / (width - CORNER_X))):
                v = noise_arr[y, x]
                if v > 0:
                    pixels[x, y] = (255, 255, 255)
                    alphas[x, y] = min(18, v * 3)
                elif v < 0:
                    pixels[x, y] = (0, 0, 0)
                    alphas[x, y] = min(18, -v * 3)
    del pixels
    del alphas
    bg.blit(noise_overlay, (0, 0))

    return bg


def ray_segment_intersect(ray_origin, ray_dir, p1, p2):
    """Computes ray-segment intersection for spider spoke framing."""
    ox, oy = ray_origin
    dx, dy = ray_dir
    x1, y1 = p1
    x2, y2 = p2

    vx = x2 - x1
    vy = y2 - y1

    denom = dx * vy - dy * vx
    if abs(denom) < 1e-9:
        return None

    t = ((x1 - ox) * vy - (y1 - oy) * vx) / denom
    u = ((x1 - ox) * dy - (y1 - oy) * dx) / denom

    if t > 0.01 and 0.0 <= u <= 1.0:
        return (ox + t * dx, oy + t * dy), t
    return None


class SpiderSilkStrand:
    """A realistic silk strand segment with catenary sag and aerodynamic breeze physics."""

    def __init__(self, p1, p2, strand_type="spiral", sag_factor=0.08, center_ref=None, thickness=1.0):
        self.p1 = np.array(p1, dtype=float)
        self.p2 = np.array(p2, dtype=float)
        self.strand_type = strand_type
        self.sag_factor = sag_factor
        self.thickness = thickness
        self.current_alpha = 0.03  # Initial nearly invisible state (~3% opacity)
        self.target_alpha = 0.03
        self.midpoint = (self.p1 + self.p2) * 0.5
        self.length = float(np.linalg.norm(self.p2 - self.p1))

        # Calculate catenary curve control point
        if center_ref is not None:
            # Sag inward towards center hub + gentle gravitational sag
            inward = center_ref - self.midpoint
            dist = np.linalg.norm(inward)
            if dist > 1e-4:
                inward_u = inward / dist
            else:
                inward_u = np.array([0.0, 1.0])
            sag_vec = (0.85 * inward_u + 0.15 * np.array([0.0, 1.0]))
            sag_vec = sag_vec / np.linalg.norm(sag_vec)
            self.ctrl = self.midpoint + sag_vec * (self.length * sag_factor)
        else:
            # Subtle gravitational sag for structural bridge lines
            self.ctrl = self.midpoint + np.array([0.0, 1.0]) * (self.length * sag_factor)

        # Micro-glue droplet locations for capture silk
        self.droplets = []
        if strand_type == "spiral" and self.length > 14:
            num_droplets = max(1, int(self.length / 16))
            for d_idx in range(1, num_droplets + 1):
                self.droplets.append(d_idx / (num_droplets + 1))

    def get_curve_points(self, breeze_offset=0.0, num_steps=5):
        """Generates curved silk coordinates under tension and breeze flutter."""
        ctrl_flutter = self.ctrl + np.array([breeze_offset, breeze_offset * 0.3])
        pts = []
        for t in np.linspace(0.0, 1.0, num_steps):
            # Quadratic Bézier catenary curve
            pt = (1 - t) ** 2 * self.p1 + 2 * (1 - t) * t * ctrl_flutter + t ** 2 * self.p2
            pts.append((int(pt[0]), int(pt[1])))
        return pts


class SpiderWeb:
    """
    Biological orb spider web constructed across the architectural building corner.
    Features:
    - 14 wall anchor points with piriform silk pads
    - Perimeter bridge frame lines
    - Central hub with tight irregular spirals and free zone
    - 24 radial spokes extending to frame lines
    - 28 turns of catenary capture spiral
    - Proximity-based progressive unveiling & air disturbance physics
    """

    def __init__(self, hub_pos=(440, 380)):
        self.hub = np.array(hub_pos, dtype=float)
        self.strands = []
        self.anchor_points = []
        self.guy_lines = []

        # Air dynamics state
        self.air_energy = 0.0
        self.mouse_prev = np.array([0.0, 0.0])

        self._build_web_structure()

    def _build_web_structure(self):
        """Constructs authentic spider web geometry."""
        # 1. Realistic Anchor Points along Left Wall, Corner Crease, and Right Wall
        anchors_left = [
            (110, 160), (80, 260), (70, 370), (100, 480), (160, 580), (250, 650)
        ]
        anchor_corner_top = (CORNER_X, 110)
        anchor_corner_bot = (CORNER_X, 680)
        anchors_right = [
            (690, 150), (780, 250), (810, 360), (770, 470), (710, 570), (620, 640)
        ]

        self.anchor_points = [anchor_corner_top] + anchors_left + [anchor_corner_bot] + list(reversed(anchors_right))

        # Secondary Guy Lines (Anchoring deeper into concrete walls)
        self.guy_lines = [
            ((110, 160), (50, 120)),
            ((80, 260), (20, 240)),
            ((70, 370), (15, 390)),
            ((100, 480), (40, 520)),
            ((160, 580), (100, 630)),
            ((250, 650), (210, 710)),
            ((CORNER_X, 110), (CORNER_X, 40)),
            ((CORNER_X, 680), (CORNER_X, 735)),
            ((690, 150), (750, 100)),
            ((780, 250), (850, 220)),
            ((810, 360), (890, 350)),
            ((770, 470), (860, 490)),
            ((710, 570), (800, 620)),
            ((620, 640), (700, 705)),
        ]

        # 2. Structural Perimeter Frame Lines (Bridge lines between anchors)
        n_anchors = len(self.anchor_points)
        for i in range(n_anchors):
            p1 = self.anchor_points[i]
            p2 = self.anchor_points[(i + 1) % n_anchors]
            self.strands.append(SpiderSilkStrand(
                p1, p2, strand_type="frame", sag_factor=0.035, center_ref=self.hub, thickness=1.6
            ))

        for p1, p2 in self.guy_lines:
            self.strands.append(SpiderSilkStrand(
                p1, p2, strand_type="guy", sag_factor=0.015, center_ref=None, thickness=1.4
            ))

        # 3. Radial Spokes (24 natural spokes extending outward from hub to perimeter)
        num_spokes = 24
        spoke_ends = []
        random.seed(1337)  # Consistent biological organic web

        for i in range(num_spokes):
            theta = i * 2 * math.pi / num_spokes + random.uniform(-0.04, 0.04)
            dir_x = math.cos(theta)
            dir_y = math.sin(theta)

            # Find ray intersection with outer perimeter frame polygon
            best_pt = None
            min_t = 1e9
            for j in range(n_anchors):
                p1 = self.anchor_points[j]
                p2 = self.anchor_points[(j + 1) % n_anchors]
                res = ray_segment_intersect(self.hub, (dir_x, dir_y), p1, p2)
                if res and res[1] < min_t:
                    min_t = res[1]
                    best_pt = res[0]

            if best_pt:
                spoke_ends.append(best_pt)
                self.strands.append(SpiderSilkStrand(
                    self.hub, best_pt, strand_type="spoke", sag_factor=0.012, center_ref=None, thickness=1.2
                ))

        # 4. Central Hub Spirals (4 tight reinforcing loops + free zone)
        hub_radii = [8, 14, 20, 27]
        for hr in hub_radii:
            for i in range(num_spokes):
                p1_u = (spoke_ends[i] - self.hub) / np.linalg.norm(spoke_ends[i] - self.hub)
                p2_u = (spoke_ends[(i + 1) % num_spokes] - self.hub) / np.linalg.norm(spoke_ends[(i + 1) % num_spokes] - self.hub)
                p1 = self.hub + p1_u * (hr + random.uniform(-1.0, 1.0))
                p2 = self.hub + p2_u * (hr + random.uniform(-1.0, 1.0))
                self.strands.append(SpiderSilkStrand(
                    p1, p2, strand_type="hub", sag_factor=0.03, center_ref=self.hub, thickness=1.1
                ))

        # 5. Capture Spiral (28 viscid turns with natural catenary sagging arcs)
        r_free = 46.0
        num_turns = 28
        for k in range(num_turns):
            frac = (k / float(num_turns)) ** 1.16  # Denser near center, expanding outward

            for i in range(num_spokes):
                # Calculate radial spoke distance
                spoke1_len = float(np.linalg.norm(spoke_ends[i] - self.hub))
                spoke2_len = float(np.linalg.norm(spoke_ends[(i + 1) % num_spokes] - self.hub))

                r1 = r_free + (spoke1_len * 0.91 - r_free) * frac + random.uniform(-1.2, 1.2)
                r2 = r_free + (spoke2_len * 0.91 - r_free) * (frac + 1.0 / (num_turns * num_spokes)) + random.uniform(-1.2, 1.2)

                p1_u = (spoke_ends[i] - self.hub) / spoke1_len
                p2_u = (spoke_ends[(i + 1) % num_spokes] - self.hub) / spoke2_len

                p1 = self.hub + p1_u * r1
                p2 = self.hub + p2_u * r2

                # Catenary inward sag
                self.strands.append(SpiderSilkStrand(
                    p1, p2, strand_type="spiral", sag_factor=0.075, center_ref=self.hub, thickness=0.9
                ))

    def update(self, mouse_pos, enable_wind=True):
        """
        Updates thread opacity and aerodynamic breeze flutter based on mouse proximity and motion.
        """
        m_pos = np.array(mouse_pos, dtype=float)

        # 1. Mouse Velocity & Aerodynamic Impulse
        mouse_vel = np.linalg.norm(m_pos - self.mouse_prev)
        self.mouse_prev = m_pos.copy()

        dist_to_hub = float(np.linalg.norm(m_pos - self.hub))

        # Impart air current disturbance when mouse moves near web
        if dist_to_hub < 400.0:
            impulse = min(7.0, mouse_vel * 0.12) * max(0.0, 1.0 - dist_to_hub / 400.0)
            self.air_energy = min(8.0, self.air_energy + impulse)

        # Air energy natural damping
        self.air_energy *= 0.93

        # 2. Ambient Harmonic Air Draft
        time_s = pygame.time.get_ticks() * 0.001
        if enable_wind:
            ambient_breeze = 0.9 * math.sin(time_s * 1.6) + 0.4 * math.sin(time_s * 3.1)
        else:
            ambient_breeze = 0.0

        total_breeze = ambient_breeze + self.air_energy * math.sin(time_s * 11.5)

        # 3. Global Proximity Opacity Curve
        # Mouse far (>450 px): ~3% opacity (almost invisible)
        # Mouse approaching (150-400 px): gradual smooth appearance
        # Mouse directly over (<70 px): 100% full detail
        if dist_to_hub >= 480.0:
            p_global = 0.03
        elif dist_to_hub <= 60.0:
            p_global = 1.0
        else:
            # Smooth cosine falloff
            t = (dist_to_hub - 60.0) / 420.0
            p_global = 0.03 + 0.97 * ((1.0 + math.cos(t * math.pi)) * 0.5) ** 1.3

        # 4. Update Each Strand's Opacity with Exponential Smoothing (Lerp)
        for strand in self.strands:
            d_local = float(np.linalg.norm(m_pos - strand.midpoint))
            # Local illumination spotlight factor
            if d_local < 220.0:
                f_local = ((220.0 - d_local) / 220.0) ** 2.0
            else:
                f_local = 0.0

            # Target opacity combines global web proximity and local spotlight
            target = min(1.0, max(0.03, p_global * 0.70 + f_local * 0.50))
            # Structural frame lines and spokes appear slightly earlier
            if strand.strand_type in ("frame", "guy"):
                target = min(1.0, target * 1.18)

            strand.target_alpha = target
            # Smooth continuous exponential lerp (~0.4s glide)
            strand.current_alpha += (strand.target_alpha - strand.current_alpha) * 0.08

        return total_breeze, dist_to_hub

    def draw(self, surface, breeze):
        """Renders silk threads with soft cast shadow, charcoal core, and specular glints."""
        # 1. Piriform Attachment Pads (Tiny silk discs bonding into concrete pores)
        for ax, ay in self.anchor_points:
            # Subtle anchor shadow
            pygame.draw.circle(surface, (160, 166, 175, 120), (ax + 2, ay + 2), 4)
            pygame.draw.circle(surface, (90, 95, 105, 180), (ax, ay), 3)
            pygame.draw.circle(surface, (50, 54, 62, 220), (ax, ay), 2)

        # 2. Render Silk Strands
        time_s = pygame.time.get_ticks() * 0.001

        for strand in self.strands:
            alpha = strand.current_alpha
            if alpha < 0.015:
                continue

            # Calculate thread deflection under breeze
            # High-tension bridge lines deflect less, fine capture spirals flutter freely
            flexibility = 1.0 if strand.strand_type == "spiral" else 0.4 if strand.strand_type == "spoke" else 0.2
            flutter = breeze * flexibility * math.sin(time_s * 2.0 + strand.midpoint[1] * 0.02)
            pts = strand.get_curve_points(breeze_offset=flutter, num_steps=5)

            # A. Subtle Ambient Cast Shadow on Concrete Wall (+3px X, +5px Y)
            shadow_alpha = int(35 * alpha)
            if shadow_alpha > 2:
                shadow_pts = [(x + 3, y + 5) for x, y in pts]
                pygame.draw.lines(surface, (*COLOR_SILK_SHADOW, shadow_alpha), False, shadow_pts, 1)

            # B. Core Silk Thread
            core_alpha = int(230 * alpha)
            if strand.strand_type in ("frame", "guy"):
                core_alpha = int(250 * alpha)
            pygame.draw.lines(surface, (*COLOR_SILK_CORE, core_alpha), False, pts, int(strand.thickness))

            # C. Specular Silk Glint / Fiber Highlight
            glint_alpha = int(95 * alpha)
            if glint_alpha > 5:
                glint_pts = [(x, y - 1) for x, y in pts]
                pygame.draw.lines(surface, (*COLOR_SILK_HILITE, glint_alpha), False, glint_pts, 1)

            # D. Viscid Glue Droplets along Spiral Silk
            if strand.droplets and alpha > 0.35:
                for frac in strand.droplets:
                    t = frac
                    ctrl_flutter = strand.ctrl + np.array([flutter, flutter * 0.3])
                    d_pos = (1 - t) ** 2 * strand.p1 + 2 * (1 - t) * t * ctrl_flutter + t ** 2 * strand.p2
                    dx, dy = int(d_pos[0]), int(d_pos[1])
                    pygame.draw.circle(surface, (*COLOR_SILK_CORE, int(180 * alpha)), (dx, dy), 1)
                    pygame.draw.circle(surface, (255, 255, 255, int(140 * alpha)), (dx, dy - 1), 1)


def main():
    # 2. Setup Pygame
    pygame.init()
    pygame.display.set_caption("🕸️ Day 14: Interactive Spider Web on a Building Corner | 30 Days Python")

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Pre-render architectural background
    background = create_architectural_background(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Initialize Spider Web
    web = SpiderWeb(hub_pos=(440, 380))

    # Silk rendering layer (SRCALPHA for smooth opacity compositing)
    silk_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)

    # HUD Font
    try:
        font_hud = pygame.font.SysFont("couriernew", 13, bold=True)
    except Exception:
        font_hud = pygame.font.Font(None, 14)

    running = True
    fullscreen = False
    enable_wind = True

    # Initial mouse state (center of screen, far from corner)
    mouse_pos = (CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

    while running:
        clock.tick(FPS)

        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Trigger air breeze impulse
                    web.air_energy = 8.0
                elif event.key == pygame.K_w:
                    enable_wind = not enable_wind
                elif event.key == pygame.K_s:
                    snap_name = "spider_web_corner.png"
                    pygame.image.save(screen, snap_name)
                    print(f"Saved screenshot: {snap_name}")
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

        # -------------------------------------------------------------
        # DYNAMIC PHYSICS & PROXIMITY UPDATE
        # -------------------------------------------------------------
        breeze, dist_to_hub = web.update(mouse_pos, enable_wind=enable_wind)

        # -------------------------------------------------------------
        # RENDER SCENE
        # -------------------------------------------------------------
        # 1. Blit Architectural Background
        screen.blit(background, (0, 0))

        # 2. Render Spider Silk Layer
        silk_layer.fill((0, 0, 0, 0))
        web.draw(silk_layer, breeze)
        screen.blit(silk_layer, (0, 0))

        # 3. Minimalist Architectural HUD
        hud_bg = pygame.Surface((CANVAS_WIDTH, 26), pygame.SRCALPHA)
        hud_bg.fill((246, 248, 252, 190))
        screen.blit(hud_bg, (0, CANVAS_HEIGHT - 26))

        # Calculate web reveal percentage
        proximity_pct = int(max(0.0, min(1.0, 1.0 - (dist_to_hub - 60.0) / 420.0)) * 100)
        wind_status = "ON" if enable_wind else "OFF"
        status_text = (
            f"🕸️ SPIDER WEB | Corner Proximity: {proximity_pct}% | "
            f"Breeze: {wind_status} (Impulse: {web.air_energy:.1f})"
        )
        rendered_status = font_hud.render(status_text, True, (45, 50, 58))
        screen.blit(rendered_status, (14, CANVAS_HEIGHT - 19))

        controls_text = "Hover Mouse: Reveal | [SPACE] Breeze Gust | [W] Wind Toggle | [S] Snap | [ESC] Exit"
        rendered_ctrl = font_hud.render(controls_text, True, (95, 102, 115))
        screen.blit(rendered_ctrl, (CANVAS_WIDTH - rendered_ctrl.get_width() - 14, CANVAS_HEIGHT - 19))

        # Subtle bottom progress bar indicating proximity reveal
        bar_w = int(CANVAS_WIDTH * (proximity_pct / 100.0))
        if bar_w > 0:
            pygame.draw.rect(screen, (85, 95, 110), (0, CANVAS_HEIGHT - 2, bar_w, 2))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
