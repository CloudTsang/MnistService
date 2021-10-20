
import tensorflow as tf
from keras import layers
import numpy as np
import keras as keras
import  matplotlib.pyplot as plt
import os
import gzip
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from PIL import Image,ImageDraw
from array import *
import urllib
import random
import time
import cgi
import math
import traceback
import loss_history

 
pratise_cache ="data/user/"
BaseLine=False

def getLabels(txt):
	#获取labels
	label=open(txt,"r",encoding='utf-8')
	content=label.read()
	content=content.strip(" ")
	names=[]
	for i in range(0,len(content)):
		# print(content[i])
		names.append(content[i])
	return names


def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = tf.graph_util.convert_variables_to_constants(
            session, input_graph_def, output_names, freeze_var_names)
        return frozen_graph

def plot_image(i, predictions_array, true_label, imgs):
  # 显示图片
  predictions_array, true_label, img = predictions_array[i], true_label[i], imgs[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  # 显示数据 
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')


def load_data(basepath,testName="test"):

  dirname = basepath
  files = [
      'train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz',
      testName+'-labels-idx1-ubyte.gz', testName+'-images-idx3-ubyte.gz'
  ]

  paths = []
  for fname in files:
    p=os.path.join(dirname , fname)
    if os.path.exists(p):
      paths.append(p)
    else:
      print("Error: Can not load file:",p)
      raise ValueError('Can not load file:'+p)

  # print(paths)
  with gzip.open(paths[0], 'rb') as lbpath:
    y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)

  with gzip.open(paths[1], 'rb') as imgpath:
    x_train = np.frombuffer(
        imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28)

  with gzip.open(paths[2], 'rb') as lbpath:
    y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)

  with gzip.open(paths[3], 'rb') as imgpath:
    x_test = np.frombuffer(
        imgpath.read(), np.uint8, offset=16).reshape(len(y_test), 28, 28)

  return (x_train, y_train), (x_test, y_test)

def load_one(p):

  data_image = array('B')
  Im = Image.open(p).convert('L')

 
  # http://www.cnblogs.com/yinxiangnan-charles/p/5928689.html

  pixel = Im.load()

  # Im.show()
  
  width, height = Im.size
  print("@load_one w,h=",width,height)
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
      # data_image.extend(pi)
  
  x_test = np.frombuffer(data_image, np.uint8, offset=0).reshape(1, 28, 28)
  # print("x_test.len =",len(x_test))
  # print("x_test.shape =",x_test.shape)
  # print("x_test=",x_test)
  
  return x_test


def draw_split(jsdata):
    textdata=[]
    rectdata=[]
    onedata=[]
    rs=[]
    rs_len=0
    draw_set=[]
    for _,v in enumerate(jsdata):
        left=-1
        top=-1
        right=1
        bottom=1
        # print("v=",v)
        for i2,v2 in enumerate(v):
            x=v2[0]
            y=v2[1]
            if left==-1:
                left=x
                top=y
                right=x
                bottom=y
            if x<left:
                left=x
            if x>right:
                right=x
            if y<top:
                top=y
            if y>bottom:
                bottom=y
        draw_set.append((v,left,top,right,bottom))
    sort_set= sorted(draw_set ,key=lambda student: student[1] )
    
    last_rect=[0,0,0,0]
    last_v=sort_set[0]
    for i,v in enumerate(sort_set):
        if i==0:
            last_v=v
            onedata.append(v[0])
            last_rect=[v[1],v[2],v[3],v[4]]
            continue
        
        if last_rect[2]<v[1]:
            # right > left
            textdata.append(onedata)
            rectdata.append(last_rect)
            onedata=[v[0]]
            last_rect=[v[1],v[2],v[3],v[4]]
        else:
            #update
            if v[1]<last_rect[0]:
                #left
                last_rect[0]=v[1]
            if v[2]<last_rect[1]:
                #top
                last_rect[1]=v[2]
            if v[3]>last_rect[2]:
                #right
                last_rect[2]=v[3]
            if v[4]>last_rect[3]:
                #bottom
                last_rect[3]=v[4]
            onedata.append(v[0])
        last_v=v


    if len(onedata)>0:
        textdata.append(onedata)
        rectdata.append(last_rect)
    # print("last:",textdata)
    return textdata,rectdata

