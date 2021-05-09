import laserpointer
import pygame
from pygame.locals import *
import sys
from random import randint

class Sakana():
    def __init__(self):
        self.x = 0
        self.y = randint(0, 960)

    def update(self):
#        print(self.x, self.y)
        self.x += 10
        
        if self.x > 1350:
            return False

        return True

class Test(laserpointer.LaserPoint):

    def setup(self):

        self.w = 1280
        self.h = 960

        self.x = 1000
        self.y = 400

        pygame.init()

        self.creen = pygame.display.set_mode((self.w, self.h), FULLSCREEN)  # 画面設定
        self.screen = pygame.display.get_surface()
        self.player = pygame.image.load("player.png").convert_alpha()    # プレイヤー画像の取得
        self.sakana = pygame.image.load("sakana.png").convert_alpha()    # プレイヤー画像の取得
        self.bg = pygame.image.load("bg.jpg").convert_alpha()
        self.rect_bg = self.bg.get_rect()
        self.list = []
        self.font = pygame.font.Font(None, 200)
        self.text = self.font.render('GAME OVER', True, (255, 255, 255))
        
        self.font2 = pygame.font.Font(None, 100)
        
        self.gameover = False
        
        self.score = 0
            
    def program(self):

        pygame.display.update()             # 画面更新

        if self.gameover:

            for i in self.list:
                self.screen.blit(self.sakana, (i.x, i.y))

            self.screen.blit(self.text, [320, 200])
            self.screen.blit(self.text2, [100, 50])
            
            pygame.display.update()             # 画面更新
                        
            for event in pygame.event.get():
                if event.type == QUIT:          # 閉じるボタンが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:       # キーを押したとき
                    if event.key == K_ESCAPE:   # Escキーが押されたとき
                        pygame.quit()
                        sys.exit()

            return


        if randint(0, 100) < 10:
            self.list.append(Sakana())

        tmp = [x for x in self.list if x.update()]
        self.list = tmp
        
#        pygame.time.wait(1)                # 更新時間間隔
        self.screen.fill((0, 20, 0, 0))          # 画面の背景色
        self.screen.blit(self.bg, self.rect_bg)

        for i in self.list:
            self.screen.blit(self.sakana, (i.x, i.y))
            if ((i.x - self.x) ** 2 + (i.y - self.y) ** 2) ** 0.5 < 50:
                self.screen.blit(self.text, [320, 200])
                pygame.display.update()
                self.gameover = True
                break
            
        self.screen.blit(self.player, (self.x, self.y))    # プレイヤー画像の描画

        self.text2 = self.font2.render('SCORE: ' + str(self.score), True, (255, 255, 255))
        self.score += 1

        self.screen.blit(self.text2, [100, 50])

        if self.get_point()[0]:
            self.x, self.y = self.get_point()# event.pos
            self.x -= self.player.get_width() / 2
            self.y -= self.player.get_height() / 2
        
Test(camera_num=1, show_img=True, show_log=False).run()
