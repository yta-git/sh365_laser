import cv2
from sys import exit
import numpy as np
import serial

from time import time

class LaserPoint:
    def __init__(self, camera_num=0, pointer_serial=None, show_img=False, show_log=False):
        try:
            self.camera = cv2.VideoCapture(camera_num)
            if self.camera is None:
                print('Camera Error')
                exit(1)
        except:
            print('Camera Error')
            exit(1)

        self.pointer = None

        if pointer_serial:
            try:
                self.pointer = serial.Serial(pointer_serial[0], pointer_serial[1])
                print('using', pointer_serial[0])
            except:
                print('Pointer Serial Error')
                print('Nomal mode')
                self.pointer = None

        
        self.height, self.width = self.camera.read()[1].shape[:2]

        print(self.height, self.width)

        self.thereshold = 760

        self.frame_point_x = None
        self.frame_point_y = None

        self.show_img = show_img
        self.show_log = show_log

        self.corners = [[0, 0], [self.width, 0], [
            0, self.height], [self.width, self.height]]
        self.perspective_matrix = None

        self.areaW, self.areaH = self.width, self.height

        self.gestures = {}
        self.drawing = False
        self.area_history = []
        self.show_history = False

        self.hold_buttons = []
        self.hold_button_name = None
        self.hold_counter = 0

        self.circle_buttons = []
        self.old_point_x = None
        self.old_point_y = None

        self.safe_time = 10
        self.frame_safe_f = None
        self.safe_counter = 0
        self.pointer_mode = None

        self.filter_dots = []
        

    def set_view(self, check_count=1):
        self.corners = [[0, 0] for _ in range(4)]

        for i in range(4):
            print('### {} ###'.format(i))
            for j in range(check_count):
                while True:
                    self.pointer_comm()
                    # print('mode: ', self.check_pointer_mode(), end=' ')
                    # print('safe: ', self.check_safe())
                    self.set_point()
                    x, y = self.get_point()
                    if cv2.waitKey(1) != -1 and x is not None:
                        break

                self.corners[i][0] += x / check_count
                self.corners[i][1] += y / check_count

        cs = sorted(self.corners)

        l = sorted(cs[:2], key=lambda x: x[1])
        r = sorted(cs[2:], key=lambda x: x[1])

        print(l[0], r[0], l[1], r[1])
        pts1 = np.float32([l[0], r[0], l[1], r[1]])
        pts2 = np.float32(
            [[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]])
        self.areaW, self.areaH = self.width, self.height

        self.perspective_matrix = cv2.getPerspectiveTransform(pts1, pts2)
        cv2.destroyAllWindows()

    def transform(self, img):
        for x, y in self.filter_dots:
            cv2.circle(img, (x, y), 20, (0, 0, 0), -1)


        if self.perspective_matrix is None:
            return img

        return cv2.warpPerspective(img, self.perspective_matrix, (self.areaW, self.areaH))

#####################################################

    def set_point(self):
        img = self.transform(self.camera.read()[1])

        sum_mat = np.sum(np.array(img), axis=2)
        y, x = np.unravel_index(sum_mat.argmax(), sum_mat.shape)