def draw_trim(jsdata):
    left=-1
    top=-1
    right=1
    bottom=1
    for _,v in enumerate(jsdata):
        for i2,v2 in enumerate(v):
            x=v2[0]
            y=v2[1]
            if left==-1:
                left=x
                top=y
                right=x
                bottom=y
            if x<left:
                left=x
            if x>right:
                right=x
            if y<top:
                top=y
            if y>bottom:
                bottom=y
    h2=bottom-top
    w2=right-left
    # print("trim:",w2,h2)
    side_len=w2
    if h2>w2:
        side_len=h2
    # print("side_len:",side_len)
    margin=math.ceil(side_len*0.05)

    left2=left-math.ceil((side_len-w2)/2)-margin
    top2=top-math.ceil((side_len-h2)/2)-margin
    w2=side_len+margin*2
    h2=side_len+margin*2
    for i1,v in enumerate(jsdata):
        for i2,v2 in enumerate(v):
            jsdata[i1][i2]=(v2[0]-left2,v2[1]-top2)
    return w2,h2,jsdata

def drawimg(w,h,draw_x,draw_y,jsdata,size):
    ## draw image
    size=3
    scale=1.0

    max_w=56
    max_h=56
    last_size=(28,28)

    #正方形
    if w>h:
      h=w
    else:
      w=h
    if w>max_w:
      scale=max_w/w
      w=max_w
      h=int(h*scale)
    elif w<max_w:
      scale=max_w/w
      w=max_w
      h=int(h*scale)
       
    if h>max_h:
      scale2=max_h/h
      h=max_h
      w=int(scale2*w)
      scale=scale*scale2
    elif h<max_h:
      scale2=max_h/h
      h=max_h
      w=int(scale2*w)
      scale=scale*scale2

    w=max_w
    h=max_h
 
    print("scale,w,h,size:",scale,w,h,size)
    # print("jsdata=",jsdata)
    # print("draw_x,draw_y:",draw_x,draw_y)
    # print("type draw_x,draw_y:",type(draw_x),type(draw_y))
    Offset = math.ceil((size-1)/2)
    image = Image.new("L",[w,h],'white') #Image.open(image_path)
    #创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(image)
    for _,v in enumerate(jsdata):
        for i2,v2 in enumerate(v):
            # print("v2=",v2)
            i0=v2[0]+draw_x
            f1=float(i0)
            x1=int(scale*float(f1))
            x2=int(scale*float(v2[1])+scale*float(draw_y))
            v[i2]=(x1,x2)
            # print(v[i2])
            if size>1:
              draw.ellipse((x1-Offset,x2-Offset,x1+Offset,x2+Offset), fill='black')
        # print("draw v=",v)
        draw.line(v, fill="black", width=size)
        # draw.polygon(v, outline=(0,0,0),fill=1)
    # image.show()
    image=image.resize(last_size)
    return image

input_path = "data" #mnist数据库
test_name ="test"
mode_file="./model/20210527v2.h5"

# input_path = "./keras/fashion-mnist-master/data/number/net" #mnist数据库
# test_name ="t10k"




seed = 7 
np.random.seed(seed)

 

# fashion_mnist = keras.datasets.fashion_mnist
 

# C:\Users\yondor\.keras\datasets\fashion-mnist
# (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
(train_images, train_labels), (test_images, test_labels) = load_data(input_path,testName=test_name)

print("train_images.shape=",train_images.shape)
num_pixels = train_images.shape[1] * train_images.shape[2]
print("num_pixels=",num_pixels)
# print("train_labels=",train_labels)



train_images_fit=train_images
test_images_fit=test_images
train_labels_fit=train_labels
test_labels_fit=test_labels

if BaseLine:
  train_images_fit = train_images.reshape(train_images.shape[0], num_pixels).astype('float32')
  test_images_fit = test_images.reshape(test_images.shape[0], num_pixels).astype('float32')
else:
  train_images_fit = train_images.reshape(train_images.shape[0], 28,28,1).astype('float32')
  test_images_fit = test_images.reshape(test_images.shape[0],28,28,1).astype('float32')

train_labels_fit = np_utils.to_categorical(train_labels)
test_labels_fit = np_utils.to_categorical(test_labels)


# class_names = ["0","1","2","3","4","5","6","7","8","9","+","-","×","÷","=",">","<",".","(",)"%","[","]","A","B","C","D","E","F","√"]

class_names=getLabels("data/label.txt")

num_classes = len(class_names)

print("train_images.size=",len(train_images))
print("train_labels.size=",len(train_labels))
print("test_images.size=",len(test_images))
print("test_labels.size=",len(test_labels))
print("num_classes=",num_classes)



train_images_fit = train_images_fit / 255.0

test_images_fit = test_images_fit / 255.0

# plt.figure(figsize=(3,4))
# for i in range(10):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i], cmap=plt.cm.binary)
#     plt.xlabel(class_names[train_labels[i]])
    



need_fit=True
if os.path.exists(mode_file):
  # 加载模型
  print("存在已有模型！")
  model=load_model(mode_file)
  need_fit=False
  model.summary()
