# Import standard
import random

# Import other modules
import pygame

# Import local files
from pygame.sprite import Group

from animation import Animation
from camera import Camera
from control import Control

from zelda_sprites.background import *
from zelda_sprites.mobs import Karel
from zelda_sprites.player import Player
from zelda_utilities.collision import *
from zelda_utilities.constants import *
# from zelda_sprites.y_sorted_group import YSortedGroup  #TODO: see file

# Center window on monitor
os.environ['SDL_VIDEO_CENTERED'] = '1'


# ~HUD functions
# Health bar
# TODO: use images or counter to represent health?
def draw_player_health(surf, x, y, pct):
    bar_length = 40
    bar_height = 10
    if pct < 0:
        pct = 0
    fill = pct * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 1)


# Game Class
class Game:
    all_sprites: Group

    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Initialize game-pad / joystick[0]
        self.control = Control(self)
        # Create variable to satisfy game loop
        self.running = True

        # Set window title and icon
        pygame.display.set_caption('Zorlda')
        self.icon = pygame.image.load('assets/icon/zelda_icon.png')
        pygame.display.set_icon(self.icon)

        # Set display size to match assets, create display, and scale
        self.screen = pygame.display.set_mode((ART_SCALE_X, ART_SCALE_Y), SCALED)

        # ~Levels/Maps
        # Load the map!
        self.map = TiledMap('assets/maps/castle_garden_tiled.tmx')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # ~Sprite Groups~
        # ALL sprites # group with all sprites for camera updates
        self.all_sprites = pygame.sprite.Group()
        # Walls group
        self.walls = pygame.sprite.Group()
        # Mobs group
        self.mobs = pygame.sprite.Group()
        # Animated sprites group
        self.anim_spr = pygame.sprite.Group()
        # EXPERIMENTAL Set up active sprite group, which sorts layering by Y axis value
        # self.sprite_draw_group = YSortedGroup()
        # Beeper group
        self.beepers = pygame.sprite.Group()

        # Load map from Tiled file
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'karel':
                # place Karels
                Karel(self, tile_object.x, tile_object.y)
            if tile_object.name == 'player':
                # Place Player
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                # place wall, etc. bounding boxes
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        # -Background objects - transparent layer on top of other sprites bushes, fountains, etc.
        self.bg_objects = BGObjects(self, 0, 0)

        # ~Clocks
        # Pygame clock
        self.clock = pygame.time.Clock()
        # # Delta time for movement
        # self.dt = 0
        # Animation clock
        self.anim_clock = Animation()

        # ~Camera
        # IT'S MAGIC
        self.camera = Camera(self.map.width, self.map.height)

        # Testing
        self.show_fps = False
        self.draw_debug = False

    def input_processing(self):
        self.control.get_input()

    def update(self):
        # Update ALL SPRITES
        # Sprite groups can ONLY call the update function and then use the functions *in there* XD
        self.all_sprites.update()

        # a Karel hits the Player(!)
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collided=collide_hit_rect)
        for hit in hits:
            self.player.health -= 1
            # hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.running = False
        if hits:
            # KNOCK-BACK
            # TODO: make this more responsive
            #  ...camera moves too much to be comfortable at high velocities
            #  solution might be to stop the mob and player's movement for a sec, freeze mob longer than player
            self.player.pos += hit.vel * 8
            hit.pos = hit.pos - (hit.vel * 12)

        # a Karel hits a beeper
        hits = pygame.sprite.groupcollide(self.mobs, self.beepers, False, True)
        for hit in hits:
            hit.health -= 1

        # Update camera
        self.camera.update(self.player.hit_rect)

    def render(self):
        # Render Map layers
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        # Render all sprites!!
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)

        # Testing functions
        # Show FPS in window title
        if self.show_fps:
            pygame.display.set_caption('Zorlda - FPS:{:.2f}'.format(self.clock.get_fps()))
        else:
            pygame.display.set_caption('Zorlda')
        # Show bounding boxes
        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

        # Update display
        pygame.display.update()

    def run(self):
        while self.running:
            self.input_processing()
            self.update()
            self.render()
            # Frame-rate (essentially divides 1000 milliseconds(via PyGame clock) by FRAME_RATE)
            self.clock.tick(FRAME_RATE)


# Game Loop!
Game().run()
