# Import local files
from zelda_utilities.constants import *


# Camera class to follow player
# Almost verbatim from:
#  Chris Bradfield - KidsCanCode
#  Tile-based game Part 4: Scrolling Map / Camera
#  https://www.youtube.com/watch?v=3zV2ewk-IGU
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.centerx + ART_SCALE_X // 2
        y = -target.centery + ART_SCALE_Y // 2

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - ART_SCALE_X), x)  # right
        y = max(-(self.height - ART_SCALE_Y), y)  # bottom
        # Update camera
        self.camera = pygame.Rect(x, y, self.width, self.height)