else:
  model = keras.Sequential()
  if BaseLine:
    model.add(Dense(num_pixels, input_dim=num_pixels, init='normal', activation='relu'))
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dense(num_classes, init='normal', activation='softmax'))
    # model.summary()
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  else:
    model.add(Convolution2D(30, 5, 5, border_mode='valid', input_shape=( 28, 28, 1 ), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.4))
    model.add(Convolution2D(15, 3, 3, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.4))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(num_classes, activation='softmax'))
    # Compile model
  model.summary()
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])



# model.compile(optimizer=tf.train.AdamOptimizer(),
#                 loss='sparse_categorical_crossentropy',
#                 metrics=['accuracy'])

# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# model.summary()

# accuracy 准确率监控指标
# loss 损失函数 https://keras-cn.readthedocs.io/en/latest/other/objectives/
# 编译模型

if need_fit:
  # logs_loss = loss_history.LossHistory()
  # model.fit(train_images_fit, train_labels_fit,batch_size=64, epochs=20,verbose=1,callbacks=[logs_loss])
  model.fit(train_images_fit, train_labels_fit,batch_size=64, epochs=100,verbose=1)
  # logs_loss.end_draw()
  # 训练模型 epochs=总轮数,batch_size=没次训练样本数
  model.save(mode_file)
  # 保存模型

# output_names=[out.op.name for out in model.outputs]
# print("output_names=",output_names)

# frozen_graph = freeze_session(K.get_session(),
#                               output_names=output_names)
# tf.train.write_graph(frozen_graph, "model", "my_model.pb", as_text=False)


# test_loss, test_acc = model.evaluate(test_images_fit, test_labels_fit)

 
 

# 评估准确率

# img_slice=test_images[0:1]

predictions = model.predict(test_images_fit)
# predictions = model.predict(test_images)

# plt.figure(figsize=(1,1))
# plt.subplot(1,1,1)
# plt.grid(False)
# plt.imshow(test_images[0], cmap=plt.cm.binary)
# plt.xlabel(class_names[np.argmax(predictions[0])])
# plt.show()

# 做出预测
# print("img_slice=",img_slice)
print("label0=",test_labels[0])
print(predictions[0])
# 看第一张
print("predict0=",np.argmax(predictions[0]))


# test_myimg=load_one("./data/5.png")
# test_myimg_fit = test_myimg.reshape(1,28,28,1).astype('float32')
# test_myimg_fit = test_myimg_fit / 255.0

# print("test_myimg=",test_myimg)

# print("1",test_images_fit[0])
# print("2",test_myimg_fit[0])

# predictions2 = model.predict(test_myimg_fit)
# print("predictionsa=",predictions2)
# print("predictions2=",np.argmax(predictions2[0]))

# plt.figure(figsize=(1,1))
# plt.subplot(1,1,1)
# plt.grid(False)
# plt.imshow(test_myimg[0], cmap=plt.cm.binary)
# plt.xlabel(class_names[np.argmax(predictions2[0])])
# plt.show()


# 看那个最接近

# num_rows = 5
# num_cols = 2
# num_images = num_rows*num_cols
# plt.figure(figsize=(2*2*num_cols, 2*num_rows))
# for i in range(num_images):
#   plt.subplot(num_rows, 2*num_cols, 2*i+1)
#   plot_image(i, predictions, test_labels, test_images)
#   plt.subplot(num_rows, 2*num_cols, 2*i+2)
#   plot_value_array(i, predictions, test_labels)

# plt.show()


host = ('0.0.0.0', 80)

