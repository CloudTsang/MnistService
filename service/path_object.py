import cv2
import numpy as np
import json


class PathObject:
    def __init__(self):
        self.min_x = -1
        self.min_y = -1
        self.max_x = -1
        self.max_y = -1
        self.paths = []
        self.mnist_result = ""
        self.start_point = None
        self.end_point = None
        self.checked5 = False
        self.checked8 = False
        self.checkedGe = False
        self.added_pobjs = []

    def add_path(self, path):
        for x, y in path:
            self.min_x = x if self.min_x == -1 else min(x, self.min_x)
            self.min_y = y if self.min_y == -1 else min(y, self.min_y)
            self.max_x = x if self.max_x == -1 else max(x, self.max_x)
            self.max_y = y if self.max_y == -1 else max(y, self.max_y)
        self.paths.append(path)

    def add_paths(self, path_obj, keep_obj=False):
        if keep_obj:
            if len(self.added_pobjs) == 0:
                p = PathObject()
                p.add_paths(self)
                self.added_pobjs.append(p)
            self.added_pobjs.append(path_obj)
        self.paths += path_obj.paths
        self.min_x = path_obj.min_x if self.min_x == -1 else min(path_obj.min_x, self.min_x)
        self.min_y = path_obj.min_y if self.min_y == -1 else min(path_obj.min_y, self.min_y)
        self.max_x = path_obj.max_x if self.max_x == -1 else max(path_obj.max_x, self.max_x)
        self.max_y = path_obj.max_y if self.max_y == -1 else max(path_obj.max_y, self.max_y)

    def check_contain(self, pobj):
        # self.print_position()
        # pobj.print_position()
        if pobj.min_x > self.min_x and pobj.max_x < self.max_x:
            return True
        if self.min_x > pobj.min_x and self.max_x < pobj.max_x:
            return True
        return False

    def check_dot(self, pobj):
        return self.max_y - self.min_y < (pobj.max_y - pobj.min_y)/3 and self.min_y > pobj.min_y+(pobj.max_y-pobj.min_y)/2

    def check5(self,pobj):
        minx = pobj.min_x
        miny = pobj.min_y
        maxx = pobj.max_x
        maxy = pobj.max_y
        judge5 = (miny<self.min_y + self.max_y - self.min_y/4) and ((maxy-miny)<(self.max_y-self.min_y)/4);
        if minx > self.min_x:
            judge5 = judge5 and (minx-self.max_x) < (maxx-minx)
        else:
            judge5 = judge5 and minx < self.max_x and maxy < self.max_y
        return judge5

    def check_chn8(self,pobj):
        if len(self.paths) > 1 or len(pobj.paths) > 1:
            return False
        if self.min_x < pobj.min_x:
            left_obj = self
            right_obj = pobj
        else:
            left_obj = pobj
            right_obj = self
        if left_obj.start_point[0] < left_obj.end_point[0] or left_obj.start_point[1] > left_obj.end_point[1]:
            return False
        if right_obj.start_point[0] > right_obj.end_point[0] or right_obj.start_point[1] > right_obj.end_point[1]:
            return False
        if right_obj.start_point[0] - left_obj.start_point[0] < right_obj.end_point[0] - left_obj.end_point[0]:
            return True
        return False

    def check_cross(self, pobj):
        check1 = pobj.max_x > self.min_x and pobj.min_x < self.max_x
        if not check1:
            return False
        cross_part = (self.max_x - pobj.min_x)*3
        check2 = cross_part > pobj.max_x - pobj.min_x or cross_part > self.max_x-self.min_x
        return check2

    def check_fraction(self):
        if len(self.paths) < 3:
            return None
        bounds = []
        cur_fraction_line_len = 0
        fraction_line_rect = None
        fraction_line_index = -1
        # print(self.min_y + (self.max_y - self.min_y) * 0.3, self.min_y + (self.max_y - self.min_y) * 0.7,
        #       (self.max_x - self.min_x) * 0.8)
        for i, line in enumerate(self.paths):
            np_line = np.array(line)
            rf0 = cv2.boundingRect(np_line)
            rf = [rf0[0], rf0[1], rf0[0]+rf0[2], rf0[1]+rf0[3]]
            if rf[3] - rf[1] >= (self.max_y - self.min_y)*0.7:
                bounds.append(rf)
                continue
            # print(rf)
            if rf[1] > self.min_y+(self.max_y-self.min_y)*0.3 and \
                rf[3]<self.min_y+(self.max_y-self.min_y)*0.7 and \
                rf[2]-rf[0] >= (self.max_x-self.min_x)*0.8 and \
                rf[2]-rf[0] > cur_fraction_line_len:
                cur_fraction_line_len = rf[2]-rf[0]
                fraction_line_index = i
                fraction_line_rect = rf
            bounds.append(rf)
        if fraction_line_rect is None:
            print("fraction line not found")
            return None
        # print(fraction_line_rect)
        up = []
        down = []
        upword = False
        downword = False
        for i, rf in enumerate(bounds):
            if i == fraction_line_index:
                continue
            center_y = rf[1] + (rf[3]-rf[1])/2
            if center_y < fraction_line_rect[1]:
                p = self.paths[i]
                obj = PathObject()
                obj.add_path(p)
                up.append(obj)
                if upword is False and rf[3]-rf[1]>=(self.max_y-self.min_y)*0.2:
                    upword = True
            elif center_y > fraction_line_rect[3]:
                p = self.paths[i]
                obj = PathObject()
                obj.add_path(p)
                down.append(obj)
                # print("down", rf, self.max_y, self.min_y)
                if downword is False and rf[3]-rf[1]>=(self.max_y-self.min_y)*0.2:
                    downword = True

        if upword is False or downword is False:
            # print("upword=",upword,"  downword=",downword)
            return None
        return [up, down]

    def draw(self, size_w, size_h, border=1, thickness=2):
        scale_w = size_w * border / ((self.max_x - self.min_x)+1)
        scale_y = size_h * border / ((self.max_y - self.min_y)+1)
        scale = min(scale_w, scale_y)

        offset_x = (size_w - (self.max_x - self.min_x) * scale) / 2
        offset_y = (size_h - (self.max_y - self.min_y) * scale) / 2
        start_x = self.min_x * scale
        start_y = self.min_y * scale

        base = np.zeros((int(size_h), int(size_w)), np.uint8)
        base[:, :] = 255

        for i, line in enumerate(self.paths):
            for j, point in enumerate(line):
                x1, y1 = np.array(point) * scale
                if j < len(line) - 1:
                    x2, y2 = np.array(line[j + 1]) * scale
                else:
                    break
                x1 += -start_x + offset_x
                x2 += -start_x + offset_x
                y1 += -start_y + offset_y
                y2 += -start_y + offset_y
                cv2.line(base, (int(x1), int(y1)), (int(x2), int(y2)), 0, thickness)
        # cv2.imshow('base', base)
        # cv2.waitKey()
        return base

    def print_position(self):
        print((self.min_x, self.min_y), (self.max_x, self.max_y))


def get_path_objects(paths):
    pObjs = []
    for path in paths:
        pobj = PathObject()
        pobj.start_point = path[0]
        pobj.end_point = path[-1]
        pobj.add_path(path)
        pObjs.append(pobj)
    pObjs.sort(key=lambda x: x.min_x)
    return pObjs


if __name__ == "__main__":
    line = [[1,1],[2,2],[3,3]]
    line = np.array(line)
    r = cv2.boundingRect(line)
    print(r)

    # paths_str = "[[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]"
    # paths = json.loads(paths_str)
    # pobj = PathObject()
    # for path in paths:
    #     pobj.add_path(path)
    # cv2img = pobj.draw(pobj.max_x-pobj.min_x, pobj.max_y-pobj.min_y)
    # cv2.imshow("im", cv2img)
    # cv2.waitKey()

