# Import other modules
import pygame
import pytmx

# Import local files
from zelda_utilities.constants import *


# Loads Tiled Map Editor maps!
# Almost verbatim from:
#  Chris Bradfield - KidsCanCode
#  Tile-based game Part 12: Loading Tiled Maps
#  https://www.youtube.com/watch?v=QIXyj3WeyZM
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


# Bounding boxes for collisions
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        # initialize parent class
        super().__init__()
        # Set game class
        self.game = game

        # ~Sprite Groups
        self.game.walls.add(self)

        # Dimensions
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


# Top transparent layer
class BGObjects(pygame.sprite.Sprite):
    def __init__(self, game,  x, y, file_name='assets/image/background/castle_garden_tiled_objects.png'):
        # initialize parent class
        super().__init__()
        # Set game class
        self.game = game

        # ~Sprite Groups
        self.game.all_sprites.add(self)

        # self.image = pygame.image.load(~file~).convert_alpha()
        self.image = pygame.image.load(file_name).convert_alpha()
        # Create rect, and take arguments for starting position
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

        self.x = x
        self.y = y
        # Set x and y
        self.rect.x = x
        self.rect.y = y
