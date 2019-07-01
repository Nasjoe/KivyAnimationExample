#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import *

#pour le passage d'arguments
from functools import partial

from kivy.clock import Clock

ex = 800
ey = 600

Window.size = (480, 800)

class Test(App):

    def build(self):
        #titre
        self.title = 'manaRpg'
        #taille de l'écran
        self.content = FloatLayout(size_hint=(None, None),size=(ex, ey))

        self.anim_button = Button(on_press=self.courir,size_hint=(None,None),size=(120,20),pos=(0,0),text="Attaque")
        self.content.add_widget(self.anim_button)

        self.img = "atlas://baronIdle/myatlas/baron_idle"
        self.maxSprite = 46

        self.sprite = Image(source = self.img+"1",size_hint=(None,None),size=(150,150),pos=(330,325))
        self.content.add_widget(self.sprite)
        self.temps = 0
        self.imgSprite1 = 1
        self.dirSprite1 = 1
        Clock.schedule_interval(partial(self.animeSprite,2), 1.0/60.0)
        return self.content

    def courir(self, *args):
        self.img = "atlas://baronrun/myatlas/baron_run"
        self.maxSprite = 16

        animation = Animation(x=60,y=325,duration=0.5)
        animation.bind(on_complete=self.attaque)

        animation.start(self.sprite)

    def attaque(self, *args):
        self.img = "atlas://baronattackA/myatlas/baron_attackA"
        self.maxSprite = 37

        animation = Animation(x=50,y=325,duration=2)
        animation.bind(on_complete=self.Idle)

        animation.start(self.sprite)
    
    def Idle(self,*args):
        self.sprite.pos=(330,325)
        self.img = "atlas://baronIdle/myatlas/baron_idle"
        self.maxSprite = 46

    def animeSprite(self,inter,*args):
        #animation sprite
        self.temps = self.temps + 1
        if self.temps>inter:
            self.temps = 0
            self.imgSprite1 = self.imgSprite1 + 1
            if self.imgSprite1>self.maxSprite:
                self.imgSprite1 = 1
            
        image = self.img+str(self.imgSprite1)
        self.sprite.source = image
        #deplacement sprite
        # self.sprite.x = self.sprite.x + self.dirSprite1
        # if self.sprite.x>760 or self.sprite.x<40:
        #     self.dirSprite1 = -self.dirSprite1
        # print(self.sprite.x)
if __name__ == '__main__':
    Test().run()
    
