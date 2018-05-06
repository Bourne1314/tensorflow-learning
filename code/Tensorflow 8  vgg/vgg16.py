#!/usr/bin/python
#coding:utf-8

import inspect
import os
import numpy as np
import tensorflow as tf
import time
import matplotlib.pyplot as plt

#����RGB��ƽ��ֵ
VGG_MEAN = [103.939, 116.779, 123.68] 

class Vgg16():
    def __init__(self, vgg16_path=None):
        if vgg16_path is None:
			#���ص�ǰ����Ŀ¼
            vgg16_path = os.path.join(os.getcwd(), "vgg16.npy") 
			#�������ڼ�ֵ�ԣ�����ģ�Ͳ���
            self.data_dict = np.load(vgg16_path, encoding='latin1').item() 

    def forward(self, images):
        
        print("build model started")
		#��ȡǰ�򴫲���ʼʱ��
        start_time = time.time() 
		#������س���255
        rgb_scaled = images * 255.0 
		#��GRBת����ɫͨ����BRG
        red, green, blue = tf.split(rgb_scaled,3,3) 
		#��ȥÿ��ͨ��������ƽ��ֵ�����ֲ��������Ƴ�ͼ���ƽ������ֵ
		#�÷��������ڻҶ�ͼ����
        bgr = tf.concat([     
            blue - VGG_MEAN[0],
            green - VGG_MEAN[1],
            red - VGG_MEAN[2]],3)
        #����VGG��16�����磨����5�ξ����3��ȫ���ӣ����������������ռ��ȡ�������
		#��һ�ξ����������������㣬��������ػ��㣬������СͼƬ�ߴ�
        self.conv1_1 = self.conv_layer(bgr, "conv1_1") 
		#���������ռ��name������ȡ�ò�ľ���˺�ƫ�ã�����������㣬��󷵻ؾ�����������ֵ
        self.conv1_2 = self.conv_layer(self.conv1_1, "conv1_2")
		#���ݴ����pooling���ֶԸò�����Ӧ�ĳػ�����
        self.pool1 = self.max_pool_2x2(self.conv1_2, "pool1")
        
		#�ڶ��ξ����������������㣬һ�����ػ���
        self.conv2_1 = self.conv_layer(self.pool1, "conv2_1")
        self.conv2_2 = self.conv_layer(self.conv2_1, "conv2_2")
        self.pool2 = self.max_pool_2x2(self.conv2_2, "pool2")

        #�����ξ����������������㣬һ�����ػ���
        self.conv3_1 = self.conv_layer(self.pool2, "conv3_1")
        self.conv3_2 = self.conv_layer(self.conv3_1, "conv3_2")
        self.conv3_3 = self.conv_layer(self.conv3_2, "conv3_3")
        self.pool3 = self.max_pool_2x2(self.conv3_3, "pool3")
        
		#���Ķξ����������������㣬һ�����ػ���
        self.conv4_1 = self.conv_layer(self.pool3, "conv4_1")
        self.conv4_2 = self.conv_layer(self.conv4_1, "conv4_2")
        self.conv4_3 = self.conv_layer(self.conv4_2, "conv4_3")
        self.pool4 = self.max_pool_2x2(self.conv4_3, "pool4")
        
		#����ξ����������������㣬һ�����ػ���
        self.conv5_1 = self.conv_layer(self.pool4, "conv5_1")
        self.conv5_2 = self.conv_layer(self.conv5_1, "conv5_2")
        self.conv5_3 = self.conv_layer(self.conv5_2, "conv5_3")
        self.pool5 = self.max_pool_2x2(self.conv5_3, "pool5")
        
		#������ȫ����
		#���������ռ�name����Ȩ�������
        self.fc6 = self.fc_layer(self.pool5, "fc6")
		#����relu�����
        self.relu6 = tf.nn.relu(self.fc6) 
        
		#���߲�ȫ����
        self.fc7 = self.fc_layer(self.relu6, "fc7")
        self.relu7 = tf.nn.relu(self.fc7)
        
		#�ڰ˲�ȫ����
        self.fc8 = self.fc_layer(self.relu7, "fc8")
        self.prob = tf.nn.softmax(self.fc8, name="prob")
        
		#�õ�ȫ�򴫲�ʱ��
        end_time = time.time() 
        print(("time consuming: %f" % (end_time-start_time)))
        
		#��ձ��ζ�ȡ����ģ�Ͳ����ֵ�
        self.data_dict = None 
    
	#����������    
    def conv_layer(self, x, name):
		#���������ռ�name�ҵ���Ӧ�������������
        with tf.variable_scope(name): 
			#�����ò�ľ����
            w = self.get_conv_filter(name) 
			#�������
            conv = tf.nn.conv2d(x, w, [1, 1, 1, 1], padding='SAME') 
            #����ƫ����
			conv_biases = self.get_bias(name) 
			#����ƫ�ã������������
            result = tf.nn.relu(tf.nn.bias_add(conv, conv_biases)) 
            return result
    
	#�����ȡ����˵Ĳ���
    def get_conv_filter(self, name):
		#���������ռ�Ӳ����ֵ��л�ȡ��Ӧ�ľ����
        return tf.constant(self.data_dict[name][0], name="filter") 
    
	#�����ȡƫ����Ĳ���
    def get_bias(self, name):
		#���������ռ�Ӳ����ֵ��л�ȡ��Ӧ��ƫ����
        return tf.constant(self.data_dict[name][1], name="biases")
    
	#�������ػ�����
    def max_pool_2x2(self, x, name):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name=name)
    
	#����ȫ���Ӳ��ȫ�򴫲�����
    def fc_layer(self, x, name):
		#���������ռ�name��ȫ���Ӳ�ļ���
        with tf.variable_scope(name): 
			#��ȡ�ò��ά����Ϣ�б�
            shape = x.get_shape().as_list() 
            dim = 1
            for i in shape[1:]:
				#��ÿ���ά�����
                dim *= i 
			#�ı�����ͼ����״��Ҳ���ǽ��õ��Ķ�ά���������������ֻ�ڽ��������ȫ���Ӳ����ò���
            x = tf.reshape(x, [-1, dim])
			#����Ȩ��ֵ
            w = self.get_fc_weight(name) 
			#����ƫ����ֵ
            b = self.get_bias(name) 
            #�Ըò���������Ȩ��ͣ��ټ���ƫ��
            result = tf.nn.bias_add(tf.matmul(x, w), b) 
            return result
    
	#�����ȡȨ�صĺ���
    def get_fc_weight(self, name): 
		#���������ռ�name�Ӳ����ֵ��л�ȡ��Ӧ1��Ȩ��
        return tf.constant(self.data_dict[name][0], name="weights")

