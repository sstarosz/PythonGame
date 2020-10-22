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
    def __init__(self,game,name,pos,flip):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.spritesheet = self.game.player_sprite[name]
        self.image = self.spritesheet.get_image(33, 25, 99, 119)

        #position
        self.rect = self.image.get_rect()
       
        self.pos = pos
        self.flip_h = flip

        #player sprite image group
        self.move_forward_frames = []
        self.move_left_right_frames = []
        self.move_back_frames = []
        self.utility_frames = []
        self.idle_frames = []
        self.load_frames()

        #animation
        self.last_update = 0
        self.current_frame = 0
        self.idle_state = False
        self.walk_state = True

    def update_animation(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            #idle_frames
            if self.idle_state:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.midbottom = self.pos
            #move left right frames
            elif self.walk_state:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.move_left_right_frames)
                bottom = self.rect.bottom
                self.image = self.move_left_right_frames[self.current_frame]

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


        self.utility_frames = [self.spritesheet.get_image(0, 480, 159, 159),
                               self.spritesheet.get_image(160, 480, 159, 159),
                               self.spritesheet.get_image(320, 480, 159, 159),
                               self.spritesheet.get_image(480, 480, 159, 159)]

        self.idle_frames = [self.spritesheet.get_image(0, 640, 159, 159),
                            self.spritesheet.get_image(160, 640, 159, 159),
                            self.spritesheet.get_image(320, 640, 159, 159),
                            self.spritesheet.get_image(480, 640, 159, 159)]

    def draw(self):    
        self.game.screen.blit(self.image,self.rect)

       