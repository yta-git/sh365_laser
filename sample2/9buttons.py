import laserpointer

class Test(laserpointer.LaserPoint):

    def show(self):
        for i in range(9):
            if i in (3, 6, 9):
                    print()
            print(['X', 'O'][self.buttons[i]], end='\t')
        print('\n\n##########')

    def setup(self):
        for i in range(9):
            self.make_circle_button(str(i))

        self.make_gesture('全てXのジェスチャを検知した', '01010')
        self.buttons = [False] * 9
        self.show()
            
    def program(self):
        tmp = self.get_circle_buttons()
        if tmp is not None:
            print('\7')
            print('selected:', tmp)

            for i in tmp:
                self.buttons[int(i)] = not self.buttons[int(i)]
            self.show()

        tmp = self.get_gesture()
        if tmp is not None:
            print('\7')
            print(tmp)
            self.buttons = [False] * 9
            self.show()
        
Test(camera_num=1, show_img=True, show_log=False).run()