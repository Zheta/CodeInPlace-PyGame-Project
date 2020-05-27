# Import local files
from zelda_utilities.constants import *
from pygame.sprite import Sprite


# TODO: sort player, mob, and beeper render order based on relative y-axis position
# REALLY wanted to get this done prior to submission
#
# I could get it to work with individual sprites in tests but not with sprite groups
#  at the time I was working on it, didn't know enough about PyGame sprite groups, classes and callback functions
#  could PROBABLY get it wot work now, but want to move on to Godot or something else than PyGame
#  leaving it in for now
#
# starter code from:
#  sloth
#  https://stackoverflow.com/questions/55233448/pygame-overlapping-sprites-draw-order-based-on-location

class YSortedGroup(pygame.sprite.Group):
    def y_draw(self, surface):
        sprites = self.sprites()
        for sprite in sorted(sprites, key=lambda sprite: sprite.rect.bottom):
            self.spritedict[sprite] = surface.blit(sprite.image, sprite.rect)
