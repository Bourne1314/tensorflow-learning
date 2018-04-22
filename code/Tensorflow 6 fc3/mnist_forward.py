#coding:utf-8
#1ǰ�򴫲�����
import tensorflow as tf

#��������ڵ�Ϊ784��������ÿ������ͼƬ�����ظ�����
INPUT_NODE = 784
#����ڵ�Ϊ10������ʾ���Ϊ����0-9��ʮ���ࣩ
OUTPUT_NODE = 10
#���ز�ڵ�500��
LAYER1_NODE = 500


def get_weight(shape, regularizer):
	#��������ض���̬�ֲ�����ʹ�����򻯣�
    w = tf.Variable(tf.truncated_normal(shape,stddev=0.1))
    #w = tf.Variable(tf.random_normal(shape,stddev=0.1))
	#��ÿ��������������ʧ�ӵ�����ʧ��
    if regularizer != None: tf.add_to_collection('losses', tf.contrib.layers.l2_regularizer(regularizer)(w))
    return w


def get_bias(shape):  
	#��ʼ����һά���飬��ʼ��ֵΪȫ 0
    b = tf.Variable(tf.zeros(shape))  
    return b
	
def forward(x, regularizer):
	#������㵽���ز�Ĳ���w1��״Ϊ[784,500]
    w1 = get_weight([INPUT_NODE, LAYER1_NODE], regularizer)
	#������㵽���ص�ƫ��b1��״Ϊ����500��һά���飬
    b1 = get_bias([LAYER1_NODE])
	#ǰ�򴫲��ṹ��һ��Ϊ���� x����� w1������˼���ƫ�� b1 ���پ���relu���� ���õ����ز���� y1��
    y1 = tf.nn.relu(tf.matmul(x, w1) + b1)
    #�����ز㵽�����Ĳ���w2��״Ϊ[500,10]
    w2 = get_weight([LAYER1_NODE, OUTPUT_NODE], regularizer)
	#�����ز㵽�����ƫ��b2��״Ϊ����10��һά����
    b2 = get_bias([OUTPUT_NODE])
	#ǰ�򴫲��ṹ�ڶ���Ϊ������� y1��� �� w2 ������˼���ƫ�� ������˼���ƫ�� b2���õ���� y��
	#������� ��������� yҪ����softmax oftmax ������ʹ����ϸ��ʷֲ��������y������ relu����
    y = tf.matmul(y1, w2) + b2
    return y
