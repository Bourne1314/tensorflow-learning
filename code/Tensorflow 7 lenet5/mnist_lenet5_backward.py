#coding:utf-8
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_lenet5_forward
import os
import numpy as np

#batch������
BATCH_SIZE = 100
#��ʼѧϰ��
LEARNING_RATE_BASE =  0.005 
#ѧϰ��˥����
LEARNING_RATE_DECAY = 0.99 
#����
REGULARIZER = 0.0001
#����������
STEPS = 50000 
#����ƽ��˥����
MOVING_AVERAGE_DECAY = 0.99 
#ģ�ͱ���·��
MODEL_SAVE_PATH="./model/"
#ģ������
MODEL_NAME="mnist_model" 

def backward(mnist):
	#���������Ϊ�Ľ�����
	#��һ�ױ�ʾÿ��ι���ͼƬ�������ڶ��׺͵����׷ֱ��ʾͼƬ���зֱ��ʺ��зֱ��ʣ����Ľױ�ʾͨ����
    x = tf.placeholder(tf.float32,[
	BATCH_SIZE,
	mnist_lenet5_forward.IMAGE_SIZE,
	mnist_lenet5_forward.IMAGE_SIZE,
	mnist_lenet5_forward.NUM_CHANNELS]) 
    y_ = tf.placeholder(tf.float32, [None, mnist_lenet5_forward.OUTPUT_NODE])
	#ǰ�򴫲�����
    y = mnist_lenet5_forward.forward(x,True, REGULARIZER) 
	#����һ��ȫ�ּ�����
    global_step = tf.Variable(0, trainable=False) 
    #���������һ������y��softmax����ȡ�������ĳһ��ĸ���
    ce = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
	#�������ֵ
    cem = tf.reduce_mean(ce) 
    #���򻯵���ʧֵ
    loss = cem + tf.add_n(tf.get_collection('losses')) 
    #ָ��˥��ѧϰ�� 
    learning_rate = tf.train.exponential_decay( 
        LEARNING_RATE_BASE,
        global_step,
        mnist.train.num_examples / BATCH_SIZE, 
		LEARNING_RATE_DECAY,
        staircase=True) 
    #�ݶ��½��㷨���Ż���
    #train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    train_step = tf.train.MomentumOptimizer(learning_rate,0.9).minimize(loss, global_step=global_step)
    #���û���ƽ���ķ������²���
	ema = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    ema_op = ema.apply(tf.trainable_variables())
	#��train_step��ema_op����ѵ�������󶨵�train_op��
    with tf.control_dependencies([train_step, ema_op]): 
        train_op = tf.no_op(name='train')

    #ʵ����һ������ͻָ�������saver
    saver = tf.train.Saver() 
    #����һ���Ự 
    with tf.Session() as sess: 
        init_op = tf.global_variables_initializer() 
        sess.run(init_op) 
        #ͨ�� checkpoint �ļ���λ�����±����ģ�ͣ����ļ����ڣ���������µ�ģ��
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH) 
        if ckpt and ckpt.model_checkpoint_path:
        	saver.restore(sess, ckpt.model_checkpoint_path) 
       
        for i in range(STEPS):
			#��ȡһ��batch���ݣ�����������xsת��������������ͬ��״�ľ���
            xs, ys = mnist.train.next_batch(BATCH_SIZE) 
            reshaped_xs = np.reshape(xs,(  
		    BATCH_SIZE,
        	mnist_lenet5_forward.IMAGE_SIZE,
        	mnist_lenet5_forward.IMAGE_SIZE,
        	mnist_lenet5_forward.NUM_CHANNELS))
			#��ȡһ��batch���ݣ�����������xsת��������������ͬ��״�ľ���
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: reshaped_xs, y_: ys}) 
            if i % 100 == 0: 
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)

def main():
    mnist = input_data.read_data_sets("./data/", one_hot=True) 
    backward(mnist)

if __name__ == '__main__':
    main()


