# Libraries
# from turtle import distance
from telnetlib import GA
import arcade
from pyglet.math import Vec2
import random
import os
from firebase_con import *
from firebase_admin import db
# import thread module
import threading

import sys
import time
from hand import *

# Constants
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Stick Racing"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING)
VIEWPORT_MARGIN = SPRITE_PIXEL_SIZE * SPRITE_SCALING
RIGHT_MARGIN = 4 * SPRITE_PIXEL_SIZE * SPRITE_SCALING
MOVEMENT_SPEED = 50 * SPRITE_SCALING
JUMP_SPEED = 20 * SPRITE_SCALING
GRAVITY = 0.7* SPRITE_SCALING
CAMERA_SPEED = 0.1

# Main game class
class MyGame(arcade.Window):
 
    def __init__(self, width, height, title , user_name, room_id):
      
        super().__init__(width, height, title)
        # thread.start_new_thread ( function, args[, kwargs] )
    
        # run the thread
        self.Hand_Class = ThisClass()
        self.thread = threading.Thread(target=self.Hand_Class.get_hand_position)
        self.thread2 = threading.Thread(target=self.setup , args=(self))
        self.thread.start()
        self.thread2.start()
        self.result_local = -1
        self.room_id = room_id
        # print(self.thread.join(), self.thread2.join())


        # self.time_clock = clock()
        self.x = 0
        self.static_wall_list = None
        self.moving_wall_list = None
        self.stop_movment = False
        self.player_list = None
        self.user_name = user_name
        self.player_sprite = None
        self.physics_engine = None
        self.game_over = False

        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.left_down = False
        self.speed_flag = False
    def Revive(self ):
        self.player_sprite.center_x = self.x - 1*GRID_PIXEL_SIZE
        self.player_sprite.center_y = 6 * GRID_PIXEL_SIZE
        self.stop_movment = True
    def setup(self):
        
        self.static_wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        # Character
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
        # Map creation
        for i in range(10):            
            rand = random.randint(80 , 200)
            # y_rand = counters
            for o in range(10):
                countes = 1
                for i in range(5):
                    wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING)
                    wall.center_x =  10000
                    wall.center_y = countes * GRID_PIXEL_SIZE
                    self.static_wall_list.append(wall)
                    countes += 1
                y_heights = rand
            for j in range(rand):
                wall = arcade.Sprite(":resources:images/tiles/sandMid.png", SPRITE_SCALING)
                # wall.bottom = 20 * 
                wall.center_x = (j)*random.randint(1,9)* GRID_PIXEL_SIZE 
                if(random.randint(0,5)==0):
                    # y_heights += random.randint(1,3)  
                    rands = random.randint(2,4)
                    for v in range(rands):
                     wall.center_y = v*GRID_PIXEL_SIZE


                self.static_wall_list.append(wall)


            # counters+=1
            counter = counter*random.randint(2, 4)
        
        wall = arcade.Sprite(":resources:images/tiles/sandMid.png", SPRITE_SCALING)
        wall.center_y = 3 * GRID_PIXEL_SIZE
        wall.center_x = 3 * GRID_PIXEL_SIZE
        wall.boundary_left = 2 * GRID_PIXEL_SIZE
        wall.boundary_right = 5 * GRID_PIXEL_SIZE
        wall.change_x = 2 * SPRITE_SCALING

        wall = arcade.Sprite(":resources:images/tiles/sandMid.png", SPRITE_SCALING)
        wall.center_y = 3 * GRID_PIXEL_SIZE
        wall.center_x = 7 * GRID_PIXEL_SIZE
        wall.boundary_left = 5 * GRID_PIXEL_SIZE
        wall.boundary_right = 9 * GRID_PIXEL_SIZE
        wall.change_x = -2 * SPRITE_SCALING


        wall = arcade.Sprite(":resources:images/tiles/sandMid.png", SPRITE_SCALING)
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
        # if self.stop_movment:
            # for i in range(4):
                # time.sleep(1)
        # print()
        # wait for key press
        
        if ~self.speed_flag:
            self.player_sprite.change_x = MOVEMENT_SPEED /8 
        # if 
        self.x = self.player_sprite.center_x
        if self.Hand_Class.result != self.result_local:
            print(self.Hand_Class.result)
            self.result_local = self.Hand_Class.result
            if self.Hand_Class.result == 2:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = JUMP_SPEED
        distance = self.player_sprite.right
        if distance > 1000:
            self.game_over = True
            print(self.user_name)
            print(self.room_id)

            db.reference('rooms').child(self.room_id).child('users').child(self.user_name).update({
                'time': self.time,
            })
            time_list = []
            for i in list:
                if list[i]['status'] == 'over' and list[i]['name']!=self.user_name:
                    time_list.append(list[i]['time'])
            time_list.sort()
            rank = 0
            for i in time_list:
                if i > self.time:
                    rank += 1
            self.rank = rank
            print(rank)


                

            
        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.RIGHT:
            self.speed_flag = True
            self.set_x_speed()
        elif key == arcade.key.R:
            self.Revive()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_down = False
            self.set_x_speed()
        elif key == arcade.key.RIGHT:
            self.speed_flag = False
            self.set_x_speed()

    def on_update(self, delta_time):
        distance = self.player_sprite.top
        # print(distance)
        

       
        if(distance < -500):
            self.game_over = True
            print("GAME OVER")
            # game over
            # restart game
            self.Revive()
            # time.sleep(5)
              
            
        self.physics_engine.update()

        self.scroll_to_player()

        

    def scroll_to_player(self):
       

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)


