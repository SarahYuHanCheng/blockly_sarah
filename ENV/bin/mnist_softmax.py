# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A very simple MNIST classifier.

See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import data
from tensorflow.examples.tutorials.mnist import input_data
from array import array
import tensorflow as tf
import numpy as np


# preprocess need:
import os,fnmatch
import socket  
from PIL import Image
#from array import *
from random import shuffle

#gzip (windows can use)
import gzip
import shutil

from random import randrange
imgName = 0
# Load from and save to
Names = [['/Users/sarahcheng/Desktop/tensorflow_db/test_image//','test']]#, ['/Users/sarahcheng/Desktop/tensorflow_db/trainingSample//','train']
# Names = [['D:\\tensorflow_db\\','test'], ['D:\\tensorflow_db\\','test']]
img_test_dir = "///Users/sarahcheng/Desktop/tensorflow_db/test_image/2/"
img_train_dir = "///Users/sarahcheng/Desktop/tensorflow_db/trainingSample/"
output_dir = "/Users/sarahcheng/Documents/Master/scream/Blockly_/MNIST_data_copy/"
isRecv=False
tensorflow_img_recognize="tensorflowimg##"
prefix_tensorflow_prediction="tensorflowPrediction#"
recognize_false="false#"
recognize_true="true#"
# preprocess functions
def resizeImage(DATA_DIR):
    # Names = [['training-images\\','train'], ['tensorflow_db\\','test']]
    
    #DATA_DIR = "D:\\myimg2\\"
    file_data = []
    for filename in os.listdir(DATA_DIR):
        if fnmatch.fnmatch(filename,"*.jpg"):
            print('Loading: %s' % filename)
            im = Image.open(DATA_DIR+filename).convert('L')  # to Gray scale
            print (im.size)
            width = 28
            ratio = float(width)/im.size[0]
            height = 28
            nim = im.resize( (width, height), Image.BILINEAR )
            print (nim.size)
            nim.save(DATA_DIR+filename)

def convertImageToMnistFormat():

    for name in Names:
    
        data_image = array('B')
        data_label = array('B')

        FileList = []
        for dirname in os.listdir(name[0])[1:]: # [1:] Excludes .DS_Store from Mac OS
            print('dirname:'+dirname)
            path = os.path.join(name[0],dirname)#,dirname
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    FileList.append(os.path.join(name[0],dirname,filename))
                if filename.endswith(".jpg"):
                    FileList.append(os.path.join(name[0],dirname,filename))
        shuffle(FileList) # Usefull for further segmenting the validation set
        # print(FileList)
        for filename in FileList:
            # print ('filename: '+filename)
            label = int(filename.split('//')[1][0]) #sarah \\-->// # [2]-->[1][0]

            Im = Image.open(filename)
            print (filename)

            pixel = Im.load()

            width, height = Im.size
           # print ('width'+width)
           # print ('height'+height)
            x=0
            y=0
            for x in range(0,width):
                for y in range(0,height):
                    data_image.append(pixel[y,x])

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

        output_file = open(name[1]+'-images-idx3-ubyte', 'wb')
        data_image.tofile(output_file)
        print (name[1]+'-images-idx3-ubyte' + 'success!')
        output_file.close()

        output_file = open(name[1]+'-labels-idx1-ubyte', 'wb')
        data_label.tofile(output_file)
        print (name[1]+'-labels-idx1-ubyte' + 'success!')
        output_file.close()

##
def recvImage(DATA_DIR):
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    port = 17784                    # Reserve a port for your service.

    s.connect(("127.0.0.1", port))
##    s.send("imgte") only work on python 2.7
    s.send(tensorflow_img_recognize.encode('utf-8'))  # recv site also need to decode
    global isRecv
    while (not isRecv) :
        print(isRecv)
        cmd = s.recv(33) 
        strCmd = str(cmd.strip().decode('utf-8'))
        print('daemon said: '+ strCmd)        
        if strCmd.find('readyTheFileBuffer')!=-1:
            s.send((tensorflow_img_recognize+'fileBufferIsReady').encode('utf-8'))
            # start recv file
            global imgName
            imgName = randrange(9999999) # random a img file name  
            with open(DATA_DIR+str(imgName)+'.jpg', 'wb') as f:
                print ('file opened')
##                data = s.recv(1024)
##                f.write(991)
##                print(len(data))
##                print(len(cmd))
##                data = ""
                while True:
                    print('receiving data...')
                    data = s.recv(1024)                
                    #print('data=%s', (data))
                    if not data:
                        break
                    # write data to a file
                    f.write(data)

            f.close()
            print('Successfully get the file')
            s.close()
            print('connection closed')
            # why didn't need global keyword?
            # global isRecv
            isRecv=True

