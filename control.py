# Import local files
from zelda_utilities.constants import *

vec = pygame.math.Vector2


# Collect all the player inputs needed and does some of the processing
# Created mostly from scratch from PyGame documentation
# Had to build this just right so that the player moves in a Zelda-like way
class Control:
    def __init__(self, game):
        self.game = game

        # Check for joysticks/game-pads
        self.joy_amount = pygame.joystick.get_count()
        if self.joy_amount > 0:
            # Initialize game-pad/joystick, uses the index in zelda_utilities/constants
            # TODO: certainly if the game ever had a pause menu or options screen,
            #   being able to choose the joystick index there would be nice
            self.joy = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            self.joy[JOY_INDEX].init()

        # Player movement variables

        # ~Keyboard~
        # Directional list for multi-key fix (EVERY direction accounted for)
        # Also for zelda-style facing fix (take first key pressed for facing)
        self.kb_direction_list = []
        # Current control vector
        self.kb_vector = (0, 0)
        # Storing button input, abstraction
        self.kb_button_a = 0
        self.kb_button_b = 0

        # ~Joystick~
        # Storing d-pad input
        self.joy_hat_input = 0
        # Testing if d-pad was accessed on frame
        self.joy_hat_active = False
        # Current d-pad control vector
        self.joy_hat_vector = (0, 0)
        # Zelda-style facing fix (store previous update for facing)
        self.joy_hat_vect_prev = (0, 0)

        # Storing analog input
        self.joy_lf_analog_y = 0
        self.joy_lf_analog_x = 0
        # Testing if analog-stick was accessed on frame
        self.joy_lf_analog_active = False
        # Current analog control vector
        self.joy_lf_analog_vector = (0, 0)
        # Zelda-style facing fix (store previous update for facing)
        self.joy_lf_analog_vect_prev = (0, 0)

        # Storing button input
        self.joy_button_a = 0
        self.joy_button_b = 0

        # Initial sprite vector
        self.vector = vec(0, 0)
        # Initial sprite facing (setting specific instead of None starts idle animation!)
        self.facing = 'down'

        self.draw_debug = True

    def get_input(self):
        # Process all pygame events
        for event in pygame.event.get():
            # Stop game on window close
            if event.type == QUIT:
                self.game.running = False
                break
            # Keyboard control events
            elif event.type == KEYDOWN:
                # Stop game on ESC key
                if event.key == K_ESCAPE:
                    self.game.running = False
                    break
                # KB directional controls pressed
                # Add direction to list while keeping list at 2, allows rollover adjustment, KEEP AS 'str' FOR FACING
                elif event.key == P1_KB_UP:
                    self.kb_direction_list.append('up')
                elif event.key == P1_KB_DOWN:
                    self.kb_direction_list.append('down')
                elif event.key == P1_KB_LEFT:
                    self.kb_direction_list.append('left')
                elif event.key == P1_KB_RIGHT:
                    self.kb_direction_list.append('right')
                elif event.key == P1_KB_BUTTON1:
                    self.kb_button_a = 1
                elif event.key == P1_KB_BUTTON2:
                    self.kb_button_b = 1
            elif event.type == KEYUP:
                # KB directional controls released
                # Remove direction from list, KEEP AS 'str' FOR FACING
                if event.key == P1_KB_UP:
                    if 'up' in self.kb_direction_list:
                        self.kb_direction_list.remove('up')
                elif event.key == P1_KB_DOWN:
                    if 'down' in self.kb_direction_list:
                        self.kb_direction_list.remove('down')
                elif event.key == P1_KB_LEFT:
                    if 'left' in self.kb_direction_list:
                        self.kb_direction_list.remove('left')
                elif event.key == P1_KB_RIGHT:
                    if 'right' in self.kb_direction_list:
                        self.kb_direction_list.remove('right')
                elif event.key == P1_KB_BUTTON1:
                    self.kb_button_a = 0
                elif event.key == P1_KB_BUTTON2:
                    self.kb_button_b = 0
                elif event.key == P1_SHOW_FPS:
                    self.game.show_fps = not self.game.show_fps
                elif event.key == P1_SHOW_BOUNDING_BOXES:
                    self.game.draw_debug = not self.game.draw_debug

            # Joystick control events
            # Joystick d-pad
            elif event.type == JOYHATMOTION:
                # get value of joystick hat switch (d-pad)
                self.joy_hat_input = self.joy[JOY_INDEX].get_hat(0)
                # print(str(joy_hat))  # for testing!
                self.joy_hat_active = True
            # Joystick left-analog
            elif event.type == JOYAXISMOTION:
                # get values of joystick left analog stick
                self.joy_lf_analog_x = self.joy[JOY_INDEX].get_axis(0)
                self.joy_lf_analog_y = self.joy[JOY_INDEX].get_axis(1)
                # print('x: ' + str(self.joy_lf_analog_x))  # for testing!
                # print('y: ' + str(self.joy_lf_analog_y))  # for testing!
                self.joy_lf_analog_active = True
            elif event.type == pygame.JOYBUTTONDOWN:
                self.joy_button_a = self.joy[JOY_INDEX].get_button(0)
                self.joy_button_b = self.joy[JOY_INDEX].get_button(1)
            elif event.type == pygame.JOYBUTTONUP:
                self.joy_button_a = self.joy[JOY_INDEX].get_button(0)
                self.joy_button_b = self.joy[JOY_INDEX].get_button(1)

        # player d-pad active
        if self.joy_hat_active:
            self.joy_hat()
            self.vector = vec(self.joy_hat_vector)
        # Player left analog active
        elif self.joy_lf_analog_active:
            self.joy_lf_analog()
            self.vector = vec(self.joy_lf_analog_vector)
        # Player KB active?
        else:
            self.keyboard_direction()
            self.vector = vec(self.kb_vector)

    def joy_hat(self):
        # Centered
        if self.joy_hat_input == (0, 0):
            self.joy_hat_vector = D_STOP
            self.joy_hat_active = False
        # Cardinals
        elif self.joy_hat_input == (0, 1):
            self.joy_hat_vector = D_UP
            self.facing = 'up'
        elif self.joy_hat_input == (0, -1):
            self.joy_hat_vector = D_DOWN
            self.facing = 'down'
        elif self.joy_hat_input == (-1, 0):
            self.joy_hat_vector = D_LEFT
            self.facing = 'left'
        elif self.joy_hat_input == (1, 0):
            self.joy_hat_vector = D_RIGHT
            self.facing = 'right'
        # Ordinals
        elif self.joy_hat_input == (-1, 1):
            self.joy_hat_vector = D_UP_LEFT
            if self.joy_hat_vect_prev == D_LEFT:
                self.facing = 'left'
            else:
                self.facing = 'up'
        elif self.joy_hat_input == (1, 1):
            self.joy_hat_vector = D_UP_RIGHT
            if self.joy_hat_vect_prev == D_RIGHT:
                self.facing = 'right'
            else:
                self.facing = 'up'
        elif self.joy_hat_input == (-1, -1):
            self.joy_hat_vector = D_DOWN_LEFT
            if self.joy_hat_vect_prev == D_LEFT:
                self.facing = 'left'
            else:
                self.facing = 'down'
        elif self.joy_hat_input == (1, -1):
            self.joy_hat_vector = D_DOWN_RIGHT
            if self.joy_hat_vect_prev == D_RIGHT:
                self.facing = 'right'
            else:
                self.facing = 'down'
        # Store previous d-pad vector for facing
        self.joy_hat_vect_prev = self.joy_hat_vector

    def joy_lf_analog(self):
        # Centered
        if (-0.4 < self.joy_lf_analog_x < 0.4) and (-0.4 < self.joy_lf_analog_y < 0.4):
            self.joy_lf_analog_vector = D_STOP
            self.joy_lf_analog_active = False
        # Cardinals
        elif self.joy_lf_analog_y <= -0.4 and (-0.4 < self.joy_lf_analog_x < 0.4):
            self.joy_lf_analog_vector = D_UP
            self.facing = 'up'
            # Store previous analog vector for facing
            self.joy_lf_analog_vect_prev = self.joy_lf_analog_vector
        elif self.joy_lf_analog_y >= 0.4 and (-0.4 < self.joy_lf_analog_x < 0.4):
            self.joy_lf_analog_vector = D_DOWN
            self.facing = 'down'
            # Store previous analog vector for facing
            self.joy_lf_analog_vect_prev = self.joy_lf_analog_vector
        elif self.joy_lf_analog_x <= -0.4 and (-0.4 < self.joy_lf_analog_y < 0.4):
            self.joy_lf_analog_vector = D_LEFT
            self.facing = 'left'
            # Store previous analog vector for facing
            self.joy_lf_analog_vect_prev = self.joy_lf_analog_vector
        elif self.joy_lf_analog_x >= 0.4 and (-0.4 < self.joy_lf_analog_y < 0.4):
            self.joy_lf_analog_vector = D_RIGHT
            self.facing = 'right'
            # Store previous analog vector for facing
            self.joy_lf_analog_vect_prev = self.joy_lf_analog_vector
        # ordinals
        elif self.joy_lf_analog_y <= -0.4 and self.joy_lf_analog_x <= -0.4:
            self.joy_lf_analog_vector = D_UP_LEFT
            if self.joy_lf_analog_vect_prev == D_LEFT:
                self.facing = 'left'
            else:
                self.facing = 'up'
        elif self.joy_lf_analog_y <= -0.4 and self.joy_lf_analog_x >= 0.4:
            self.joy_lf_analog_vector = D_UP_RIGHT
            if self.joy_lf_analog_vect_prev == D_RIGHT:
                self.facing = 'right'
            else:
                self.facing = 'up'
        elif self.joy_lf_analog_y >= 0.4 and self.joy_lf_analog_x <= -0.4:
            self.joy_lf_analog_vector = D_DOWN_LEFT
            if self.joy_lf_analog_vect_prev == D_LEFT:
                self.facing = 'left'
            else:
                self.facing = 'down'
        elif self.joy_lf_analog_y >= 0.4 and self.joy_lf_analog_x >= 0.4:
            self.joy_lf_analog_vector = D_DOWN_RIGHT
            if self.joy_lf_analog_vect_prev == D_RIGHT:
                self.facing = 'right'
            else:
                self.facing = 'down'

    def keyboard_direction(self):
        # If keyboard has a direction list
        if self.kb_direction_list:
            # set facing
            # based on earliest input still in the list
            self.facing = self.kb_direction_list[0]
            # cardinals
            if len(self.kb_direction_list) == 1:
                if self.kb_direction_list[0] == 'up':
                    self.kb_vector = D_UP
                elif self.kb_direction_list[0] == 'down':
                    self.kb_vector = D_DOWN
                elif self.kb_direction_list[0] == 'left':
                    self.kb_vector = D_LEFT
                elif self.kb_direction_list[0] == 'right':
                    self.kb_vector = D_RIGHT
            # 2-key ordinals + L/R / U/D fix
            elif len(self.kb_direction_list) == 2:
                if ('up' in self.kb_direction_list) and ('left' in self.kb_direction_list):
                    self.kb_vector = D_UP_LEFT
                elif ('up' in self.kb_direction_list) and ('right' in self.kb_direction_list):
                    self.kb_vector = D_UP_RIGHT
                elif ('down' in self.kb_direction_list) and ('left' in self.kb_direction_list):
                    self.kb_vector = D_DOWN_LEFT
                elif ('down' in self.kb_direction_list) and ('right' in self.kb_direction_list):
                    self.kb_vector = D_DOWN_RIGHT
                else:
                    self.kb_vector = D_STOP
            # 3-key cardinals
            elif len(self.kb_direction_list) == 3:
                if ('up' in self.kb_direction_list) and ('left' in self.kb_direction_list) \
                        and ('right' in self.kb_direction_list):
                    self.facing = 'up'
                    self.kb_vector = D_UP
                elif ('down' in self.kb_direction_list) and ('left' in self.kb_direction_list) \
                        and ('right' in self.kb_direction_list):
                    self.facing = 'down'
                    self.kb_vector = D_DOWN
                elif ('left' in self.kb_direction_list) and ('up' in self.kb_direction_list) \
                        and ('down' in self.kb_direction_list):
                    self.facing = 'left'
                    self.kb_vector = D_LEFT
                elif ('right' in self.kb_direction_list) and ('up' in self.kb_direction_list) \
                        and ('down' in self.kb_direction_list):
                    self.facing = 'right'
                    self.kb_vector = D_RIGHT
            # 4-key stop
            else:
                self.facing = 'down'
                self.kb_vector = D_STOP
        else:
            self.kb_vector = D_STOP
