import laserpointer

class Test(laserpointer.LaserPoint):

    def setup(self):
        # 初期設定用
        pass

    def program(self):
        # 処理用
        x, y = self.get_point()
        
        if x is not None:
            print(x, y)

    def closing(self):
        # 終了時処理用
        pass

Test(camera_num=1, show_img=True, show_log=False).run()