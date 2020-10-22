import os
import pygame as pg
from Player import *
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

        #init pygame and screen
        pg.init()
        pg.display.set_caption("Cow Farm")
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))

        #load all images
        self.load_data()

        #all create players
        self.create_players()


    def start_new_game(self):
        self.clock.tick(self.FPS)       
        self.game_loop()

    def game_loop(self):
        self.game_run = True
        while self.game_run:
            #force game to to run in 60 FPS
            self.clock.tick(self.FPS)

            #cound elapsed time betwen each frame
            current = pg.time.get_ticks()
            elapsed = (current - self.last_time) * 0.001

            self.proces_events()
            self.update(elapsed)
            self.draw()
            pg.display.update()

            self.last_time = current

    def load_data(self):
        #path to img folder
        self.img_directory = os.path.join(os.path.dirname(__file__), 'img')
        
        #path to sprite and background file
        self.background_image = os.path.join(self.img_directory,'background.png')
        self.cow_sprite_path =  os.path.join(self.img_directory,'cow.png')
        self.cow_black_sprite_path =  os.path.join(self.img_directory,'cow_dark.png')

        #load background image
        self.background_image = pg.image.load(self.background_image).convert()

        #load sprites  
        self.player_sprite = {}   
        cow_sprite = Spritesheet(self.cow_sprite_path )
        cow_black_sprite = Spritesheet(self.cow_black_sprite_path)

        self.player_sprite['Cow'] = cow_sprite
        self.player_sprite['CowBlack'] = cow_black_sprite

    def create_players(self):
        self.all_players = []
        self.cow = Player(self, 'Cow', vec2(400, 500), True)
        self.cow_black = Player(self, 'CowBlack', vec2(600, 500), False)

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
                if event.key == pg.K_ESCAPE:
                    pg.quit()

    def update(self,elapsed):
        for player in self.all_players:
            player.update(elapsed)

    def draw(self):
        #draw background
        self.screen.blit(self.background_image,(0,0))

        #draw all players
        for player in self.all_players:
            player.draw()



if __name__ == "__main__":
    game = Game()
    game.start_new_game()
    