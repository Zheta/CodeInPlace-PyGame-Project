# Import other modules
from zelda_utilities.constants import *


# Helps establish the current frame for sprite animation/image changing
class Animation:
    def __init__(self):
        # Animation clock
        self.next_frame = pygame.time.get_ticks()

        # Starting frame
        self.frame = 0

        # ~12 frames/sec (1000ms // 12)
        self.frame_time = 1000 // ANIMATION_RATE

    def anim_sprite(self):
        if pygame.time.get_ticks() > self.next_frame:
            self.frame = (self.frame + 1) % (24 * ANIMATION_RATE)  # reset > 20 sec
            self.next_frame += self.frame_time
        return self.frame