class Resquest(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
      print("do_OPTIONS")
      self.send_response(200, "ok")
      self.send_header('Access-Control-Allow-Origin', '*')
      self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
      self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
      self.send_header("Access-Control-Allow-Headers", "Content-Type")
      self.end_headers()
      
    def do_POST(self):
        print("path=",self.path)
        show_img=False
        self.path=self.path.strip(" ")
        p2=self.path.split("?")
        if len(p2)<=1 and p2[0]!="/draw" :
          self.send_response(400)
          self.send_header('Content-type', 'application/json')
          self.wfile.write(json.dumps({'result': "error param!"}).encode())
          self.end_headers()
          return

        param1=p2[0]

        content_len = int(self.headers.get('Content-Length'))
        print("content_len=",content_len)
        
        

        # post_body = self.rfile.read(content_len)
        # print("post_body=",post_body)
        


        img_paths=[]
        if param1=="/draw":
          txt=self.rfile.read(content_len)
          print("txt=",txt)
          jsdata={}
          try:
            jsdata = json.loads(txt)
          except:
            traceback.print_exc()
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.wfile.write(json.dumps({'result': "error json data!"}).encode())
            self.end_headers()
            return

          datas,rects=draw_split(jsdata["data"])
          last_h=0
          last_w=0
          h_i=0
          for v in datas:
            w,h,imgdata=draw_trim(v)
            if w<=0 or h<=0:
              print("Error: w or h is zero! w=",w,",h=",h)
              continue
            start_x=0
            start_y=0
            draw_w=w
            draw_h=h
            if h_i>0:
              cur_top=rects[h_i][1]
              last_top=rects[h_i-1][1]
              if h<last_h*0.5 and cur_top>(last_top+last_h*0.5):
                #小数点的情况
                start_x=math.ceil((last_w-w)/2)
                start_y=math.ceil((last_h-h))
                draw_w=last_w
                draw_h=last_h
            img=drawimg(draw_w,draw_h,start_x,start_y,imgdata,4)
            last_h=h
            last_w=w
            h_i+=1
            # img=drawimg(w,h,imgdata)
            str_time=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+"_"+str(random.randint(100,999))
            revpath = './data/tmp/%s.png' % str_time
            img.save(revpath)
            img_paths.append(revpath)
          # f.write(form.getvalue('file'))

        else:
          str_time=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+"_"+str(random.randint(100,999))
          revpath = './data/tmp/%s.png' % str_time
          form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST','CONTENT_TYPE': self.headers['Content-Type']}
          )
          f = open(revpath,'wb')
          param2=urllib.parse.parse_qs(p2[1])
          # self.do_action(mpath, margs)
          print(param2)
          path=param2["path"]
          # print("path=",path)
          f.write(form.getvalue('file'))
          f.close()
          img_paths.append(revpath)

        print("img_paths=",img_paths)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        # imgpath="./"+path[0]
        nums=""
        for imgpath in img_paths:
          img=load_one(imgpath)
          x_test=img
          if BaseLine:
            x_test = img.reshape(1,28*28).astype('float32')
          else:
            x_test = img.reshape(1,28,28,1).astype('float32')

          x_test = x_test / 255.0
          predictions = model.predict(x_test)
          # 看第一张
          # print("predictions=",predictions)

          num=int(np.argmax(predictions[0]))
          print("num=",num)
          nums=nums+class_names[num]

          #保存图片
          pname=class_names[num]
          if pname=="." or pname==">"  or pname=="<":
            print("change to ascii: ",pname)
            pname=hex(ord(pname))
          dirname=pratise_cache+pname
          if not os.path.exists(dirname):
            os.mkdir(dirname)
          filename=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+"_"+str(random.randint(100,999))
          target=dirname+"/"+filename+".png"
          open(target, "wb").write(open(imgpath, "rb").read())

          if show_img:
            plt.figure(figsize=(4,2))
            plt.subplot(1,2,1)
            plt.grid(False)
            plt.imshow(img[0], cmap=plt.cm.binary)
            index=np.argmax(predictions[0])
            predicted_label=class_names[index]
            plt.xlabel(predicted_label)

            plt.subplot(1,2,2)
            plt.grid(False)
            plt.xticks([])
            plt.yticks([])
            thisplot = plt.bar(range(10), predictions[0], color="#777777")
            plt.ylim([0, 1])
            thisplot[index].set_color('blue')
            plt.show()
            
        data = {'result': nums}
        self.wfile.write(json.dumps(data,ensure_ascii=False).encode())
        # thisplot[predicted_label].set_color('red')


if __name__ == '__main__':
    fpath = r'G:\pythonproject\collection\source\training-images\÷\20190326193956_892.png'
    fpath = r'G:\pythonproject\collection\source\test-images\√\mnist-2019-12-06-pCoGzkOP.jpg'
    fpath = r'G:\pythonproject\collection\source\test-images\零\mnist-2019-12-24-7GcDyoAz.jpg'
    # fpath = r'G:\pythonproject\collection\source\training-images\4\20190321122306_697.png'
    # fpath = r'G:\pythonproject\collection\source\training-images\5\_El4AiJ37_100_5.jpg'
    fpath = r'G:\pythonproject\collection\source\training-images\1616213562-005766-answer0.png'
    # fpath = r'G:\pythonproject\collection\source\training-images\6\_4oGyt2Wx_100_5.jpg'
    img = load_one(fpath)
    x_test = img
    if BaseLine:
        x_test = img.reshape(1, 28 * 28).astype('float32')
    else:
        x_test = img.reshape(1, 28, 28, 1).astype('float32')
    x_test = x_test / 255.0
    predictions = model.predict(x_test)
    # 看第一张
    # print("predictions=",predictions)

    num = int(np.argmax(predictions[0]))
    print("num=", num, " label=", class_names[num])


if __name__ == '__main2__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()