简单的手写识别服务  
使用keras和自行收集的数据集重新训练的识别模型，和网上的手写识别教程的不同在于，网上的数据集大多是真实手写图片（有笔锋），这里的是用触摸屏写出来的坐标点数组还原出来的专门给手机app用的数据集。但是由于是自己人写的，数量和丰富性都有所不足，实际效果难说是不是优于普通手写识别。  
为了方便开发分成了几个小工程。  


 - uploadimg  
 一个简单的图片上传的python服务，会将小工具传来的笔迹坐标数组比例换算还原成28x28的图片。  
 运行：  
    python server.py

 - MnistDataGen   
 一个生成训练数据的安卓app小工具，选择字符类型，写&上传，并且有上传笔顺和测试识别结果的功能。

 - collection  
 将训练数据打包的工程，将图片置于source/test-images或source/trainging-images中，有新加入的识别则更新label.txt，运行`python convert-to-mnist.py`在target下生成打包的训练集。


 - handwriting
 运行`python handwriting.py`开始训练keras的h5分类模型。

 - service   
 使用模型进行识别的服务，模型本身只能单个字的识别，但是这里的使用场景是小学生直接在屏幕上手写做题并且识别出完整结果，导致笔划分割成了很大的问题，连笔、5之类笔划可能完全分开的字符如何分割/组合一个字，一直没有很好的解决方案，在触摸屏上多少会更潦草一些，小学生的书写更是难以捉摸-_-||   
最后采用的是拆分出更多的单笔划识别类型（ㄅつ丿㇏𠃍𠃌等），在根据位置进行初步的笔划分割后，如果识别置信度低，则进行单笔划识别，并且匹配笔划字典（dict.txt文件，可添加新的笔划模式），效果稍微变好了一些。

![图](https://raw.githubusercontent.com/CloudTsang/MnistService/main/MnistDataGen/Screenshot.png)
