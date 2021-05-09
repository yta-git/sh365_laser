import pointtest
import serial
import pyautogui as pag


class Test(pointtest.Point):
    def setup(self):
        pass

    def program(self):

        x, y = self.get_point()

        print(x, y)

    def closing(self):
        pass

Test(camera_num=0, show_img=True, show_log=False).run()
