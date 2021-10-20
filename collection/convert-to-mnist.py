# coding=utf-8
from PIL import Image
from array import *
from random import shuffle
import os
import gzip
import shutil

# pip install Pillow
# pip install Pillow-PIL
# pip install pytest-shutil

# Load from and save to
BasePath ="./source/"
OutPutDir ="./target/"
Names = [['training-images','train'], ['test-images','test']]

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
class_names=getLabels(BasePath+"label.txt")
# class_names = class_names[1:]
# class_names = ['0','1','2','3','4','5','6','7','8','9','+','-','×','÷','=','>','<','.','(',')','%','[',']','A','B','C','D','E','F','√']

width=28
height=28
print(class_names)

for name in Names:
	
	data_image = array('B')
	data_label = array('B')

	FileList = []
	dir0= "%s%s" % (BasePath,name[0])

	for dirname in os.listdir(dir0): # [1:] Excludes .DS_Store from Mac OS
		# if str.index(dirname,".")
		# print(dirname)
		# if dirname not in class_names:
		# 	print(dirname)
		# 	continue
		path = os.path.join(dir0,dirname)
		for filename in os.listdir(path):
			if filename.endswith(".png"):
				FileList.append(os.path.join(name[0],dirname,filename))
			if filename.endswith(".jpg"):
				FileList.append(os.path.join(name[0], dirname, filename))
	print(len(FileList))

	shuffle(FileList) # Usefull for further segmenting the validation set

	for filename in FileList:
		# print(filename)
		arr=filename.split('\\')
		fname=arr[1]
		label=-1
		if len(fname)>1:
			b=int(fname,16)
			fname=chr(b)
		i=class_names.index(fname)
		if i<0:
			print("Err label:",arr[1])
			continue
		label = i

		realfilename=BasePath+filename
		# print(realfilename)
		Im = Image.open(realfilename)
		ImL= Im.convert('L')

		pixel = ImL.load()
		# gray

		width, height = Im.size

		if width!=28 or height !=28:
			print("Error im.size=",width,height,filename)
			continue
		
		if width>28 or height>28:
			Im=Im.resize((28,28))
			width, height = Im.size
		# print("im.size=",width,height)

		for x in range(0,width):
			for y in range(0,height):
				data_image.append(255-pixel[y,x])
				#反转

		data_label.append(label) # labels start (one unsigned byte each)

	hexval = "{0:#0{1}x}".format(len(FileList),6) # number of files in HEX

	# header for label array

	header = array('B')
	header.extend([0,0,8,1,0,0])
	header.append(int('0x'+hexval[2:][:2],16))
	header.append(int('0x'+hexval[2:][2:],16))
	
	data_label = header + data_label

	# additional header for images array
	
	if max([width,height]) <= 256:
		header.extend([0,0,0,width,0,0,0,height])
	else:
		raise ValueError('Image exceeds maximum size: 256x256 pixels');

	header[3] = 3 # Changing MSB for image data (0x00000803)
	
	data_image = header + data_image

	output_file = open(OutPutDir+name[1]+'-images-idx3-ubyte', 'wb')
	data_image.tofile(output_file)
	output_file.close()

	output_file = open(OutPutDir+name[1]+'-labels-idx1-ubyte', 'wb')
	data_label.tofile(output_file)
	output_file.close()

# gzip resulting files
def gzipFile(f1):
	with open(f1, 'rb') as f_in:
		with gzip.open(f1+".gz", 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)

for name in Names:
	# os.system('gzip '+BasePath+name[1]+'-images-idx3-ubyte')
	# os.system('gzip '+BasePath+name[1]+'-labels-idx1-ubyte')
	gzipFile(OutPutDir+name[1]+'-images-idx3-ubyte')
	gzipFile(OutPutDir+name[1]+'-labels-idx1-ubyte')

