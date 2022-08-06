import arcade
from pyglet.math import Vec2
import random
SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Stick Racing"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING)

VIEWPORT_MARGIN = SPRITE_PIXEL_SIZE * SPRITE_SCALING
RIGHT_MARGIN = 4 * SPRITE_PIXEL_SIZE * SPRITE_SCALING
MOVEMENT_SPEED = 50 * SPRITE_SCALING
JUMP_SPEED = 20 * SPRITE_SCALING
GRAVITY = 1* SPRITE_SCALING
UPDATES_PER_FRAME = 5
CAMERA_SPEED = 0.1

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class MyGame(arcade.Window):
    """ Main application class. """
    
    def __init__(self, width, height, title):
        """ Initializer """

        super().__init__(width, height, title)
        self.character_face_direction = 1
        self.cur_texture = 0
        self.scale = 1
        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction


        self.static_wall_list = None
        self.moving_wall_list = None

        self.player_list = None
    
        self.player_sprite = None
        self.physics_engine = None
        self.game_over = False

        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.left_down = False
        self.speed_flag = False
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
        self.texture = self.walk_textures[frame][direction]
            
    def update_animation(self, delta_time: float = 1 / 60):

            if self.change_x < 0 and self.character_face_direction == 1:
                self.character_face_direction = 0
            elif self.change_x > 0 and self.character_face_direction == 0:
                self.character_face_direction = 1

            if self.change_x == 0 and self.change_y == 0:
                self.texture = self.idle_texture_pair[self.character_face_direction]
                return


    def setup(self):
        """ Set up the game and initialize the variables. """

        self.static_wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/"
                                           "femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player_sprite.center_x = 2 * GRID_PIXEL_SIZE
        self.player_sprite.center_y = 3 * GRID_PIXEL_SIZE
        self.player_list.append(self.player_sprite)
        counter = 1
        # for i in range(20):
        #     wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING)
        #     wall.center_x = counter * GRID_PIXEL_SIZE
        #     wall.center_y = 3 * GRID_PIXEL_SIZE
        #     self.static_wall_list.append(wall)
        #     counter += 1
        counters = 1
        for i in range(30):            
            rand = random.randint(30 , 200)
            # y_rand = counters
            y_heights = rand
            for j in range(rand):
                wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
                # wall.bottom = 20 * 
                wall.center_x = (j)*random.randint(2,10)* GRID_PIXEL_SIZE 
                # wall.center_y = y_heights
                self.static_wall_list.append(wall)
            # counters+=1
            counter = counter*random.randint(2, 6)
        
        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 3 * GRID_PIXEL_SIZE
        wall.center_x = 3 * GRID_PIXEL_SIZE
        wall.boundary_left = 2 * GRID_PIXEL_SIZE
        wall.boundary_right = 5 * GRID_PIXEL_SIZE
        wall.change_x = 2 * SPRITE_SCALING

        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 3 * GRID_PIXEL_SIZE
        wall.center_x = 7 * GRID_PIXEL_SIZE
        wall.boundary_left = 5 * GRID_PIXEL_SIZE
        wall.boundary_right = 9 * GRID_PIXEL_SIZE
        wall.change_x = -2 * SPRITE_SCALING


        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 5 * GRID_PIXEL_SIZE
        wall.center_x = 8 * GRID_PIXEL_SIZE
        wall.boundary_left = 7 * GRID_PIXEL_SIZE
        wall.boundary_right = 9 * GRID_PIXEL_SIZE
        wall.boundary_top = 8 * GRID_PIXEL_SIZE
        wall.boundary_bottom = 4 * GRID_PIXEL_SIZE
        wall.change_x = 2 * SPRITE_SCALING
        wall.change_y = 2 * SPRITE_SCALING

        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.player_sprite,
                                           [self.static_wall_list],
                                           gravity_constant=GRAVITY)

        arcade.set_background_color(arcade.color.AMAZON)

        self.game_over = False

    def on_draw(self):
        """
        Render the screen.
        """

        self.clear()

        self.camera_sprites.use()

        self.static_wall_list.draw()
        self.player_list.draw()

        self.camera_gui.use()

        distance = self.player_sprite.right
        output = f"Distance: {distance}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def set_x_speed(self):
        if self.speed_flag and not self.left_down:
            self.player_sprite.change_x = MOVEMENT_SPEED
        
        
    # LOOP
    def update(self, delta_time):
        """ Movement and game logic """
        if ~self.speed_flag:
            self.player_sprite.change_x = MOVEMENT_SPEED /5
          

    def on_key_press(self, key, modifiers):
        """ Called whenever the mouse moves. """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.RIGHT:
            self.speed_flag = True
            self.set_x_speed()

    def on_key_release(self, key, modifiers):
        """ Called when the user presses a mouse button. """
        if key == arcade.key.LEFT:
            self.left_down = False
            self.set_x_speed()
        elif key == arcade.key.RIGHT:
            self.speed_flag = False
            self.set_x_speed()

    def on_update(self, delta_time):
        """ Movement and game logic """
        distance = self.player_sprite.top
        print(distance)
        if(distance < -1000):
            self.game_over = True
            print("GAME OVER")
            # game over
            # restart game
            self.setup()
            
        self.physics_engine.update()
        # self.player_list.update()
        self.update_animation()
        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()