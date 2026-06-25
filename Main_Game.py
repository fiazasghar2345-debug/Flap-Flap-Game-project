
#======================Author: Ali Haider======================#
#==============================================================#
#importing libs
import pygame as pg
import sys,time
from bird import Bird
from pipe import Pipe
#Using OOP's,object oriented programming
pg.init()
#setting_game_icon
pg.display.set_icon(pg.image.load("Assests/icon.png"))
class Game:
    def __init__(self):
        self.dead_sound_played=False
        self.dead_sound=pg.mixer.Sound("Assests/sfx/dead.wav")
        self.viewable=False
        self.score=int(0)
        self.font=pg.font.Font("Assests/font.ttf",30)
        self.font_2=pg.font.Font("Assests/font.ttf",50)
        self.Game_over_lable=self.font_2.render("Game Over!",True,(0,0,0))
        self.lable_info=self.font.render(f"Score:{self.score}",True,(0,0,0))
        self.best_scole_lable=self.font.render(f"Best score:{self.score}",True,(0,0,0),(250,250,250))
        self.not_colided=True
        self.flap_sound=pg.mixer.Sound("Assests/sfx/flap.wav")
        #setting_window_configuration
        self.width=600
        self.height= 768
        self.scale_factor=1.5
        self.move_speed=250
        self.clock=pg.time.Clock()
        self.win=pg.display.set_mode((self.width,self.height))
        self.is_enter_pressed=False
        self.SetupBgAndGround()
        self.bird_scale=1.5
        self.bird= Bird(self.bird_scale)
        self.pipe_generate_counter=100
        self.dead=False
        self.pipes=[]
        self.pipe_scale=self.bird_scale
        self.pipe=Pipe(self.pipe_scale,self.move_speed)
        self.played=False
        self.Game_loop()
    def Game_loop(self):
        last_time=time.time()
        while True:
            if self.is_enter_pressed==True:
                self.played=True
            if self.is_enter_pressed==True:
                self.score+=0.05
            if self.not_colided==True:
                self.lable_info=self.font.render(f"Score:{int(self.score)}",True,(0,0,0))
            #Calculating Delta Time
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_RETURN:
                        self.is_enter_pressed=True
                    if event.key==pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)
                        if self.not_colided==True:
                            self.flap_sound.play()
                    #Kaam Ithar Rook Gheia Tha Lets Gets Started in this line Generating Pises
            if self.not_colided==True:
                self.UpdateEveryThing(dt)
                self.DrawEveryThings()
            self.checkCollisions()
            self.clock.tick(65)
            self.check_out()
            pg.display.update()
    def UpdateEveryThing(self,dt):
        if self.is_enter_pressed:
            self.ground1_rec.x-=int(self.move_speed*dt)
            self.ground2_rec.x-=int(self.move_speed*dt)
            if self.ground1_rec.right<0:
                self.ground1_rec.x=self.ground2_rec.right
            if self.ground2_rec.right<0:
                self.ground2_rec.x=self.ground1_rec.right
            if self.pipe_generate_counter>100:
                self.pipes.append(Pipe(self.pipe_scale,self.move_speed))
                self.pipe_generate_counter=0
            self.pipe_generate_counter+=1
            for pipe in self.pipes:
                pipe.update(dt)
            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)
            if self.not_colided==True:
                self.bird.update(dt)
    def DrawEveryThings(self):
            self.win.blit(self.bg_Image,(0,-300))
            for pipe in self.pipes:
                pipe.drawPipe(self.win)
            self.win.blit(self.ground1_image,self.ground1_rec)
            self.win.blit(self.ground2_image,self.ground2_rec)
            self.win.blit(self.bird.image,self.bird.rect)
            self.win.blit(self.lable_info,(400,50))
    def checkCollisions(self):
        if len(self.pipes):
            if (self.bird.rect.y>510 or
            self.bird.rect.colliderect(self.pipes[0].rect_up) or 
            self.bird.rect.colliderect(self.pipes[0].rect_down)):
                self.not_colided=False
                self.lable_info=self.font.render(" ",True,(0,0,0))
                self.win.blit(self.lable_info,(400,50))
                if self.dead_sound_played==False:
                    self.dead_sound_played=True
                    self.dead_sound.play()
    def SetupBgAndGround(self):
        #loading_images_and_other
        self.bg_Image=pg.transform.scale(pg.image.load("Assests/bg.png").convert(),(600,1066))
        self.ground1_image=pg.transform.scale_by(pg.image.load("Assests\\ground.png").convert(),self.scale_factor)
        self.ground2_image=pg.transform.scale_by(pg.image.load("Assests\\ground.png").convert(),self.scale_factor)
        self.ground1_rec=self.ground1_image.get_rect()
        self.ground2_rec=self.ground2_image.get_rect()
        self.ground1_rec.x=0
        self.ground2_rec.x=self.ground1_rec.right
        self.ground1_rec.y=568
        self.ground2_rec.y=568
    def check_out(self):
        if self.not_colided==False:
            if self.viewable==False:
                self.viewable=True
                self.win.blit(self.Game_over_lable,(150,200))
                self.best_scole_lable=self.font.render(f"Best score:{int(self.score)}",True,(0,0,0))
                self.win.blit(self.best_scole_lable,(200,300))
game=Game()