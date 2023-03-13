import pygame
import math
import tween
import os

class spritesheet:
    def __init__(self,table,sprite,frameAmt):
        self.positions = table
        self.x = table[0][0]
        self.y = table[0][1]
        self.w = table[0][2]
        self.h = table[0][3]
        self.r = table[0][4]
        self.sprite = pygame.image.load(sprite)
        self.spritePath = sprite
        self.frameAmt = frameAmt
        self.cFrame = table[0][5]
        self.uiStuff = [3.14]
    
    def update(self,WINDOW,frame,colorshift,camera):
        if frame < len(self.positions):
            self.x = self.positions[frame][0]
            self.y = self.positions[frame][1]
            self.w = self.positions[frame][2]
            self.h = self.positions[frame][3]
            self.r = self.positions[frame][4]
            self.cFrame = self.positions[frame][5]
        self.sprite.set_alpha(colorshift[3])
        
        frameSprite = clip(self.sprite,(self.sprite.get_size()[0]/self.frameAmt)*self.cFrame,0,self.sprite.get_size()[0]/self.frameAmt,self.sprite.get_size()[1])
        drawSprite = pygame.transform.scale(pygame.transform.rotate(frameSprite,self.r),(abs(self.w),abs(self.h)))
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
            pygame.draw.circle(WINDOW,pygame.Color(255,150,255),(self.x-40-self.w/2+camera[0],self.y-self.cFrame*10+camera[1]),15,6)
            if abs(mouse[0][0]-self.x-camera[0]) < 20 and abs(mouse[0][1]-self.y-camera[1]) < 20:
                if mouse[1][0]:
                    self.positions[frame][0] += mouse[2][0]*1
                    self.positions[frame][1] += mouse[2][1]*1
            if abs(mouse[0][0]-self.x-self.w/2-camera[0]) < 20 and abs(mouse[0][1]-self.y-self.h/2-camera[1]) < 20:
                if mouse[1][0]:
                    self.positions[frame][2] += mouse[2][0]*2
                    self.positions[frame][3] += mouse[2][1]*2
            if abs(mouse[0][0]-self.x+self.r-camera[0]) < 20 and abs(mouse[0][1]-(self.y-self.h/2)-camera[1]) < 20:
                if mouse[1][0]:
                    self.positions[frame][4] -= mouse[2][0]
            if mouseCircleCol(self.x-40-self.w/2+camera[0],self.y-self.cFrame*10+camera[1],15,mouse) and mouse[1][0]:
                if self.uiStuff[0] == 3.14:
                    self.uiStuff[0] = mouse[0][1]
                if abs(mouse[0][1]-self.uiStuff[0]) > 5:
                    if mouse[0][1]-self.uiStuff[0] > 0:
                        self.positions[frame][5] -= 1
                    else:
                        self.positions[frame][5] += 1
                    self.uiStuff[0] = mouse[0][1]
                if self.positions[frame][5] < 0:
                    self.positions[frame][5] += 1
                elif self.positions[frame][5] >= self.frameAmt:
                    self.positions[frame][5] -= 1
            else:
                self.uiStuff[0] = 3.14
    
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
                                        self.positions[subject][5]])

def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return

def mouseCircleCol(x,y,r,mouse):
    if abs(mouse[0][0] - x) < r and abs(mouse[0][1] - y) < r:
        return True
    return False