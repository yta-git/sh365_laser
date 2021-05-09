import cv2
from sys import exit
import numpy as np
import serial


class LaserPoint:
    def __init__(self, camera_num=0, pointer_serial=None, show_img=False, show_log=False):
        try:
            self.camera = cv2.VideoCapture(camera_num)
        except:
            print('Camera Error')
            exit(1)

        if pointer_serial:
            try:
                self.pointer = serial.Serial(pointer_serial[0], pointer_serial[1])
            except:
                print('Pointer Serial Error')
                print('Nomal mode')
                self.pointer = None

        self.height, self.width = self.camera.read()[1].shape[:2]

        print(self.height, self.width)

        self.frame_point_x = None
        self.frame_point_y = None

        self.show_img = show_img
        self.show_log = show_log

        self.corners = [[0, 0], [self.width, 0], [
            0, self.height], [self.width, self.height]]
        self.perspective_matrix = None
        self.areaH = None
        self.areaW = None

        self.gestures = {}
        self.drawing = False
        self.area_history = []
        self.show_history = False

        self.safe_time = 100
        self.frame_safe_f = None
        self.safe_counter = 0
        self.gesture_mode = None

    def set_view(self, check_count=1):
        self.corners = [[0, 0] for _ in range(4)]

        for i in range(4):
            print('### {} ###'.format(i))
            for j in range(check_count):
                while True:
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
        if self.perspective_matrix is None:
            return img

        return cv2.warpPerspective(img, self.perspective_matrix, (self.areaW, self.areaH))

    def set_point(self):
        img = self.transform(self.camera.read()[1])

        sum_mat = np.sum(np.array(img), axis=2)
        y, x = np.unravel_index(sum_mat.argmax(), sum_mat.shape)

        if sum_mat[y][x] < 700:
            if self.show_img:
                img = cv2.resize(img, (self.width // 2, self.height // 2))
                cv2.imshow("image", img)

            self.frame_point_x, self.frame_point_y = None, None
            return

        if self.show_log:
            print('log:', x, y)

        if self.show_img:
            cv2.line(img, (x, 0), (x, self.height), (0, 0, 55), 2)
            cv2.line(img, (0, y), (self.width, y), (0, 0, 55), 2)
            # img = img[:self.areaH, :self.areaW]
            img = cv2.resize(img, (self.width // 2, self.height // 2))
            cv2.imshow("image", img)

        self.frame_point_x, self.frame_point_y = x, y

    def get_point(self):
        return self.frame_point_x, self.frame_point_y

    def make_gesture(self, name, command, show_history=False):
        self.gestures[command] = name
        self.show_history = show_history

    def get_pointed_area(self):
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

    def set_safe_time(self, count):
        self.safe_time = count
    
    def set_frame_safe_f(self):
        pass
        
    def check_safe(self):
        return self.frame_safe_f

    def set_frame_gesture_mode(self):
        pass
    
    def check_gesture_mode(self):
        pass


    def setup(self):
        pass

    def program(self):
        pass

    def closing(self):
        pass

    def run(self):
        self.set_view()
        self.setup()

        while True:
            self.set_point()

            self.program()

            if cv2.waitKey(1) == 27:
                break

        self.closing()

        self.camera.release()
