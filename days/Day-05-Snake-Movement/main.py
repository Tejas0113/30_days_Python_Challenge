import sys
import pygame

# Initialize Pygame
pygame.init()

# Set up the window size
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reptile Cursor Animation - Python")
clock = pygame.time.Clock()

# Tail parameters: stores past coordinates to create the smooth trailing spine
trail_length = 35
trail = [[WIDTH // 2, HEIGHT // 2] for _ in range(trail_length)]

# Click ripples list
ripples = []


class Ripple:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.radius = 5
    self.alpha = 255

  def update(self):
    self.radius += 3
    self.alpha -= 8

  def draw(self, surface):
    if self.alpha > 0:
      # Transparent surface for the expanding ripple ring effect
      surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
      pygame.draw.circle(
          surf, (0, 255, 180, max(0, self.alpha)), (self.x, self.y), self.radius, 2
      )
      surface.blit(surf, (0, 0))


# Main loop
while True:
  screen.fill((10, 10, 15))  # Dark webpage-like background canvas

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:  # Left click triggers a ripple effect
        mx, my = pygame.mouse.get_pos()
        ripples.append(Ripple(mx, my))

  # Get current mouse position
  target_x, target_y = pygame.mouse.get_pos()

  # Smooth spring interpolation for the head segment leading the tail
  head = trail[0]
  head[0] += (target_x - head[0]) * 0.4
  head[1] += (target_y - head[1]) * 0.4

  # Propagate physics down the spine / tail segments
  for i in range(1, len(trail)):
    prev_segment = trail[i - 1]
    curr_segment = trail[i]
    curr_segment[0] += (prev_segment[0] - curr_segment[0]) * 0.5
    curr_segment[1] += (prev_segment[1] - curr_segment[1]) * 0.5

  # Update and draw click ripples
  for ripple in ripples[:]:
    ripple.update()
    ripple.draw(screen)
    if ripple.alpha <= 0:
      ripples.remove(ripple)

  # Draw the reptile spine/tail (tapering down from head to tip)
  for i in range(len(trail) - 1, 0, -1):
    radius = int(max(2, 14 * (1 - i / trail_length)))
    color = (0, int(220 * (1 - i / trail_length)), int(255 * (1 - i / trail_length)))
    pygame.draw.circle(screen, color, (int(trail[i][0]), int(trail[i][1])), radius)

  # Draw the leading head cursor
  pygame.draw.circle(screen, (0, 255, 200), (int(head[0]), int(head[1])), 8)

  pygame.display.flip()
  clock.tick(60)