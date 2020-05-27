# Import standard
import random

# Import local files
from zelda_utilities.collision import *
from zelda_utilities.constants import *


class Karel(pygame.sprite.Sprite):
    def __init__(self, game, x, y, file_name, frames=53):
        # initialize parent class
        super().__init__()
        # Set game class
        self.game = game

        # ~Sprite Groups
        self.game.all_sprites.add(self)
        self.game.mobs.add(self)
        self.game.anim_spr.add(self)

        # Load sprite-sheet from image file
        # Adapted/modified from:
        #  Steve Paget/Pygame_Functions
        #  https://github.com/StevePaget/Pygame_Functions/blob/master/pygame_functions.py
        #  newSprite() class
        full_image = pygame.image.load(file_name).convert_alpha()
        # define variables for surface creator
        self.original_width = full_image.get_width() // frames
        self.original_height = full_image.get_height()
        # create sprite list to hold all the frames
        self.images = []
        # Start at beginning
        list_x = 0
        # Generate sprite from sheet
        for frame_num in range(frames):
            frame_surf = pygame.Surface((self.original_width, self.original_height), pygame.SRCALPHA, 32)
            frame_surf.blit(full_image, (list_x, 0))
            self.images.append(frame_surf.copy())
            list_x -= self.original_width
        # get frame 0 of sprite and create new surface
        self.image = pygame.Surface.copy(self.images[0])
        # get a per-pixel mask
        self.mask = pygame.mask.from_surface(self.image)
        # get pygame rect for movement and initial bounding box
        self.rect = self.image.get_rect()
        # Create movement bounding-box for positioning sprite and wall collisions, (x, y) is start position
        self.hit_rect = pygame.Rect(0, 0, 11, 11)

        # ~Movement
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

        self.hit_rect.center = self.pos
        self.rect.center = (self.hit_rect.centerx, self.hit_rect.centery)

        # ~Animations
        # Walking
        self.move_frames = 8
        self.facing = 'right'
        # Idle
        self.idle_rate = 12
        self.idle_facing = 1
        self.roll_idle = 0

        # Health
        self.health = KAREL_HEALTH

        # Start Karel as inactive and out of range to wait for player, play idle animation
        self.is_active = False
        self.last_active = 0
        self.out_of_range = 0

    # Need this function name for updates to play nice with pygame sprite groups!!
    # add additional update functions *here*
    def update(self):
        self.update_loc()
        # self.update_actions()
        if not self.health <= 0:
            self.update_anim()

    # Move the sprite based on key presses
    def update_loc(self):
        if self.health <= 0:
            # If Karel's beeper bag is full, disable movement, collision, etc. and just hold on sit frame
            self.game.mobs.remove(self)
            self.vel = vec(0, 0)
            self.rect.center = (self.hit_rect.centerx, self.hit_rect.centery)
            self.change_image(52)
            if not self.game.mobs.sprites():
                self.game.running = False
        else:
            # If still looking for beepers
            if self.is_active:
                # Math stuff to get the angle to the player and move at a normalized speed to the game
                self.vel = vec(self.game.player.hit_rect.centerx - self.hit_rect.centerx,
                               self.game.player.hit_rect.centery - self.hit_rect.centery)
                self.vel.normalize_ip()
                # Set speed multiplier here
                self.vel *= 0.5
                if self.vel.x < 0.1:
                    self.facing = 'left'
                else:
                    self.facing = 'right'
                self.pos += self.vel

                # Collisions
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.game.walls, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.game.walls, 'y')

                # Move sprite image rect to match bounding box
                self.rect.center = (self.hit_rect.centerx, self.hit_rect.centery)

                # If player moves too far away, deactivate
                if self.pos.distance_to(self.game.player.pos) >= 80:
                    self.out_of_range += 1
                    # Waits about 4 seconds (60 * 4) to deactivate
                    if self.out_of_range >= 240:
                        self.out_of_range = 0
                        self.is_active = False
                else:
                    self.out_of_range = 0

            else:
                # If not active
                # Set velocity to 0
                self.vel = vec(0, 0)
                # Make sure image rect is centered on hit-box
                self.rect.center = (self.hit_rect.centerx, self.hit_rect.centery)
                # Activation function
                # Makes Karel wait to move until Player is close
                now = pygame.time.get_ticks()
                # Check every second or so
                if now - self.last_active > 1000:
                    self.last_active = now
                    if self.pos.distance_to(self.game.player.pos) <= 70:
                        self.is_active = True

    def update_anim(self):
        frame = self.game.anim_clock.anim_sprite()
        # Movement animations
        if self.vel != vec(0, 0):
            mod_move_frame = frame % self.move_frames
            if self.health == 3:
                # Left
                if self.facing == 'left':
                    self.change_image(28 + mod_move_frame)
                # Right
                else:
                    self.change_image(2 + mod_move_frame)
            elif self.health == 2:
                # Left
                if self.facing == 'left':
                    self.change_image(36 + mod_move_frame)
                # Right
                else:
                    self.change_image(10 + mod_move_frame)
            else:
                # Left
                if self.vel.x < 0.1:
                    self.change_image(44 + mod_move_frame)
                # Right
                else:
                    self.change_image(18 + mod_move_frame)
        else:
            # Idle animations
            mod_idle_frame = frame % self.idle_rate  # TODO
            now = pygame.time.get_ticks()
            if now - self.roll_idle > 3000:
                self.roll_idle = now
                self.idle_facing = random.randint(0, 1)
            # Left
            if self.idle_facing == 0:
                if mod_idle_frame >= 7:
                    self.change_image(27)
                else:
                    self.change_image(26)
            # Right
            else:
                if mod_idle_frame >= 7:
                    self.change_image(1)
                else:
                    self.change_image(0)

    def change_image(self, index):
        # load the new frame
        self.image = self.images[index]
        # get a per-pixel mask
        self.mask = pygame.mask.from_surface(self.image)
