import pygame
import math
import tween
import os

class sprite:
    def __init__(self,table,sprite):
        self.positions = table
        self.x = table[0][0]
        self.y = table[0][1]
        self.w = table[0][2]
        self.h = table[0][3]
        self.r = table[0][4]
        self.sprite = pygame.image.load(sprite)
        self.spritePath = sprite
    
    def update(self,WINDOW,frame,colorshift,camera):
        if frame < len(self.positions):
            self.x = self.positions[frame][0]
            self.y = self.positions[frame][1]
            self.w = self.positions[frame][2]
            self.h = self.positions[frame][3]
            self.r = self.positions[frame][4]
        self.sprite.set_alpha(colorshift[3])
        drawSprite = pygame.transform.scale(pygame.transform.rotate(self.sprite,self.r),(abs(self.w),abs(self.h)))
        flipVert = False
        if self.h < 0:
            flipVert = True
        else:
            flipVert = False
        if self.w < 0:
            drawSprite = pygame.transform.flip(drawSprite,True,flipVert)
        else:
            drawSprite = pygame.transform.flip(drawSprite,False,flipVert)
        WINDOW.blit(drawSprite,(self.x-abs(self.w)/2+camera[0],self.y-abs(self.h)/2+camera[1]))
        #pygame.draw.ellipse(WINDOW,pygame.Color(255,255,255),(self.x-self.w/2,self.y-self.h/2,self.w,self.h))
    def edit(self,frame,mouse,WINDOW,playing,camera):
        if not playing and frame < len(self.positions):
            pygame.draw.circle(WINDOW,pygame.Color(255,255,100),(self.x+camera[0],self.y+camera[1]),20,6)
            pygame.draw.circle(WINDOW,pygame.Color(150,255,150),(self.x+self.w/2+camera[0],self.y+self.h/2+camera[1]),15,6)
            pygame.draw.circle(WINDOW,pygame.Color(150,150,255),(self.x-self.r+camera[0],self.y-self.h/2+camera[1]),15,6)
            if abs(mouse[0][0]-self.x-camera[0]) < 20 and abs(mouse[0][1]-self.y-camera[1]) < 20:
                if mouse[1][0] and frame < len(self.positions):
                    self.positions[frame][0] += mouse[2][0]*1
                    self.positions[frame][1] += mouse[2][1]*1
            if abs(mouse[0][0]-self.x-self.w/2-camera[0]) < 20 and abs(mouse[0][1]-self.y-self.h/2-camera[1]) < 20:
                if mouse[1][0] and frame < len(self.positions):
                    self.positions[frame][2] += mouse[2][0]*2
                    self.positions[frame][3] += mouse[2][1]*2
            if abs(mouse[0][0]-self.x+self.r-camera[0]) < 20 and abs(mouse[0][1]-(self.y-self.h/2)-camera[1]) < 20:
                if mouse[1][0] and frame < len(self.positions):
                    self.positions[frame][4] -= mouse[2][0]
    
    def deleteFrame(self,subject):
        self.positions.pop(subject)

    def extend(self,subject,target):
        self.positions.insert(target,self.positions[subject])

    def copy(self,subject,target):
        self.positions.insert(target,[self.positions[subject][0],
                                        self.positions[subject][1],
                                        self.positions[subject][2],
                                        self.positions[subject][3],
                                        self.positions[subject][4],
                                        1])