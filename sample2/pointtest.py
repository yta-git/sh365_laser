import cv2
import numpy as np


class Point:
    def __init__(self, camera_num=0, show_img=False, show_log=False):
        self.camera = cv2.VideoCapture(camera_num)
        self.show_img = show_img
        self.show_log = show_log
        self.corners = None
        self.perspective_matrix = None
        self.rects = []
        self.stroke = False
        self.old_x = 0
        self.old_y = 0
        self.height, self.width = self.camera.read()[1].shape[:2]
        self.max_r = 0
        self.max_l = self.width
        self.max_u = self.height
        self.max_d = 0
        self.counterr = 0
        self.counterl = 0

    def set_view(self, check_count=3):
        check_count
        self.corners = [[0, 0], [0, 0], [0, 0], [0, 0]]

        for i in range(4):
            print(['右上', '右下', '左下', '左上'][i])
            for j in range(check_count):
                print('{} / {}'.format(j, check_count))
                while True:
                    x, y = self.get_point()
                    if cv2.waitKey(1) != -1:
                        break

                self.corners[i][0] += x / check_count
                self.corners[i][1] += y / check_count

        original = np.float32(self.corners)
        trans = np.float32([(0, self.height), (self.width, self.height), (self.width, 0), (0, 0)])

        self.perspective_matrix = cv2.getPerspectiveTransform(original, trans)

    def make_button(self, x=None, y=None, check_count=3):
        if y is not None:
            self.rects.append([list(x), list(y)])
            return

        rect_corners = [[0, 0], [0, 0]]

        for i in range(2):
            print(['左上', '右下'][i])
            for j in range(check_count):
                print('{} / {}'.format(j, check_count))
                while True:
                    x, y = self.get_point()
                    if cv2.waitKey(1) != -1:
                        break

                rect_corners[i][0] += x / check_count
                rect_corners[i][1] += y / check_count

            rect_corners[i][0] = int(rect_corners[i][0])
            rect_corners[i][1] = int(rect_corners[i][1])

        self.rects.append(rect_corners)
        print(self.rects)

    def transform(self, img):
        if self.perspective_matrix is not None:
            return cv2.warpPerspective(img, self.perspective_matrix, (self.width, self.height))
        else:
            return img

    def get_point(self):
        img = self.transform(self.camera.read()[1])

        sum_mat = np.sum(np.array(img), axis=2)
        x, y = np.unravel_index(sum_mat.argmax(), sum_mat.shape)

        if self.show_img:
            for rect in self.rects:
                # if self.button_selected(x, y):
                #     cv2.rectangle(img, tuple(rect[0]), tuple(rect[1]), (55, 0, 0), -1)
                # else:
                cv2.rectangle(img, tuple(rect[0]), tuple(rect[1]), (55, 0, 0), 2)

            rect_num = self.button_selected(x, y)
            if rect_num is not False:
                cv2.rectangle(img, tuple(self.rects[rect_num][0]), tuple(self.rects[rect_num][1]), (55, 0, 0), -1)

            cv2.line(img, (y, 0), (y, self.height), (0, 0, 55), 2)
            cv2.line(img, (0, x), (self.width, x), (0, 0, 55), 2)
            img = cv2.resize(img, (self.width // 3, self.height // 3))
            cv2.imshow("img", img)

        if self.show_log:
            print('log:', x, y)

        # self.old_x = x
        # self.old_y = y

        if sum_mat[x][y] > 100:
            self.stroke = True
            self.max_r = max(x, self.max_r)
            self.max_l = min(x, self.max_l)
            self.max_u = min(y, self.max_u)
            self.max_d = max(y, self.max_d)

            return x, y
        else:
            self.max_r = 0
            self.max_l = self.width
            self.max_u = self.height
            self.max_d = 0
            self.stroke = False

            # return False, False
            return x, y

    def button_selected(self, x=None, y=None):

        if y is None:
            x, y = self.get_point()

        for i, rect in enumerate(self.rects):
            if (rect[0][0] < x < rect[1][0]) and (rect[0][1] < y < rect[1][1]):
                return i

        return False

    def button_circled(self):
        if not self.stroke:
            return False

        for i, rect in enumerate(self.rects):
            if self.max_l < rect[0][0] and self.max_u < rect[0][1] and rect[1][0] < self.max_r and rect[1][1] < self.max_d:
                return i

        return False

    def button_hold(self):
        if not self.stroke:
            return False

        rect_num = self.button_selected()

        if rect_num is not False:
            self.counter += 1

            if self.counter > 100:
                return rect_num

        else:
            self.counter = 0

        return False

    def slide_right(self, x):

        if self.old_x < x:
            self.counterr += 1
            print('right', self.counterr)

            if self.counterr >= 10:
                print('rright')
                self.counterr = 0
                self.old_x = x
                return True

        else:
            self.counterr = 0
        self.old_x = x
        #self.counterr = 0
        return False

    def slide_left(self, x):

        if self.old_x > x:
            self.counterl += 1
            print('left', self.counterl)

            if self.counterl >= 10:
                print('lleft')
                self.counterl = 0
                self.old_x = x
                return True

        else:
            self.counterl = 0
        self.old_x = x
        return False

    def setup(self):
        pass

    def program(self):
        pass

    def closing(self):
        pass

    def run(self):
        # self.set_view()

        self.setup()

        while True:
            self.program()

            if cv2.waitKey(1) == 27:
                break

        self.closing()

