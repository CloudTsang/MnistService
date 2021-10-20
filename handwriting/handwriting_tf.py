import tensorflow as tf
import  numpy as np
import PIL.Image as Image
from skimage import io, transform
from array import *
import cv2


def load_one(p):

  data_image = array('B')
  Im = Image.open(p).convert('L')
  # http://www.cnblogs.com/yinxiangnan-charles/p/5928689.html
  # Im = Im.resize((28,28),Image.ANTIALIAS)
  pixel = Im.load()
  # Im.show()
  
  width, height = Im.size
  # print("@load_one w,h=",width,height)
  for x in range(0,width) :
    for y in range(0,height) :
      # pi=255-pixel[y,x]
      # 反转
      # print(pi)
      # if pi>=255:
      #   # 白色变透明
      #   pi=0
      # a=np.average(pi)
      # print(x,y)
      data_image.append(255-pixel[y,x])
      # data_image.append(255 - pixel[x, y])
      # data_image.extend(pi)
  
  x_test = np.frombuffer(data_image, np.uint8, offset=0).reshape(1, 28, 28)
  # print(x_test)
  return x_test


def recognize(img_path, pb_file_path):
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()

        with open(pb_file_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            # print(output_graph_def)
            _ = tf.import_graph_def(output_graph_def, name="")

        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)
            
            # print("graph:",sess.graph)
            ops=sess.graph.get_operations()
            # print("ops:",ops)
            # for op in enumerate(ops):
            #     if len(op[1].outputs)>0:
            #         print("op ",op[1].name,op[0],op[1].type,op[1].outputs[0].shape,op[1].outputs[0].dtype)
            #     else:
            #         print("op ",op[1].name,op[0],op[1].type)
 
            input_x = sess.graph.get_tensor_by_name("conv2d_1_input:0")
            # print(input_x)
            # out_softmax = sess.graph.get_tensor_by_name("softmax:0")
            # print(out_softmax)
            out_softmax = sess.graph.get_tensor_by_name("dense_3/Softmax:0")
            # print(out_softmax)

            # img = io.imread(img_path,True)
            img = load_one(img_path)
            input_x_data = img.reshape(1,28,28,1).astype('float32')
            
            img_out_softmax = sess.run(out_softmax, feed_dict={input_x:input_x_data})

            # print("img_out_softmax:",img_out_softmax)
            prediction_labels = np.argmax(img_out_softmax, axis=1)
            # print("label:",prediction_labels)


def recognize2(buff, pb_file_path):
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()
        with open(pb_file_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")

        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)
            ops = sess.graph.get_operations()
            # for op in enumerate(ops):
            #     if len(op[1].outputs) > 0:
            #         print("op ", op[1].name, op[0], op[1].type, op[1].outputs[0].shape, op[1].outputs[0].dtype)
            #     else:
            #         print("op ", op[1].name, op[0], op[1].type)
            input_x = sess.graph.get_tensor_by_name("conv2d_1_input:0")
            out_softmax = sess.graph.get_tensor_by_name("dense_3/Softmax:0")
            input_x_data = buff.reshape(1, 28, 28, 1).astype('float32')
            img_out_softmax = sess.run(out_softmax, feed_dict={input_x: input_x_data})
            prediction_labels = np.argmax(img_out_softmax, axis=1)
            # print("label:", prediction_labels)
        return prediction_labels[0]


if __name__ == '__main__':
    # recognize("data/5.png", "model/20190322v5.pb")

    # img = cv2.imread(r'G:\pythonproject\exam_split\tmp\testpaper1_7.png')
    # img = cv2.resize(img, (28,28))
    # cv2.imshow('img', img)
    # cv2.waitKey()

    recognize(r'G:\pythonproject\handwriting\data\testpaper1_2_28.png', "model/20190322v5.pb")
    # recognize(r'G:\pythonproject\handwriting\data\3.png', "model/20190322v5.pb")
    # recognize("data/3.png", "model/20190322v5.pb")

