import pygame
from pygame.locals import *
import sys
from random import randint

class Sakana():
    def __init__(self):
        self.x = 0
        self.y = randint(0, 900)

    def update(self):
#        print(self.x, self.y)
        self.x += 10
        
        if self.x > 1650:
            return False

        return True
            

def main():
    (w,h) = (1600,900)   # 画面サイズ
    (x,y) = (w/2, h/2)
    pygame.init()       # pygame初期化
    creen = pygame.display.set_mode((w, h), FULLSCREEN)  # 画面設定
    screen = pygame.display.get_surface()
    player = pygame.image.load("player.png").convert_alpha()    # プレイヤー画像の取得
    sakana = pygame.image.load("sakana.png").convert_alpha()    # プレイヤー画像の取得
    bg = pygame.image.load("bg.jpg").convert_alpha()
    rect_bg = bg.get_rect()
    (x, y) = (300, 200)
    list = []
    font = pygame.font.Font(None, 200)
    text = font.render('GAME OVER', True, (255, 255, 255))

    font2 = pygame.font.Font(None, 100)

    gameover = False

    score = 0
    
    while (1):

        pygame.display.update()             # 画面更新

        if gameover:

           # screen.blit(player, (x, y))    # プレイヤー画像の描画
            for i in list:
                screen.blit(sakana, (i.x, i.y))

            screen.blit(text, [360, 200])
            screen.blit(text2, [100, 50])
            
            pygame.display.update()             # 画面更新
            
            
            for event in pygame.event.get():
                if event.type == QUIT:          # 閉じるボタンが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:       # キーを押したとき
                    if event.key == K_ESCAPE:   # Escキーが押されたとき
                        pygame.quit()
                        sys.exit()

            continue


        if randint(0, 100) < 10:
            list.append(Sakana())
#            print('sakana')

        tmp = [x for x in list if x.update()]
        list = tmp
        
        pygame.time.wait(0)                # 更新時間間隔
        screen.fill((0, 20, 0, 0))          # 画面の背景色
        screen.blit(bg, rect_bg)

        for i in list:
            screen.blit(sakana, (i.x, i.y))
            if ((i.x - x) ** 2 + (i.y - y) ** 2) ** 0.5 < 50:
                screen.blit(text, [360, 200])
                pygame.display.update()
                gameover = True
                break
            
        screen.blit(player, (x, y))    # プレイヤー画像の描画

        text2 = font2.render('SCORE: ' + str(score), True, (255, 255, 255))
        score += 1

        screen.blit(text2, [100, 50])
        

        

        for event in pygame.event.get():
            # マウスポインタで画像も移動
            if event.type == MOUSEMOTION:
                x, y = event.pos
                print(x, y)
                x -= player.get_width() / 2
                y -= player.get_height() / 2
            # 終了用のイベント処理
            if event.type == QUIT:          # 閉じるボタンが押されたとき
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
        main()
