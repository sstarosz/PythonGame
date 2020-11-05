import pygame as pg
vec2 = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height),pg.SRCALPHA)   
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self,game,name,pos,playable):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.player = playable
        self.spritesheet = self.game.player_sprite[name]
        self.image = self.spritesheet.get_image(33, 25, 99, 119)

        #position
        self.rect = self.image.get_rect()

        self.jump = False
        self.pos = pos
        self.acc = vec2(0,0)
        self.vel = vec2(0, 160)
        self.GRAVITY = vec2(0,-160)
        self.flip_h = False

        #player sprite image group
        self.move_forward_frames = []
        self.move_left_right_frames = []
        self.move_back_frames = []
        self.utility_frames = []
        self.sleep_framse = []
        self.idle_frames = []
        self.load_frames()

        self.player_state_frames = {
            "WALK_LEFT": (self.move_left_right_frames, 180),
            "WALK_RIGHT": (self.move_left_right_frames, 180),
            "IDLE": (self.idle_frames,350),
            "SLEEP": (self.sleep_framse,350),
            "TONGUE":(self.utility_frames,350)
        }

        #animation
        self.update_state = False
        self.last_update = 0
        self.current_frame = 0
        self.player_state = "IDLE"
        self.walk_speed = 80


    def set_position(self,new_pos):
        self.pos = new_pos

    def get_position(self):
        return self.pos

    def set_x_position(self,new_x):
        self.pos.x = new_x

    def set_y_position(self,new_y):
            self.pos.y = new_y

    def update(self, elapsed_time):

        #parse user input
        if self.player:
            self.control(elapsed_time)
        
        # update animation
        actual_time = pg.time.get_ticks()
        if actual_time - self.last_update > self.player_state_frames[self.player_state][1]:
            self.animation()
            self.last_update = actual_time


    def control(self,elapsed_time):
        #parse user input
        self.update_state = False
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.update_state = True
            self.flip_h = True
            self.player_state = "WALK_LEFT"
            self.set_x_position(self.pos.x - self.walk_speed * elapsed_time)

        if  keys[pg.K_RIGHT]:
            self.update_state = True
            self.flip_h = False
            self.player_state = "WALK_RIGHT"
            self.set_x_position(self.pos.x + self.walk_speed * elapsed_time)

        if keys[pg.K_SPACE]:
            self.jump = True

        if keys[pg.K_q]:
            self.update_state = True
            self.player_state = "TONGUE"

        if self.jump:
            self.pos -= self.vel * elapsed_time
            self.vel += self.GRAVITY * elapsed_time
            if self.pos.y > 500:
                self.pos.y = 500
                self.jump = False
                self.vel = vec2(0, 160)

        if self.update_state == False and not self.jump :
            self.player_state = "IDLE"



    def animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.player_state_frames[self.player_state][0])
        bottom = self.rect.bottom
        self.image = self.player_state_frames[self.player_state][0][self.current_frame]

        #flip image
        if self.flip_h:
            self.image = pg.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.midbottom = self.pos

    def load_frames(self):
        self.move_forward_frames = [self.spritesheet.get_image(0, 0, 159, 159),
                                    self.spritesheet.get_image(160, 0, 159, 159),
                                    self.spritesheet.get_image(320, 0, 159, 159),
                                    self.spritesheet.get_image(480, 0, 159, 159)]

        self.move_left_right_frames = [self.spritesheet.get_image(0, 160, 159, 159),
                                       self.spritesheet.get_image(160, 160, 159, 159),
                                       self.spritesheet.get_image(320, 160, 159, 159),
                                       self.spritesheet.get_image(480, 160, 159, 159)]

        self.move_back_frames = [self.spritesheet.get_image(0, 320, 159, 159),
                                 self.spritesheet.get_image(160, 320, 159, 159),
                                 self.spritesheet.get_image(320, 320, 159, 159),
                                 self.spritesheet.get_image(480, 320, 159, 159)]

        self.sleep_framse = [self.spritesheet.get_image(160, 640, 159, 159),
                             self.spritesheet.get_image(0, 480, 159, 159),
                             self.spritesheet.get_image(160, 480, 159, 159),]

        self.utility_frames = [self.spritesheet.get_image(160, 640, 159, 159),
                               self.spritesheet.get_image(320, 640, 159, 159),
                               self.spritesheet.get_image(480, 640, 159, 159)]

        self.idle_frames = [self.spritesheet.get_image(0, 640, 159, 159)]

    def draw(self):
        self.game.screen.blit(self.image,self.rect)
       