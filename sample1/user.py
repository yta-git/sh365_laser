import pointtest
import serial
import pyautogui as pag


class Test(pointtest.Point):
    def setup(self):
     #   self.ser = serial.Serial("/dev/tty.usbmodemFA131", 9600, timeout=1)
        # self.make_button()
        pass

    def program(self):

        x, y = self.get_point()

        print(x, y)

        if x is False:
            return

        if self.slide_left(x):
            pag.typewrite(['right'])

        if self.slide_right(x):
            pag.typewrite(['right'])

        # if self.button_selected():
        #     print("button selected")

    def closing(self):
        return
        self.ser.close()


Test(camera_num=1, show_img=True, show_log=False).run()
