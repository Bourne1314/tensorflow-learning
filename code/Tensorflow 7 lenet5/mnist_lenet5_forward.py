#coding:utf-8
import tensorflow as tf
#ÿ��ͼƬ�ֱ���Ϊ28*28
IMAGE_SIZE = 28
#Mnist���ݼ�Ϊ�Ҷ�ͼ��������ͼƬͨ����NUM_CHANNELSȡֵΪ1
NUM_CHANNELS = 1
#��һ�����˴�СΪ5
CONV1_SIZE = 5
#����˸���Ϊ32
CONV1_KERNEL_NUM = 32
#�ڶ������˴�СΪ5
CONV2_SIZE = 5
#����˸���Ϊ64
CONV2_KERNEL_NUM = 64
#ȫ���Ӳ��һ��Ϊ 512 ����Ԫ
FC_SIZE = 512
#ȫ���Ӳ�ڶ���Ϊ 10 ����Ԫ
OUTPUT_NODE = 10

#Ȩ��w����
def get_weight(shape, regularizer):
	w = tf.Variable(tf.truncated_normal(shape,stddev=0.1))
	if regularizer != None: tf.add_to_collection('losses', tf.contrib.layers.l2_regularizer(regularizer)(w)) 
	return w

#ƫ��b����
def get_bias(shape): 
	b = tf.Variable(tf.zeros(shape))  
	return b

#��������
def conv2d(x,w):  
	return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')

#���ػ������
def max_pool_2x2(x):  
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME') 

def forward(x, train, regularizer):
	#ʵ�ֵ�һ����
    conv1_w = get_weight([CONV1_SIZE, CONV1_SIZE, NUM_CHANNELS, CONV1_KERNEL_NUM], regularizer) 
    conv1_b = get_bias([CONV1_KERNEL_NUM]) 
    conv1 = conv2d(x, conv1_w) 
	#�����Լ���
    relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_b)) 
	#���ػ�
    pool1 = max_pool_2x2(relu1) 

    #ʵ�ֵڶ�����
    conv2_w = get_weight([CONV2_SIZE, CONV2_SIZE, CONV1_KERNEL_NUM, CONV2_KERNEL_NUM],regularizer) 
    conv2_b = get_bias([CONV2_KERNEL_NUM])
    conv2 = conv2d(pool1, conv2_w) 
    relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_b))
    pool2 = max_pool_2x2(relu2)
     
	#��ȡһ��������ά��
    pool_shape = pool2.get_shape().as_list() 
	#pool_shape[1] Ϊ�� pool_shape[2] Ϊ�� pool_shape[3]Ϊ��
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3] 
	#�õ�����������ĳ��ȣ�pool_shape[0]Ϊbatchֵ
    reshaped = tf.reshape(pool2, [pool_shape[0], nodes]) 

    #ʵ�ֵ�����ȫ���Ӳ�
    fc1_w = get_weight([nodes, FC_SIZE], regularizer) 
    fc1_b = get_bias([FC_SIZE]) 
    fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_w) + fc1_b) 
	#�����ѵ���׶Σ���Ըò����ʹ��dropout
    if train: fc1 = tf.nn.dropout(fc1, 0.5)

    #ʵ�ֵ��Ĳ�ȫ���Ӳ�
    fc2_w = get_weight([FC_SIZE, OUTPUT_NODE], regularizer)
    fc2_b = get_bias([OUTPUT_NODE])
    y = tf.matmul(fc1, fc2_w) + fc2_b
    return y 
