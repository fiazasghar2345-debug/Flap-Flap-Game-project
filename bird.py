import pygame as pg
import random

class Bird(pg.sprite.Sprite):
    def __init__(self,scale):
        super(Bird,self).__init__()
        self.image_list=[pg.transform.scale_by(pg.image.load("Assests\\birdup.png").convert_alpha(),scale),
                        pg.transform.scale_by(pg.image.load("Assests\\birddown.png").convert_alpha(),scale)]
        self.image_index=0
        self.image=self.image_list[self.image_index]
        self.rect=self.image.get_rect(center=(120,200))
        self.y_velocity=0
        self.gravity=10
        self.flap_speed=300
        self.anim_counter=0
    def update(self,dt):
        self.apply_gravity(dt)
        self.play_anim()
        if self.rect.y<=0 and self.flap_speed==300:
            self.rect.y=0
            self.flap_speed=0
            self.y_velocity=0
        elif self.rect.y>0 and self.flap_speed==0:
            self.flap_speed=300
    def apply_gravity(self,dt):
        self.y_velocity+=self.gravity*dt
        self.rect.y+=self.y_velocity
    def flap(self,dt):
        self.y_velocity=0
        self.y_velocity -=self.flap_speed*dt
    def play_anim(self):
        if self.anim_counter==9:
            self.image=self.image_list[self.image_index]
            if self.image_index==0: self.image_index=1
            else:
                self.image_index=0
            self.anim_counter=0
        self.anim_counter+=1