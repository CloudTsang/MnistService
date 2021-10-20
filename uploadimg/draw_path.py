import cv2
import numpy as np
from path_object import PathObject

img_size = 224
# img_size = 28
small_img_size = 28


def getArea(paths):
    min_x = -1
    min_y = -1
    max_x = -1
    max_y = -1

    for line in paths:
        for x, y in line:
            min_x = x if min_x == -1 else min(min_x, x)
            min_y = y if min_y == -1 else min(min_y, y)
            max_x = x if max_x == -1 else max(max_x, x)
            max_y = y if max_y == -1 else max(max_y, y)
    return int(min_x),int(min_y), int(max_x), int(max_y)


def get_scale(min_x, min_y, max_x, max_y):
    scale_w = img_size * 0.9 / (max_x - min_x)
    scale_y = img_size * 0.9 / (max_y - min_y)
    scale = min(scale_w, scale_y)
    return scale


def draw(paths, server=True):
    min_x, min_y, max_x, max_y = getArea(paths)
    scale = get_scale(min_x, min_y, max_x, max_y)
    offset_x = (img_size - (max_x - min_x)*scale)/2
    offset_y = (img_size - (max_y - min_y)*scale)/2
    start_x = min_x * scale
    start_y = min_y * scale

    base = np.zeros((img_size, img_size), np.uint8)
    base[:, :] = 255

    for i, line in enumerate(paths):
        for j, point in enumerate(line):
            x1, y1 = np.array(point)*scale
            if j < len(line)-1:
                x2, y2 = np.array(line[j+1])*scale
            else:
                break

            x1 += -start_x + offset_x
            x2 += -start_x + offset_x
            y1 += -start_y + offset_y
            y2 += -start_y + offset_y

            cv2.line(base, (int(x1), int(y1)), (int(x2), int(y2)), 0, 2)
    if server is False:
        cv2.imshow('base', base)
        cv2.waitKey()
    return base


def split_draw(paths, server=True):
    path_objects = []
    for line in paths:
        is_add = False
        pobj = PathObject()
        pobj.add_path(line)
        for pobj2 in path_objects:
            # print(pobj.min_x, pobj.min_y, pobj.max_x, pobj.max_y)
            # print(pobj2.min_x, pobj2.min_y, pobj2.max_x, pobj2.max_y)
            if pobj2.check_connect(pobj.min_x, pobj.min_y, pobj.max_x, pobj.max_y):
                pobj2.add_paths(pobj)
                is_add = True
                break
        if is_add is False:
            path_objects.append(pobj)
    path_objects.sort(key=lambda ele:ele.min_x)

    ret_imgs = []
    for pobj in path_objects:
        img = pobj.draw(28)
        ret_imgs.append(img)
        if server is False:
            cv2.imshow('img', img)
            cv2.waitKey()
    return ret_imgs


if __name__ == '__main__':
    # 345
    paths = [[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]
    # draw(paths, server=False)
    split_draw(paths, server=False)
