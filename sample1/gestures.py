import new

class Test(new.LaserPoint):

    def setup(self):
        
        self.make_gesture('→', '01')
        self.make_gesture('→', '23')

        self.make_gesture('←', '10')
        self.make_gesture('←', '32')

        self.make_gesture('↑', '20')
        self.make_gesture('↑', '31')

        self.make_gesture('↓', '02')
        self.make_gesture('↓', '13')

        self.make_gesture('右回りの円', '01320')
        self.make_gesture('右回りの円', '13201')
        self.make_gesture('右回りの円', '32013')
        self.make_gesture('右回りの円', '20132')
        
        self.make_gesture('左回りの円', '02310')
        self.make_gesture('左回りの円', '10231')
        self.make_gesture('左回りの円', '31023')
        self.make_gesture('左回りの円', '23102')

        self.make_gesture('コ', '0132')
        self.make_gesture('C', '1023')

        self.make_gesture('ギザギザ', '01010')
        self.make_gesture('ギザギザ', '23232')
                
    def program(self):
 
        tmp = self.get_gesture()
        if tmp is not None:
            print('\7')
            print(tmp)
        
Test(camera_num=1, show_img=True, show_log=False).run()