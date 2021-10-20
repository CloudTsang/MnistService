import cv2
import numpy as np

class PathObject:
    def __init__(self):
        self.min_x = -1
        self.min_y = -1
        self.max_x = -1
        self.max_y = -1
        self.paths = []

    def add_path(self, path):
        for x, y in path:
            self.min_x = x if self.min_x == -1 else min(x, self.min_x)
            self.min_y = y if self.min_y == -1 else min(y, self.min_y)
            self.max_x = x if self.max_x == -1 else max(x, self.max_x)
            self.max_y = y if self.max_y == -1 else max(y, self.max_y)
        self.paths.append(path)

    def add_paths(self, path_obj):
        self.paths += path_obj.paths
        self.min_x = path_obj.min_x if self.min_x == -1 else min(path_obj.min_x, self.min_x)
        self.min_y = path_obj.min_y if self.min_y == -1 else min(path_obj.min_y, self.min_y)
        self.max_x = path_obj.max_x if self.max_x == -1 else max(path_obj.max_x, self.max_x)
        self.max_y = path_obj.max_y if self.max_y == -1 else max(path_obj.max_y, self.max_y)

    def check_connect(self, min_x, min_y, max_x, max_y):
        a = min_x < self.max_x and max_x > self.min_x
        b = max_x < self.min_x
        return a or b

    def draw(self, img_size):
        scale_w = img_size * 0.9 / (self.max_x - self.min_x)
        scale_y = img_size * 0.9 / (self.max_y - self.min_y)
        scale = min(scale_w, scale_y)

        offset_x = (img_size - (self.max_x - self.min_x) * scale) / 2
        offset_y = (img_size - (self.max_y - self.min_y) * scale) / 2
        start_x = self.min_x * scale
        start_y = self.min_y * scale

        base = np.zeros((img_size, img_size), np.uint8)
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

                cv2.line(base, (int(x1), int(y1)), (int(x2), int(y2)), 0, 2)

        return base

