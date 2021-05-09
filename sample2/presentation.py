import new
import pyautogui as pag

class Test(new.LaserPoint):

    def setup(self):
        self.make_gesture('R', '01')
        self.make_gesture('R', '03')
        self.make_gesture('R', '21')
        self.make_gesture('R', '23')

        self.make_gesture('L', '10')
        self.make_gesture('L', '12')
        self.make_gesture('L', '30')
        self.make_gesture('L', '32')
        
    def program(self):
        tmp = self.get_gesture()

        if tmp is not None:

            if tmp == 'R':
                print('\7')
                pag.press('right')
            
            elif tmp == 'L':
                print('\7')
                pag.press('left')

Test(camera_num=1, pointer_serial=('/dev/tty.SH365Laser-DevB', 9600) ,show_img=True, show_log=False).run()