while True:    
    # recvImage("D:\\tensorflow_db\\0\\")  
    recvImage(img_test_dir)  
    ##try :
    ##    recvImage("D:\\tensorflow_db\\0\\")
    ##except:
    ##    print ("exception")

    if isRecv:
        resizeImage(img_test_dir)# /Users/sarahcheng
##        resizeImage("D:\\training-images\\1\\")
##        resizeImage("D:\\training-images\\2\\")
##        resizeImage("D:\\training-images\\3\\")
##        resizeImage("D:\\training-images\\4\\")
##        resizeImage("D:\\training-images\\5\\")
        convertImageToMnistFormat()

        for name in Names:
            with open(name[1]+'-images-idx3-ubyte', 'rb') as f_in, gzip.open(output_dir+name[1]+'-images.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            with open(name[1]+'-labels-idx1-ubyte', 'rb') as f_in, gzip.open(output_dir+name[1]+'-labels.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out) 

        flags = tf.app.flags
        FLAGS = flags.FLAGS
        # flags.DEFINE_string('data_dir', '/tmp/data/', 'Directory for storing data')

        mnist = input_data.read_data_sets("/Users/sarahcheng/Documents/Master/scream/Blockly_/MNIST_data_copy/", one_hot=True)

        sess = tf.InteractiveSession()

        # Create the model
        x = tf.placeholder(tf.float32, [None, 784])
        W = tf.Variable(tf.zeros([784, 10]))
        b = tf.Variable(tf.zeros([10]))
        y = tf.nn.softmax(tf.matmul(x, W) + b)

        # Define loss and optimizer
        y_ = tf.placeholder(tf.float32, [None, 10])
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

        # Train
        tf.initialize_all_variables().run()
        for i in range(1000):
          batch_xs, batch_ys = mnist.train.next_batch(100)
          train_step.run({x: batch_xs, y_: batch_ys})
          if i%100==0:
##              # Test trained model
##              correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
##              accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
##              print(accuracy.eval({x: mnist.test.images, y_: mnist.test.labels}))

              # prediction label(program think what it is)
              prediction=tf.argmax(y,1)
              print(prediction.eval(feed_dict={x: mnist.test.images}))
              myPrediction = str(prediction.eval(feed_dict={x: mnist.test.images}))

##              # probility of the prediction
##              probabilities=y
##              print("probabilities", probabilities.eval(feed_dict={x: mnist.test.images}, session=sess))

##        for i in range(1):
##            # ground truth
##            print(np.argmax(mnist.test.labels[i, :]))
##
        s = socket.socket()             # Create a socket object
        host = socket.gethostname()     # Get local machine name
        port = 17784                    # Reserve a port for your service. # sarah 0823 17784-->17789

        s.connect(("127.0.0.1", port))
    ##    s.send("imgte") only work on python 2.7
        # example: tensorflowimg##tensorflowPrediction#[5]
        s.send((tensorflow_img_recognize+prefix_tensorflow_prediction+myPrediction).encode('utf-8'))  # recv site also need to decode
        while True :
            cmd = s.recv(1024)
            strCmd = str(cmd.strip().decode('utf-8'))
            print(strCmd)
            directoryNameStartInedx = len(prefix_tensorflow_prediction)+len(recognize_false)
            original_img_path = 'D:\\tensorflow_db\\0'
            training_false_img_path = 'D:\\training-images\\'+strCmd[directoryNameStartInedx:len(strCmd)]
            training_true_img_path = 'D:\\training-images\\'+myPrediction[1:2]
            print('directoryNameStartInedx:'+str(directoryNameStartInedx))
            print('train_false_path:'+training_false_img_path)
            print('train_true_path:'+training_true_img_path)
            if strCmd.find('false')!=-1:
                if not os.path.exists(training_false_img_path):
                    os.makedirs(training_false_img_path)
                os.rename(original_img_path+'\\'+str(imgName)+'.jpg',training_false_img_path+'\\'+str(imgName)+'.jpg')
                s.send((tensorflow_img_recognize+'saveToDbSuccessful').encode('utf-8'))
                print('SaveToDbSuccessful')
                isRecv=False
                s.close()
                print('connection closed')
                break;
            elif strCmd.find('true')!=-1:
                print(myPrediction)
                os.rename(original_img_path+'\\'+str(imgName)+'.jpg',training_true_img_path+'\\'+str(imgName)+'.jpg')
                s.send((tensorflow_img_recognize+'saveToDbSuccessful').encode('utf-8'))
                print('SaveToDbSuccessful')
                isRecv=False
                s.close()
                print('connection closed')
                break;
            
