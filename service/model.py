import numpy as np
import keras.backend as K
from keras.models import load_model
import cv2
from array import *
import json
from path_object import PathObject
from const import IMG_SIZE
import tensorflow as tf


def get_labels(txt):
    # 获取labels
    label = open(txt, "r", encoding='utf-8')
    content = label.read()
    content = content.strip(" ")
    names = []
    for i in range(0, len(content)):
        names.append(content[i])
    return names


def load_one(im, print_pix=False):
    if len(im.shape) == 3:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        _, im = cv2.threshold(im, 200, 255, cv2.THRESH_BINARY)
    data_image = array('B')
    width, height = im.shape
    for x in range(0, width):
        s = ""
        for y in range(0, height):
            data_image.append(255 - im[x, y])
            if print_pix:
                if 255 - im[x, y] == 0:
                    s+="0"
                else:
                    s+="1"
    #     if print_pix:
    #         print(s)
    # if print_pix:
    #     print("")
    buf = np.frombuffer(data_image, np.uint8, offset=0).reshape(1, 28, 28)
    return buf


def predict(cv2_img, print_pix=False):
    im = load_one(cv2_img, print_pix)
    x_test = im.reshape(1, 28, 28, 1).astype('float32')
    x_test = x_test / 255.0
    # return '3',[]
    # model = load_model(model_path)
    # model.summary()

    # predictions = model.predict(x_test)
    # K.clear_session()
    with graph.as_default():
        predictions = model.predict(x_test)
    # return '3', []
    indexes = predictions.argsort()[0][-3:]
    arr = []
    for i in indexes:
        arr.append({
            "label":class_names[i],
            "value":predictions[0][i]
        })
    arr.reverse()
    # print(arr)
    return arr[0]["label"], arr


# model_path = "20210329v2.h5"
model_path = "20210527v1.h5"
model = load_model(model_path)
model.summary()

model._make_predict_function()
graph = tf.get_default_graph()
class_names = get_labels("label.txt")
test_img = np.zeros((28,28), np.uint8)
predict(test_img, False)


if __name__ == "__main__":
    # fpath = r"D:\pythonproject\collection\source\training-images\F\mnist-2019-12-06-DIKad6RF.jpg"
    # fpath = r"D:\pythonproject\collection\source\training-images\m\mnist-2020-02-20-8nhbW5d9.jpg"
    fpath = r"D:\pythonproject\collection\source\training-images\5\20190117202412_264.png"
    im = cv2.imread(fpath)
    mnist_result, all_result = predict(im)
    print(all_result)



