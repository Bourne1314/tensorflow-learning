#coding:utf-8
#2���򴫲�����
#����tensorflow��input_data��ǰ�򴫲�mnist_forward��osģ��
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_forward
import os

#ÿ��ι���������ͼƬ��
BATCH_SIZE = 200
#��ʼѧϰ��
LEARNING_RATE_BASE = 0.1
#ѧϰ��˥����
LEARNING_RATE_DECAY = 0.99
#����ϵ��
REGULARIZER = 0.0001
#ѵ������
STEPS = 50000
#����ƽ��˥����
MOVING_AVERAGE_DECAY = 0.99
#ģ�ͱ���·��
MODEL_SAVE_PATH="./model/"
#ģ�ͱ�������
MODEL_NAME="mnist_model"


def backward(mnist):
    #��placeholder��ѵ������x�ͱ�ǩy_ռλ
    x = tf.placeholder(tf.float32, [None, mnist_forward.INPUT_NODE])
    y_ = tf.placeholder(tf.float32, [None, mnist_forward.OUTPUT_NODE])
    #����mnist_forward�ļ��е�ǰ�򴫲�����forword()���������������򻯣�����ѵ�����ݼ��ϵ�Ԥ����y
	y = mnist_forward.forward(x, REGULARIZER)
	#��ǰ����������������ֵ���趨Ϊ����ѵ������
    global_step = tf.Variable(0, trainable=False)

    #���ð������в���������ʧ����ʧ����loss
    ce = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cem = tf.reduce_mean(ce)
    loss = cem + tf.add_n(tf.get_collection('losses'))
    #�趨ָ��˥��ѧϰ��learning_rate
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        mnist.train.num_examples / BATCH_SIZE, 
        LEARNING_RATE_DECAY,
        staircase=True)

    #ʹ���ݶ�˥���㷨��ģ���Ż���������ʧ����
    #train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    train_step = tf.train.MomentumOptimizer(learning_rate,0.9).minimize(loss, global_step=global_step)
    #train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)
    #��������Ļ���ƽ��
    ema = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    ema_op = ema.apply(tf.trainable_variables())
	#ʵ�����ɻ�ԭ����ƽ����saver 
	#��ģ��ѵ��ʱ���뻬��ƽ������ʹģ���ڲ��������ϱ��ֵĸ��ӽ�׳
    with tf.control_dependencies([train_step,ema_op]):
        train_op = tf.no_op(name='train')

    saver = tf.train.Saver()

    with tf.Session() as sess:
		#���в�����ʼ��
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
       
		#�ϵ���ѵ������ckpt����
		ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
		    saver.restore(sess, ckpt.model_checkpoint_path)

		#ÿ��ι��batch_size�飨��200�飩ѵ�����ݺͶ�Ӧ��ǩ��ѭ������steps��
        for i in range(STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})
            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
				#����ǰ�Ự���ص�ָ��·��
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)


def main():
	#����mnist
    mnist = input_data.read_data_sets("./data/", one_hot=True)
    #���򴫲�
	backward(mnist)

if __name__ == '__main__':
    main()


