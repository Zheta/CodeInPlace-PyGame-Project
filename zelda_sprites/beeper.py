# Import local files
from zelda_utilities.constants import *
vec = pygame.math.Vector2


class Beeper(pygame.sprite.Sprite):
    def __init__(self, game, pos, file_name, frames=1):
        # initialize parent class
        super().__init__()
        # Set game class
        self.game = game

        # ~Sprite Groups
        self.game.all_sprites.add(self)
        self.game.beepers.add(self)
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
        self.hit_rect = self.rect

        # ~Movement
        self.pos = pos
        self.rect.center = pos

    # Need this function *name* for updates to play nice with pygame sprite groups!!
    # add additional update functions *here*
    def update(self):
        pass

    def update_loc(self):
        pass
