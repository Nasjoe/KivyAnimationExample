#!/usr/bin/python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import *
import json

#pour le passage d'arguments
from functools import partial

from kivy.clock import Clock

ex = 800
ey = 600

#taille de l'écran
Window.size = (480, 800)

class Test(App):

    def build(self):
        #titre
        self.title = 'manaRpg'
        self.content = FloatLayout(size_hint=(None, None),size=(ex, ey))

        # self.backimg = Image(source='bkgimg2.jpg')
        # self.backimg = Image(source='bkgimg2.jpg',norm_image=True)
        self.backimg = Image(source='bkgimg2.jpg')

        class Personnage:
            def NewEtat(self,etat):
                self.img = self.__dict__[etat]
                self.atlasFile = "Atlas/"+self.nom+"/"+etat+"/"+etat+".atlas"

                self.sprite = 1
                self.maxSprite = 0

                with open(self.atlasFile) as file:
                    for line in file:
                        Dict = json.loads(line)
                        for key in Dict :
                            self.maxSprite += len(Dict[key])

                return self.img+'{:03}'.format(1)

            def __init__(self, nom) :
                self.nom = nom

                self.idle = "atlas://Atlas/"+nom+"/idle/idle/image"
                self.run = "atlas://Atlas/"+nom+"/run/run/image"
                self.attaque = "atlas://Atlas/"+nom+"/attaque/attaque/image"
                self.hit = "atlas://Atlas/"+nom+"/hit/hit/image"

                self.NewEtat('idle')


        self.persoG = Personnage("LoupGarou")
        self.persoD = Personnage("RedBaron")

        self.anim_buttonG = Button(on_press=self.courirG,size_hint=(None,None),size=(120,20),pos=(0,0),text="Attaque")
        self.content.add_widget(self.anim_buttonG)

        self.anim_buttonD = Button(on_press=self.courirD,size_hint=(None,None),size=(120,20),pos=(360,0),text="Attaque")
        self.content.add_widget(self.anim_buttonD)

        self.spriteG = Image(source = self.persoG.img+'{:03}'.format(1),size_hint=(None,None),size=(300,300),pos=(-70,300))
        self.spriteD = Image(source = self.persoD.img+'{:03}'.format(1),size_hint=(None,None),size=(300,300),pos=(260,300))

        self.content.add_widget(self.spriteG)
        self.content.add_widget(self.spriteD)
        # import ipdb; ipdb.set_trace()

        
        self.C1 = Clock.schedule_interval(self.animeSpriteG, 1/40)
        self.C2 = Clock.schedule_interval(self.animeSpriteD, 1/40)

        return self.content


    def courirG(self, *args):
        # pour mettre le personnage sur le dernier Zindex :
        self.content.remove_widget(self.spriteG)
        self.content.add_widget(self.spriteG)

        # change son état :
        self.spriteG.source = self.persoG.NewEtat('run')

        animation = Animation(x=160,y=300,duration=0.7)
        animation.bind(on_complete=self.attaqueG)
        animation.start(self.spriteG)

    def attaqueG(self, *args):

        self.spriteG.source = self.persoG.NewEtat('attaque')
        self.spriteD.source = self.persoD.NewEtat('hit')

        animation = Animation(x=160,y=300,duration=1)
        animation.bind(on_complete=self.IdleG)

        animation.start(self.spriteG)
        
    
    def IdleG(self,*args):
        self.spriteG.source = self.persoG.NewEtat('idle')
        self.spriteD.source = self.persoD.NewEtat('idle')
        self.spriteG.pos=(-70,300)


    def animeSpriteG(self,*args):
        if self.persoG.sprite < self.persoG.maxSprite :
            self.spriteG.source = self.persoG.img+'{:03}'.format(self.persoG.sprite)
            self.persoG.sprite += 1
        else :
            self.persoG.sprite = 1
            self.spriteG.source = self.persoG.img+'{:03}'.format(self.persoG.sprite)


    def courirD(self, *args):
        # pour mettre le personnage sur le dernier Zindex, on le retire et on le rajoute. Seule solution trouvée sur les forums... :
        self.content.remove_widget(self.spriteD)
        self.content.add_widget(self.spriteD)

        self.spriteD.source = self.persoD.NewEtat('run')

        animation = Animation(x=20,y=300,duration=0.7)
        animation.bind(on_complete=self.attaqueD)
        animation.start(self.spriteD)

    def attaqueD(self, *args):
        self.spriteD.source = self.persoD.NewEtat('attaque')
        self.spriteG.source = self.persoG.NewEtat('hit')

        animation = Animation(x=20,y=300,duration=1)
        animation.bind(on_complete=self.IdleD)

        animation.start(self.spriteD)
        
    
    def IdleD(self,*args):
        self.spriteD.source = self.persoD.NewEtat('idle')
        self.spriteG.source = self.persoG.NewEtat('idle')
        self.spriteD.pos=(260,300)


    def animeSpriteD(self,*args):
        if self.persoD.sprite < self.persoD.maxSprite :
            self.spriteD.source = self.persoD.img+'{:03}'.format(self.persoD.sprite)
            self.persoD.sprite += 1
        else :
            self.persoD.sprite = 1
            self.spriteD.source = self.persoD.img+'{:03}'.format(self.persoD.sprite)

        if self.spriteD.texture.uvsize[0] > 0 :
            self.spriteD.texture.flip_horizontal()


if __name__ == '__main__':
    Test().run()