#        print('==== ', sum_mat[y][x], '====')

        if sum_mat[y][x] < self.thereshold:
            if self.show_img:
                img = cv2.resize(img, (self.width // 2, self.height // 2))
                cv2.imshow("image", img)

            self.frame_point_x, self.frame_point_y = None, None
            return

        if self.show_log and self.is_gesture_mode():
            print('log:', x, y)

        if self.show_img:
            if self.is_gesture_mode():
                cv2.line(img, (x, 0), (x, self.height), (0, 0, 55), 2)
                cv2.line(img, (0, y), (self.width, y), (0, 0, 55), 2)
                
                rect_temp = self.get_pointed_area()
                cv2.rectangle(img, (0, 0), (self.width//2 - 2, self.height//2 - 2), [(255, 100, 100), (100, 100, 255)][rect_temp == 0], 4)
                cv2.rectangle(img, (self.width//2 + 2, 0), (self.width, self.height//2 - 2), [(255, 100, 100), (100, 100, 255)][rect_temp == 1], 4)
                cv2.rectangle(img, (0, self.height//2 + 2), (self.width//2 - 2, self.height), [(255, 100, 100), (100, 100, 255)][rect_temp == 2], 4)
                cv2.rectangle(img, (self.width//2 + 2, self.height//2 + 2), (self.width, self.height), [(255, 100, 100), (100, 100, 255)][rect_temp == 3], 4)

                for name, (px, py), l in self.hold_buttons:
                    cv2.circle(img, (px, py), int(l), (0, 255, 0), [4, -1][name == self.hold_button_name])

                for name, (px, py), l in self.circle_buttons:
                    cv2.circle(img, (px, py), 10, (0, 255, 0), -1)


            img = cv2.resize(img, (self.width // 2, self.height // 2))
            cv2.imshow("image", img)

        # if not self.is_gesture_mode():
        #     self.frame_point_x, self.frame_point_y = None, None
        #     return

        self.frame_point_x, self.frame_point_y = x, y

    def get_point(self, force=False):
        if not self.is_gesture_mode() and not force:
            return None, None

        return self.frame_point_x, self.frame_point_y


#####################################################

    def make_gesture(self, name, command, show_history=False):
        self.gestures[command] = name
        self.show_history = show_history

    def get_pointed_area(self):

        if not self.is_gesture_mode():
            return None

        x, y = self.get_point()

        if x is None:
            return None

        if x < self.areaW / 2:
            if y < self.areaH / 2:
                # print('hirari ue')
                return 0
            else:
                # print('hidari sita')
                return 2
        else:
            if y < self.areaH / 2:
                # print('migi ue')
                return 1
            else:
                # print('migi sita')
                return 3

    def get_gesture(self):

        area = self.get_pointed_area()

        if area is None:
            tmp = self.gestures.get(''.join(map(str, self.area_history)), None)
            self.area_history.clear()
            return tmp

        if(not len(self.area_history) or self.area_history[-1] != area):
            self.area_history.append(self.get_pointed_area())

        if self.show_history:
            print('hist:', self.area_history)

        return None

#####################################################

    def make_hold_button(self, name):
        print('hold_button({})の中心の座標を指定してキーを押す'.format(name))
        while True:
            self.pointer_comm()
            self.set_point()
            x, y = self.get_point()

            if cv2.waitKey(1) != -1 and x is not None:
                break

        print('中心からの距離を指定してキーを押す')
        while True:
            self.pointer_comm()
            self.set_point()
            x2, y2 = self.get_point()

            if cv2.waitKey(1) != -1 and x2 is not None:
                break

        self.hold_buttons.append((name, (x, y), np.hypot(x - x2, y - y2)))
    
    def get_hold_button(self):

        if not self.is_gesture_mode():
            self.hold_button_name = None
            return None

        x, y = self.get_point()
        if x is None:
            self.hold_button_name = None
            return None

        for name, (x2, y2), l in self.hold_buttons:
            if np.hypot(x - x2, y - y2) <= l:
                if self.hold_button_name == name:
                    self.hold_counter += 1

                    if self.hold_counter > 15:
                        self.hold_button_name = None
                        self.hold_counter = 0
                        return name

                else:
                    self.hold_button_name = name
                    self.hold_counter = 0

                break
        
        return None

#####################################################
    def make_circle_button(self, name):
        print('circle_button({})の座標を指定してキーを押す'.format(name))
        while True:
            self.pointer_comm()
            self.set_point()
            x, y = self.get_point()

            if cv2.waitKey(1) != -1 and x is not None:
                break
                
        self.circle_buttons.append([name, (x, y), [False, False, False, False]])

    def get_circle_buttons(self):

        x, y = self.get_point()

        # print(self.circle_buttons)

        if x is None:


            tmp = []
            
            for name, t, l in self.circle_buttons:
                if sum(l) >= 3:
                    tmp.append(name)
            
            self.circle_buttons = list(map(lambda a: [a[0], a[1], [False, False, False, False]], self.circle_buttons))
            self.old_point_x, self.old_point_y = None, None

            if tmp == []:
                return None

            return tmp


        if self.old_point_x is None:
            self.old_point_x, self.old_point_y = x, y
            return None


        for i, l in enumerate(self.circle_buttons):
            px = l[1][0]
            py = l[1][1]

            if self.old_point_y < py < y or y < py < self.old_point_y:
                if px < x:
                    self.circle_buttons[i][2][0] = not self.circle_buttons[i][2][0]
                elif x < px:
                    self.circle_buttons[i][2][2] = not self.circle_buttons[i][2][2]

            if self.old_point_x < px < x or x < px < self.old_point_x:
                if y < py:
                    self.circle_buttons[i][2][1] = not self.circle_buttons[i][2][1]
                
                elif py < y:
                    self.circle_buttons[i][2][3] = not self.circle_buttons[i][2][3]
        

        self.old_point_x, self.old_point_y = x, y

        return None


#####################################################

    def set_safe_time(self, count):
        self.safe_time = count
    
    def set_safe_f(self):
        if self.check_pointer_mode() == 'x':
            self.safe_counter = 0;
            self.frame_safe_f = True
            return
        
        elif self.get_point(True)[0] is not None:
            self.safe_counter = 0;
            self.frame_safe_f = True
            return

        if self.safe_counter > self.safe_time:
            if self.safe_counter == self.safe_time + 1:
                print('レーザーの指している方向が危険です．\n強制的にレーザー出力を停止します．')
                self.safe_counter =+ 1
            self.frame_safe_f = False
            return

        self.safe_counter += 1
        
    def check_safe(self):
        if self.pointer is None:
            return True

        return self.frame_safe_f

    def set_mode(self):
        try:
            self.pointer_mode = self.pointer.read(self.pointer.inWaiting()).decode()[-1]
        except:
            self.pointer_mode = 'x'

    def check_pointer_mode(self):
        if self.pointer is None:
            return 'g'
        
        return self.pointer_mode

    def is_gesture_mode(self):
        if self.check_pointer_mode() == 'g':
            return True
        
        return False


    def pointer_comm(self):
        if self.pointer is None:
            return
        
        self.set_mode()
        self.set_safe_f()

        if self.check_safe():
            self.pointer.write(b'O')
        else:
            self.pointer.write(b'X')

#####################################################

    def filter(self):
        
        tmp = self.thereshold
        self.thereshold *= 0.98

        while True:
            self.set_point()
            x, y = self.get_point(True)
            if x is None:
                print(self.filter_dots)
                self.thereshold = tmp
                return
            
            self.filter_dots.append((x, y))

    def setup(self):
        pass

    def program(self):
        pass

    def closing(self):
        pass

    def run(self):

        print('位置を決めてキーを押す')
        while True:
            self.set_point()
            if cv2.waitKey(1) != -1:
                break

        print('眩しいところを隠しています.')
        
        self.filter()

        print('認識するエリアを選択してキーを押す')
        self.set_view()
        self.setup()

        print('setting ok')

        while True:

            self.set_point()
            
            self.pointer_comm()

            self.program()

            if cv2.waitKey(1) == 27:
                break

        self.closing()

        self.camera.release()
