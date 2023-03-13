import pygame
import os
import Objects.circle as circle
import Objects.sprite as sprite
import Objects.spritesheet as spritesheet
import Objects.text as text
import testProject.data as data    
from datetime import datetime
import random
import tkinter
from tkinter import filedialog
import easygui

WINDOW_W, WINDOW_H = 1280,720

WINDOW = pygame.display.set_mode((WINDOW_W,WINDOW_H))

FPS = 24

objs = data.objs

pygame.font.init()

bigFont = pygame.font.Font('Dosis-ExtraBold.ttf',60)
midFont = pygame.font.Font('Dosis-ExtraBold.ttf',40)
smallFont = pygame.font.Font('Dosis-ExtraBold.ttf',20)

def toggle(bool):
    if bool:
        return False
    else:
        return True

def ui():
    pass

def mouse_col(x,y,w,h,mouse):
    if mouse[0][0] > x and mouse[0][0] < x+w and mouse[0][1] > y and mouse[0][1] < y+h:
        return True
    return False

def main():
    animRun = True
    clock = pygame.time.Clock()
    frame = 0
    mouse = [pygame.mouse.get_pos(),pygame.mouse.get_pressed()]
    frameZoom = 30
    onionSkin = True
    play = False
    alt = False
    camera = [0,0]
    frameRate = 0
    if len(objs) < 1:
        objs.append(circle.circle([[-300,-300,100,100,0]]))
    while animRun:
        now = datetime.now()
        if play:
            clock.tick(FPS)

        alt = toggle(alt)
        op = mouse[1][0]
        mouse = [pygame.mouse.get_pos(),[False,False,False],pygame.mouse.get_rel(),False]
        mouse[1][0] = pygame.mouse.get_pressed()[0]
        mouse[1][1] = pygame.mouse.get_pressed()[1]
        mouse[1][2] = pygame.mouse.get_pressed()[2]
        
        if mouse[1][0] and mouse[1][0] != op:
            mouse[3] = True
        else:
            mouse[3] = False

        WINDOW.fill((0,0,0))
        
        for i in objs:
            if onionSkin and not play:
                i.update(WINDOW,frame+1,[0.5,0.25,0.25,100],camera)
                i.update(WINDOW,frame-1,[0.25,0.5,0.25,100],camera)

        switch = False
        if mouse[0][1] < 30 and mouse[1][0]:
            mouse[1][0] = False
            switch = True
        for i in objs:
            i.update(WINDOW,frame,[1,1,1,255],camera)
            i.edit(frame,mouse,WINDOW,play,camera)
        if switch:
            mouse[1][0] = True

        if not play:
            pygame.draw.rect(WINDOW,(100,100,255),(0+camera[0],0+camera[1],1280,720),3)
            for i in range(240):
                if i%24 == 0:
                    pygame.draw.line(WINDOW,(150,150,255),(i*frameZoom,0),(i*frameZoom,30),3)
                elif i%12 == 0:
                    pygame.draw.line(WINDOW,(150,150,255),(i*frameZoom,0),(i*frameZoom,20))
                elif i%6 == 0:
                    pygame.draw.line(WINDOW,(150,150,255),(i*frameZoom,0),(i*frameZoom,15))
                elif i%3 == 0:
                    pygame.draw.line(WINDOW,(150,150,255),(i*frameZoom,0),(i*frameZoom,12))
                else:
                    pygame.draw.line(WINDOW,(150,150,255),(i*frameZoom,0),(i*frameZoom,6))
            pygame.draw.line(WINDOW,(255,255,255),(frame*frameZoom,0),(frame*frameZoom,15),3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    frame += 1
                if event.key == pygame.K_LEFT:
                    frame -= 1
                if event.key == pygame.K_o:
                    onionSkin = toggle(onionSkin)
                if event.key == pygame.K_SPACE:
                    play = toggle(play)
                if event.key == pygame.K_ESCAPE:
                    frame = 0
                    camera = [0,0]
                    frameZoom = 30
                if event.key == pygame.K_BACKSPACE:
                    for i in objs:
                        i.deleteFrame(frame)
                    frame -= 1
                if event.key == pygame.K_e and 0 == 1:
                    for i in objs:
                        i.extend(frame,frame)
                    frame += 1
                if event.key == pygame.K_TAB:
                    for i in objs:
                        i.copy(frame,frame)
                    frame += 1
                if event.key == pygame.K_s:
                    with open("testProject/data.py", "w") as f:
                        f.write("import Objects.circle as circle\nimport Objects.sprite as sprite\nimport Objects.spritesheet as spritesheet\nimport Objects.text as text\n")
                        f.write("objs = [")
                        for i in objs:
                            if isinstance(i, circle.circle):
                               f.write("circle.circle([")
                            if isinstance(i, text.text):
                               f.write("text.text([")
                            if isinstance(i, sprite.sprite):
                               f.write("sprite.sprite([")
                            if isinstance(i, spritesheet.spritesheet):
                               f.write("spritesheet.spritesheet([")
                            for j in i.positions:
                                f.write(str(j))
                                f.write(",")
                            f.write("],")
                            if isinstance(i, text.text):
                                f.write('"'+str(i.text)+'",(')
                                for j in i.color:
                                   f.write(str(j)+",")
                                f.write(")")
                            if isinstance(i, sprite.sprite):
                               f.write('"'+str(i.spritePath)+'",')
                            if isinstance(i, spritesheet.spritesheet):
                               f.write('"'+str(i.spritePath)+'",')
                               f.write(str(i.frameAmt))
                            f.write("),")
                        f.write("]")
            if event.type == pygame.MOUSEWHEEL:
                frameZoom += event.y
        if play:
            frame += 1
        
        if not play:
            if mouse[1][0] and mouse[0][1] < 30:
                frame = int(mouse[0][0]/frameZoom)
            if mouse[1][1] or mouse[1][2]:
                camera[0] += mouse[2][0]
                camera[1] += mouse[2][1]
            
            pygame.draw.rect(WINDOW,(255,255,255),(1150,400,100,50))
            WINDOW.blit(midFont.render("text",False,(0,0,25)),(1150,400))
            if mouse_col(1150,400,100,50,mouse) and mouse[3]:
                tempText = easygui.enterbox("text displayed in text object:")
                if tempText != None:
                    tempColor = (easygui.enterbox("the red value of the text color (0-255)"),easygui.enterbox("the green value of the text color (0-255)"),easygui.enterbox("the blue value of the text color (0-255)"))
                if tempText != None and tempColor[0] != None and tempColor[1] != None and tempColor[2] != None:
                    if tempColor[0].isnumeric() and tempColor[1].isnumeric() and tempColor[2].isnumeric():
                        tempObj = text.text([[random.randrange(0,WINDOW_W),-200,100,100,0,1]],tempText,(int(tempColor[0]),int(tempColor[1]),int(tempColor[2])))
                        for i in range(len(objs[0].positions)-1):
                            tempObj.copy(0,len(tempObj.positions))
                        objs.append(tempObj)
            
            pygame.draw.rect(WINDOW,(255,255,255),(1150,500,100,50))
            WINDOW.blit(midFont.render("sprite",False,(0,0,25)),(1150,500))
            if mouse_col(1150,500,100,50,mouse) and mouse[3]:
                folder_path = filedialog.askopenfilename()
                if folder_path != '' and folder_path[len(folder_path)-3:] == "png":
                    tempObj = sprite.sprite([[random.randrange(0,WINDOW_W),-200,100,100,0,1]],folder_path)
                    for i in range(len(objs[0].positions)-1):
                        tempObj.copy(0,len(tempObj.positions))
                    objs.append(tempObj)
            
            pygame.draw.rect(WINDOW,(255,255,255),(1150,600,100,50))
            WINDOW.blit(midFont.render("sheet",False,(0,0,25)),(1150,600))
            if mouse_col(1150,600,100,50,mouse) and mouse[3]:
                folder_path = filedialog.askopenfilename()
                if folder_path != '' and folder_path[len(folder_path)-3:] == "png":
                    frameAmt = easygui.enterbox("Number of frames in sprite sheet (must be number)")
                    if frameAmt != None and frameAmt.isnumeric():
                        tempObj = spritesheet.spritesheet([[random.randrange(0,WINDOW_W),-200,100,100,0,1]],folder_path,int(frameAmt))
                        for i in range(len(objs[0].positions)-1):
                            tempObj.copy(0,len(tempObj.positions))
                        objs.append(tempObj)


                
        pygame.display.update()
        if not play:
            if float(str(datetime.now()-now)[5:]) != 0:
                frameRate = 1/float(str(datetime.now()-now)[5:])
            else:
                frameRate = "infinite"
        else:
            frameRate = clock.get_fps()

if __name__ == "__main__":
    main()