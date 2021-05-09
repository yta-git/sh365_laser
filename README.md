# sh365_laser
「レーザーポインタで家電を操作するシステムとセキュリティ対策について」

sechack365 2017 で作成しました．

[ポスター](/sechack3v4.pdf)

[youtube説明動画](https://www.youtube.com/watch?v=jSZt6sEBAZs)

[利用例(LED操作)](https://www.youtube.com/watch?v=k3hNK1m2LFg)

[利用例(ゲーム)](https://www.youtube.com/watch?v=fRyMS6CUI3Y)

## 利用例
```python

import laserpointer

class Test(laserpointer.LaserPoint):

    def setup(self):
        self.make_gesture('Cの形のジェスチャが認識されました．', '1023')
        self.make_gesture('ギザギザのジェスチャが認識されました', '01010')
        self.make_hold_button('ボタンが選択されました．')
        self.make_circle_button('ボタン1が囲まれました．')
        self.make_circle_button('ボタン2が囲まれました．')
        self.make_circle_button('ボタン3が囲まれました．')

    def program(self):

        tmp = self.get_gesture()
        if tmp:
            print('\7')
            print(tmp)
            return

        tmp = self.get_hold_button()
        if tmp:
            print('\7')
            print(tmp)
            return
    
        tmp = self.get_circle_buttons()
        if tmp:
            print('\7')
            print(tmp)
            return

Test(camera_num=1 ,show_img=True, show_log=False).run()
```


