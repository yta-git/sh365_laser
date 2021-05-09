import laserpointer
from subprocess import call

class Test(laserpointer.LaserPoint):

    def setup(self):
        self.make_hold_button('python2 irmcli/irmcli.py -p -f irmcli/on_off.json')
    
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/head.json', '01010')
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/head.json', '23232')        
    
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/l.json', '20')
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/l.json', '31')
    
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/m.json', '01')
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/m.json', '23')
        
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/s.json', '02')
        self.make_gesture('python2 irmcli/irmcli.py -p -f irmcli/s.json', '13')

    def program(self):
        tmp = self.get_hold_button()
        if tmp is not None:
            print('\7')
            call(tmp.split())

        tmp = self.get_gesture()
        if tmp is not None:
            print('\7')
            call(tmp.split())

Test(camera_num=1, show_img=True, show_log=False).run()