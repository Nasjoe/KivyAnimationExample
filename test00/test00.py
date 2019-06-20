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

class Test(App):

    def build(self):
        #titre
        self.title = 'manaRpg'
        #taille de l'écran
        Window.size=(ex, ey)
        self.content = FloatLayout(size_hint=(None, None),size=(ex, ey))
    
        self.anim_image = Image(source = 'dot_26x26.png',size_hint=(None,None),size=(26,26),pos=(30,200))
        self.anim_button = Button(on_press=self.testAnimation,size_hint=(None,None),size=(120,20),pos=(0,0),text="animation")
        self.rota_button = Button(on_press=self.rotation,size_hint=(None,None),size=(120,20),pos=(130,0),text="rotation")
        self.content.add_widget(self.anim_image)
        self.content.add_widget(self.anim_button)
        self.content.add_widget(self.rota_button)
        
        self.sprite = Image(source = "atlas://invader/id1",size_hint=(None,None),size=(32,32),pos=(40,150))
        self.content.add_widget(self.sprite)
        self.temps = 0
        self.imgSprite1 = 1
        self.dirSprite1 = 1
        Clock.schedule_interval(partial(self.animeSprite,24,2), 1.0/60.0)
        return self.content

    def testAnimation(self, *args, **kwargs):
        animation = Animation(x=400,y=280,t='out_bounce')
        animation.start(self.anim_image)

    def animeSprite(self,inter,maxSprite,*args):
        #animation sprite
        self.temps = self.temps + 1
        if self.temps>inter:
            self.temps = 0
            self.imgSprite1 = self.imgSprite1 + 1
            if self.imgSprite1>maxSprite:
                self.imgSprite1 = 1
            
        image = "atlas://invader/id"+str(self.imgSprite1)
        self.sprite.source = image
        #deplacement sprite
        self.sprite.x = self.sprite.x + self.dirSprite1
        if self.sprite.x>760 or self.sprite.x<40:
            self.dirSprite1 = -self.dirSprite1
        print(self.sprite.x)

    def rotation(self,*args):
        with self.anim_image.canvas.before:
            PushMatrix()
            Rotate(axis=(0,0,1),angle=45,origin=self.anim_image.center)
            
        with self.anim_image.canvas.after:
            PopMatrix()
        
        
if __name__ == '__main__':
    Test().run()
    
