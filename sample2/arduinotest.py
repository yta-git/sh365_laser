
import laserpointer
import serial
from time import sleep

class Test(laserpointer.LaserPoint):

    def setup(self):

        self.ser = serial.Serial('/dev/cu.usbmodem144401', 9600, timeout=1)
        
        self.make_gesture('l', '01')
        self.make_gesture('l', '23')

        self.make_gesture('r', '10')
        self.make_gesture('r', '32')

        self.make_gesture('d', '20')
        self.make_gesture('d', '31')

        self.make_gesture('u', '02')
        self.make_gesture('u', '13')

                
    def program(self):
 
        tmp = self.get_gesture()
        if tmp is not None:
            print('\7')
            print(tmp)
            self.ser.write(bytes(tmp, 'utf-8'))
            sleep(0.3)
            

    def closing(self):
        self.ser.close()
        
        
Test(camera_num=1, show_img=True, show_log=False).run()
