# Import local files
from zelda_sprites.beeper import Beeper
from zelda_utilities.collision import *
from zelda_utilities.constants import *

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, file_name='assets/image/spritesheet/zelda/zelda_character.png', frames=59):
        # initialize parent class
        super().__init__()
        # Set game class
        self.game = game

        # ~Sprite Groups
        self.game.all_sprites.add(self)
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
        # create sprite list to hold all the frames
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
        self.hit_rect = pygame.Rect(0, 0, 13, 13)

        # ~Movement
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

        self.hit_rect.center = self.pos
        self.rect.center = (self.hit_rect.centerx, self.hit_rect.centery)

        # ~Actions
        self.last_beeper = 0

        # ~Animations
        # Walking
        self.move_frames = 8

        # Idle
        self.idle_rate = 36
        # TODO: can randomize blink rate, was working before removal (1)
        # self.blink_roll = pygame.time.get_ticks()
        # self.blink_frame = 16

        # Beeper
        self.placed_beeper = 0
        self.stop_move = 0

        # Health
        self.health = PLAYER_HEALTH

    # Need this function name for updates to play nice with pygame sprite groups!!
    # add additional update functions *here*
    def update(self):
        self.update_loc()
        self.update_actions()
        self.update_anim()

    # Move the sprite based on key presses
    def update_loc(self):
        if self.stop_move >= 1:
            self.vel = vec(0, 0)
            self.stop_move = (self.stop_move + 1) % 10
        else:
            self.vel = self.game.control.vector
        # Move Zelda sprite by directional vector
        self.pos += self.vel
        # Test for collision
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        # Move sprite to match bounding box
        self.rect.center = (self.hit_rect.centerx + 1, self.hit_rect.centery - 6)

    def update_actions(self):
        if self.game.control.kb_button_a == 1 or self.game.control.joy_button_a == 1:
            now = pygame.time.get_ticks()
            if now - self.last_beeper > BEEPER_RATE:
                self.last_beeper = now
                temp_pos_x = (self.hit_rect.centerx - (self.hit_rect.centerx % 8)) + 4
                temp_pos_y = (self.hit_rect.centery - (self.hit_rect.centery % 8)) + 4
                offset_pos = vec(temp_pos_x, temp_pos_y)
                # Place beeper!
                Beeper(self.game, offset_pos)
                # Play placement animation
                self.stop_move = 1
                self.placed_beeper = 1
        if self.game.control.kb_button_b == 1 or self.game.control.joy_button_b == 1:
            pass

    def update_anim(self):
        frame = self.game.anim_clock.anim_sprite()
        facing = self.game.control.facing
        if self.placed_beeper >= 1:
            if facing == 'up':
                self.change_image(57)
            elif facing == 'down':
                self.change_image(58)
            elif facing == 'left':
                self.change_image(55)
            elif facing == 'right':
                self.change_image(56)
            self.placed_beeper = (self.placed_beeper + 1) % 6
        else:
            if self.vel != vec(0, 0):
                # 8-frame walk cycles
                mod_move_frame = frame % self.move_frames
                # Play Zelda walk animations
                if facing == 'up':
                    self.change_image(30 + mod_move_frame)
                elif facing == 'down':
                    self.change_image(2 + mod_move_frame)
                elif facing == 'left':
                    self.change_image(12 + mod_move_frame)
                elif facing == 'right':
                    self.change_image(22 + mod_move_frame)
            else:
                # TODO: can randomize blink rate, was working before removal (2)
                # # Get a random number for the blink frame
                # if pygame.time.get_ticks() > self.blink_roll:
                #     self.blink_frame = random.randint(14, 20)
                #     self.blink_roll += 10000

                # Blink rate (3-sec blinking to mimic humans)
                mod_idle_frame = frame % self.idle_rate
                # Play Zelda idle animations
                if facing == 'up':
                    self.change_image(30)
                elif facing == 'down':
                    if mod_idle_frame == 15:  # self.blink_frame
                        self.change_image(1)
                    else:
                        self.change_image(0)
                elif facing == 'left':
                    if mod_idle_frame == 15:
                        self.change_image(11)
                    else:
                        self.change_image(10)
                elif facing == 'right':
                    if mod_idle_frame == 15:
                        self.change_image(21)
                    else:
                        self.change_image(20)

    def change_image(self, index):
        # load the new frame
        self.image = self.images[index]
        # get a per-pixel mask
        self.mask = pygame.mask.from_surface(self.image)
