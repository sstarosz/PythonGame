import os
import sys
import pygame as pg
from Player import *
from Background import *
vec2 = pg.math.Vector2

class Game:
    def __init__(self):    
        #game setings
        self.game_run = False
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.clock = pg.time.Clock()
        self.last_time = 0
        self.font_name = pg.font.match_font('arial')

        #init pygame and screen
        pg.mixer.pre_init(48000, -16, 1, 1024)
        pg.mixer.init()
        pg.init()
        pg.display.set_caption("Cow Farm")
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))

        #background
        self.background = None

        #all players tab
        self.all_players = []

        self.platforms_tab = []
        self.all_platforms = pg.sprite.Group() #platfroms array

        #audio array
        self.Sounds = {}

        #load all images
        self.load_data()



    def start_new_game(self):   
        self.screen.fill((26, 145, 28))
        self.draw_text("KROWY", 48, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, (255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play", 22,(255,255,255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 22)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

        self.game_loop()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def game_loop(self):
        self.Sounds['Backgournd'].play(loops=-1,maxtime = 0, fade_ms = 500)
        self.game_run = True
        while self.game_run:
            #force game to to run in 60 FPS
            self.clock.tick(self.FPS)

            ## cound player offset
            player_position = self.all_players[0].pos
            offset_x = 0
            if player_position.x > 600:
                offset_x = int(player_position.x - 600)
  
            #cound elapsed time betwen each frame
            current = pg.time.get_ticks()
            elapsed = (current - self.last_time) * 0.001

            self.proces_events()
            self.update()
            self.draw(offset_x)
            pg.display.update()

            #update time
            self.last_time = current
            self.last_pos_y = -1000

    def load_data(self):
        #path to img folder
        self.img_directory = os.path.join(os.path.dirname(__file__), 'img')
        self.sound_directory = os.path.join(os.path.dirname(__file__),'sound')
        
        ##audio read
        background_song_path = os.path.join(self.sound_directory, 'Happy Tune.ogg')
        jump_song_path = os.path.join(self.sound_directory, 'Jump33.wav')
        moo_song_path = os.path.join(self.sound_directory, 'Cow-moo-sound.wav')
        hit_song_path = os.path.join(self.sound_directory, 'hit_ground.wav')


        self.Sounds['Backgournd'] = pg.mixer.Sound(background_song_path)
        self.Sounds['Jump'] =  pg.mixer.Sound(jump_song_path)
        self.Sounds['Moo'] = pg.mixer.Sound(moo_song_path)
        self.Sounds['Hit'] = pg.mixer.Sound(hit_song_path)
        self.Sounds['Hit'].set_volume(0.5)

        #path to sprite and background file
        background_image = os.path.join(self.img_directory,'background.png')
        background_tree_path = os.path.join(self.img_directory,'tree.png')
        cow_sprite_path =  os.path.join(self.img_directory,'cow2.png')
        cow_black_sprite_path =  os.path.join(self.img_directory,'cow_dark2.png')
        fruit_path = os.path.join(self.img_directory, 'Fruit.png')
        platform_path = os.path.join(self.img_directory, 'Platforms.png')
        
        ##Create Backgorund
        self.background = Background(self,background_image)
        background_tree = Background_Object(self,background_tree_path)
        self.background.add_object(background_tree)
        
        ##Create Platforms
        platform_localization = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,16,17,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [16,17,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,17,18,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,0,0,0,16,17,18,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,1,2,11,5,5,5,1,0,0,0,0,0,16,17,18],
                                [0,1,2,3,0,0,0,1,2,11,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0]]


        for k in range(len(platform_localization)):
            for x in range(len(platform_localization[k])):
                if platform_localization[k][x] == 0:
                    continue
                position = ((x * 64 + 32),k * 64 +52)
                platform = Platform(self,Spritesheet(platform_path),position,(platform_localization[k][x] - 1))
                self.all_platforms.add(platform)

        ##Create Players
        #load  player sprites  
        cow_sprite = Spritesheet(cow_sprite_path )
        cow_black_sprite = Spritesheet(cow_black_sprite_path)

        self.cow = Player(self, cow_sprite, vec2(380, 501), True)
        self.cow_black = Player(self, cow_black_sprite, vec2(100, 120), False)

        self.all_players.append(self.cow)
        self.all_players.append(self.cow_black)

    def proces_events(self):
        #proces user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_run = False
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.all_players[0].jump = True
 
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                     self.all_players[0].jump = False

        #parse user input
        for player in self.all_players:
            if player.player:
                player.control()

    def update(self):                   
        self.all_players[0].hit = False
        colision_tolerance = 20
        player_rect = self.all_players[0].rect.copy()
        for platform in self.all_platforms:
            if  player_rect.colliderect(platform.rect):
                if self.all_players[0].vel.y > 0:
                    #Colision Y asix up
                    if abs(platform.rect.top - self.all_players[0].rect.bottom) < colision_tolerance and self.all_players[0].vel.y > 0:
                        player_rect.bottom = platform.rect.top 
                        self.all_players[0].pos.y = platform.rect.top
                        self.last_pos_y = platform.rect.top
                        self.all_players[0].vel.y = 0
                        self.all_players[0].hit = True
       
                    #Colision Y asix down
                    if abs(platform.rect.bottom - self.all_players[0].rect.top) < colision_tolerance and self.all_players[0].vel.y < 0:                      
                        player_rect.top = platform.rect.bottom
                        self.all_players[0].pos.y = platform.rect.bottom + player_rect.height
                        self.last_pos_y = platform.rect.bottom + player_rect.height
                        self.all_players[0].vel.y = 0   
                        self.all_players[0].hit = True          
                   
                if  player_rect.colliderect(platform.rect):
                    #Colision X asix right
                    if abs(platform.rect.right - self.all_players[0].rect.left) < colision_tolerance and self.all_players[0].vel.x < 0:
                        if not pg.mixer.Channel(2).get_busy():
                            pg.mixer.Channel(2).play(self.Sounds['Hit'])
                        self.all_players[0].pos.x = platform.rect.right + int(round(player_rect.width / 2))
                        self.all_players[0].vel.x = 0    

                    #Colision X asix left
                    if abs(platform.rect.left - self.all_players[0].rect.right) < colision_tolerance and self.all_players[0].vel.x > 0:
                        if not pg.mixer.Channel(3).get_busy():
                             pg.mixer.Channel(3).play(self.Sounds['Hit'])
                        self.all_players[0].pos.x = platform.rect.left - int(round(player_rect.width / 2))
                        self.all_players[0].vel.x = 0   



        #colision with floor
        floor = pg.Rect(0,500,999999999,1)
        for player in self.all_players:
            floor_hits = floor.colliderect(player.rect)

            if floor_hits:
                player.pos.y = 500
                player.vel.y = 0
                self.all_players[0].hit = True



        #update playerss
        for player in self.all_players:
            player.update()

    def draw(self,offset_x):
        self.screen.fill((0,0,0))
        self.background.draw(offset_x*0.33)

        #draw all players
        for player in self.all_players:
            player.draw(offset_x)
 
        for platform in self.all_platforms:
            platform.draw(offset_x)


    def draw_text(self, text, size, color, x, y):
            font = pg.font.Font(self.font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (int(round(x)), int(round((y))))
            self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    game = Game()
    game.start_new_game()
    