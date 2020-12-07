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
    def __init__(self,game,sprite,pos,playable):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.player = playable
        self.spritesheet = sprite

        #position
        self.rect = pg.Rect(0,0,159,159)
        self.hit = True
        self.last_hit = True
        self.jump = False
        self.pos = pos      #vec2
        self.acc = vec2(0,0)
        self.vel = vec2(0,0)
        self.GRAVITY = 0.8
        self.flip_h = False

        #player sprite image group
        self.move_forward_frames = []
        self.move_left_right_frames = []
        self.move_back_frames = []
        self.utility_frames = []
        self.sleep_framse = []
        self.idle_frames = []
        self.load_frames()

        #Action, table that store all image frames, frame rate to play up animation
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

    def update(self):
        
        # update animation
        actual_time = pg.time.get_ticks()
        if actual_time - self.last_update > self.player_state_frames[self.player_state][1]:
            self.animation()
            self.last_update = actual_time

    def control(self):
        self.acc = vec2(0,0.8) #0.8 player gravity

        if not self.last_hit and self.hit:     
            if not pg.mixer.Channel(1).get_busy():
                print("hit")
                pg.mixer.Channel(1).play(self.game.Sounds['Hit'])

        #parse user input
        self.update_state = False
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.update_state = True
            self.flip_h = True   
            self.player_state = "WALK_LEFT"
            self.acc.x = -0.6

        if  keys[pg.K_RIGHT]:
            self.update_state = True
            self.flip_h = False
            self.player_state = "WALK_RIGHT"
            self.acc.x = 0.6

        if self.jump and self.vel.y == 0:
            if not pg.mixer.Channel(4).get_busy():
                pg.mixer.Channel(4).play(self.game.Sounds['Jump'])
            self.jump = False
            self.vel.y = -17

        if keys[pg.K_q]:
            self.game.Sounds['Moo'].play()
            self.update_state = True
            self.player_state = "TONGUE"

        if self.update_state == False and not self.jump :
            self.player_state = "IDLE"

         # apply friction
        self.acc.x += self.vel.x * (-0.12)
        # equations of motion
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
        self.last_hit = self.hit

    def animation(self):



        self.current_frame = (self.current_frame + 1) % len(self.player_state_frames[self.player_state][0])
        bottom = self.rect.bottom
        self.image = self.player_state_frames[self.player_state][0][self.current_frame]

        #flip image
        if self.flip_h:
            self.image = pg.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def load_frames(self):
        self.move_forward_frames = [self.spritesheet.get_image(35, 5, 94, 113),
                                    self.spritesheet.get_image(195, 5, 94, 113),
                                    self.spritesheet.get_image(355 , 5, 94, 113),
                                    self.spritesheet.get_image(515, 5, 94, 113)]

        self.move_left_right_frames = [self.spritesheet.get_image(4, 123, 154, 113 ),
                                       self.spritesheet.get_image(164, 123, 149, 113),
                                       self.spritesheet.get_image(324, 123, 154, 113),
                                       self.spritesheet.get_image(484, 123, 149, 113)]                            

        self.move_back_frames = [self.spritesheet.get_image(35, 241, 94, 113),
                                 self.spritesheet.get_image(190, 241, 94, 113),
                                 self.spritesheet.get_image(350, 241, 94, 113),
                                 self.spritesheet.get_image(510, 241, 94, 113)]

        self.sleep_framse = [self.spritesheet.get_image(190, 482, 94, 113),
                             self.spritesheet.get_image(32, 359, 94, 118),
                             self.spritesheet.get_image(192, 359, 94, 118),]

        self.utility_frames = [self.spritesheet.get_image(190, 482, 94, 113),
                               self.spritesheet.get_image(350, 487, 94, 113),
                               self.spritesheet.get_image(510, 487, 94, 110)]

        self.idle_frames = [self.spritesheet.get_image(30, 482, 94, 113)]

    def draw(self,offset):
        rect_offset = self.rect.move(-offset,0)
        self.game.screen.blit(self.image,rect_offset)
