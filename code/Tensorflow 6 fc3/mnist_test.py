#coding:utf-8
#��֤�����׼ȷ�Ժͷ�����
import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_forward
import mnist_backward
#����5���ѭ�����ʱ��
TEST_INTERVAL_SECS = 5

def test(mnist):
	#����tf.Graph()����֮ǰ����ļ���ͼ
    with tf.Graph().as_default() as g:
		#����placeholder��ѵ������x�ͱ�ǩy_ռλ
        x = tf.placeholder(tf.float32, [None, mnist_forward.INPUT_NODE])
        y_ = tf.placeholder(tf.float32, [None, mnist_forward.OUTPUT_NODE])
		#����mnist_forward�ļ��е�ǰ�򴫲�����forword()����
        y = mnist_forward.forward(x, None)
        #ʵ�������л���ƽ����saver���󣬴Ӷ��ڻỰ������ʱģ���е����в�������ֵΪ���ԵĻ���ƽ��ֵ����ǿģ�͵��ȶ���
        ema = tf.train.ExponentialMovingAverage(mnist_backward.MOVING_AVERAGE_DECAY)
        ema_restore = ema.variables_to_restore()
        saver = tf.train.Saver(ema_restore)
		#����ģ���ڲ��Լ��ϵ�׼ȷ��
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        while True:
            with tf.Session() as sess:
				#����ָ��·���µ�ckpt
                ckpt = tf.train.get_checkpoint_state(mnist_backward.MODEL_SAVE_PATH)
				#��ģ�ʹ��ڣ�����س�ģ�͵���ǰ�Ի����ڲ������ݼ��Ͻ���׼ȷ����֤������ӡ����ǰ�����µ�׼ȷ��
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                    accuracy_score = sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})
                    print("After %s training step(s), test accuracy = %g" % (global_step, accuracy_score))
				#��ģ�Ͳ����ڣ����ӡ��ģ�Ͳ����ڵ���ʾ���Ӷ�test()�������
                else:
                    print('No checkpoint file found')
                    return
            time.sleep(TEST_INTERVAL_SECS)

def main():
	#����ָ��·���µĲ������ݼ�
    mnist = input_data.read_data_sets("./data/", one_hot=True)
    test(mnist)

if __name__ == '__main__':
    main()
