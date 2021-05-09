import laserpointer

class Test(laserpointer.LaserPoint):

    def setup(self):
        self.make_gesture('コ', '0132')
        self.make_gesture('ギザギザ', '01010')
        self.make_gesture('→', '01')
        self.make_gesture('→', '23')
        self.make_gesture('←', '10')
        self.make_gesture('←', '32')
            
    def program(self):
      
        tmp = self.get_gesture()
        if tmp is not None:
            print('\7')
            print(tmp)
        
Test(camera_num=1, show_img=True, show_log=False).run()