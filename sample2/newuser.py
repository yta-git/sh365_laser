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

Test(camera_num=1, pointer_serial=('/dev/tty.SH365Laser-DevB', 9600) ,show_img=True, show_log=False).run()