def main(user_name , room_id):
   
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE , user_name , room_id)
    window.setup()
    arcade.run()


def create_room(name):
    # create random room id
    room_id = random.randint(10000, 99999)
    print("Enter a time to wait for other players: ")
    time_wait = int(input())
    # create room
    print("Room id: " + str(room_id))
    print("Will Start in 60 seconds!")
    db.reference("rooms").child(str(room_id)).set({"room_id": room_id})
    db.reference("rooms").child(str(room_id)).child("players").push({"name": f'{name}', "admin": True})
    time_count  = time_wait
    while time_count > 0:
       
        print(time_count)
        time_count -= 1
        list = db.reference("rooms").child(str(room_id)).child("players").get()
        # update time in database
        db.reference("rooms").child(str(room_id)).update({"time": time_count})
        print()
        print("Players: ")
        for i in list:
            print(db.reference("rooms").child(str(room_id)).child("players").child(i).get()['name'])
        # CLEANING THE TERMINAL
        # os.system('cls' if os.name == 'nt' else 'clear')
        print()
        time.sleep(1)
        print("Game Started!")
        GameScreen = main(room_id , name)

  


        
        

    # create room
def join_room( name, room_id):
    # join room 
    room_exist = db.reference("rooms").child(str(room_id)).get({"room_id": room_id})
    if room_exist[0] is None:
        print("Room does not exist")
        return
    else:
        db.reference("rooms").child(str(room_id)).child("players").push({"name": f'{name}', "admin": False})
        # start game in time count
        
        print("Joined room")
        time_count = db.reference("rooms").child(str(room_id)).get()["time"]
        print(f'Game is starting in {time_count} seconds!')

        while(time_count > 0):
            time_count = db.reference("rooms").child(str(room_id)).get()["time"]
            print()
            print()
            print("Time: ", time_count)
            time.sleep(1)
        print("Game started")
        # start game
        GameScreen = main(name , room_id)
        # GameScreen.name = name
        return
    pass

ref = db.reference('/')

if __name__ == "__main__":
    # main()
    print("Enter Your Name: ")
    name = input()
    # clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Hello " + name + "!")
    print("Choose your option: ")
    print("1. Join Room")
    print("2. Create Room")
    print("3. Exit")
    option = int(input())
    if option == 1:
        print("Enter Room ID: ")
        room_id = input()
        
        join_room(name,room_id)
    elif option == 2:
        create_room(name)
    elif option == 3:
        exit()
    else:
        print("Invalid Option")
        exit()

    

