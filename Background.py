import pygame as pg
from Player import Spritesheet

class Background(pg.sprite.Sprite):
    def __init__(self,game,img_path):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(img_path).convert()
        self.pos = pg.math.Vector2(0,0)
        self.object_list = []

    def draw(self,offset):
        #draw repeated background 
        rec_x = (self.pos.x - offset) % self.image.get_rect().width
        self.game.screen.blit(self.image,(rec_x-self.image.get_rect().width,0))
        if rec_x < self.game.SCREEN_WIDTH:
            self.game.screen.blit(self.image,(rec_x,0))


        bg_obj_offset = offset * 1.5
        start = int(round(bg_obj_offset/250))

        for x in self.object_list:
            #draw tree
            for y in range(start-1,start + 5):
                    x.draw(pg.math.Vector2(125 + y*250 ,500),bg_obj_offset)

    def add_object(self,new_obj):
        self.object_list.append(new_obj)


class Background_Object(pg.sprite.Sprite):
    def __init__(self,game,img_path):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(img_path).convert_alpha()
        self.pos = pg.math.Vector2(500,500)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

    def draw(self,pos,offset):
        # new_pos = self.rect.copy()
        # new_pos.midbottom = pos
        pos.x = pos.x - offset
        rect_offset = self.rect.copy()
        rect_offset.midbottom = pos
        self.game.screen.blit(self.image,rect_offset)


class Platform(pg.sprite.Sprite):
    def __init__(self,game,sprite,pos,image_index):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.spritesheet = sprite
        self.pos = pos
        self.index = image_index

        #array to store images
        self.platforms_image = []
        self.load_frames()
        self.image = self.platforms_image[image_index]
        self.image = pg.transform.scale(self.image,(64,64))

        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
    
    def load_frames(self):
        self.platforms_image.append(self.spritesheet.get_image(11, 27, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(166, 27, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(319, 27, 128, 128))

        self.platforms_image.append(self.spritesheet.get_image(11, 180, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(166, 180, 128,128))
        self.platforms_image.append(self.spritesheet.get_image(319, 180, 128, 128))

        self.platforms_image.append(self.spritesheet.get_image(11, 333, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(166, 333, 128,128))
        self.platforms_image.append(self.spritesheet.get_image(319, 333, 128, 128))

        #10 11
        self.platforms_image.append(self.spritesheet.get_image(298, 27, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(651, 27, 128, 128))

        #12 13
        self.platforms_image.append(self.spritesheet.get_image(498, 180, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(651, 180, 128, 128))

        #water
        self.platforms_image.append(self.spritesheet.get_image(804, 27, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(804, 180, 128, 128))

        #platform
        self.platforms_image.append(self.spritesheet.get_image(498, 368, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(651, 368, 128, 128))
        self.platforms_image.append(self.spritesheet.get_image(804 , 368, 128, 128))


    def draw(self,offset):
        new_pos = (self.pos[0] - offset,self.pos[1])
        rect_draw = self.rect.copy()
        rect_draw.midbottom = new_pos
        self.game.screen.blit(self.image,rect_draw)