#!/usr/bin/env python
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import rospy
import cv2
import numpy as np
import tensorflow as tf
from threading import Thread
from multiprocessing import Queue

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
config.gpu_options.allow_growth = True

rgb_images = None
bridge = CvBridge()

input_q = Queue(5)
output_q = Queue()

def videoCallback(data):
    global rgb_images
    global k
    try:
        #Convert the depth image using the default passthrough encoding
        color_image = bridge.imgmsg_to_cv2(data, "bgr8")
        rgb_images = color_image
        input_q.put(rgb_images)
    except CvBridgeError, e:
        print e
        #Convert the depth image to a Numpy array
        color_array = np.array(color_image, dtype=np.float32)


def load_graph(graph_filename):
    with tf.io.gfile.GFile(graph_filename, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def,
            input_map=None,
            return_elements=None,
            name="prefix",
            op_dict=None,
            producer_op_list=None
        )
    return graph

def detect_lift(graph, x, y, WIDTH, HEIGHT, input_q, output_q):

    with tf.Session(graph=graph, config=config) as sess:
        while True:
            frame = input_q.get()
            img = cv2.resize(frame, (WIDTH, HEIGHT))
            batch = np.array([img for i in range(10)])

            out = sess.run(y, feed_dict={x: batch})
            print "output shape: ", out.shape
            print "predicted class: ", out[0][:5].argmax()
            classNumber = int(out[0][:5].argmax())

            if classNumber == 1:
                print 'It is an Open Lift'
            elif classNumber == 2:
                print 'It is a Closed Lift'
            elif classNumber == 3:
                print 'It is an Open Door'
            elif classNumber == 4:
                print 'It is a Closed Door'
        

if __name__ == "__main__":
    rospy.init_node('door_detect', anonymous=True)
    rospy.Subscriber('/camera/color/image_rect_color', Image, videoCallback)

    graph = load_graph('../models/model.pb')
    x = graph.get_tensor_by_name('prefix/data:0')
    y = graph.get_tensor_by_name('prefix/prob:0')
    WIDTH, HEIGHT = 227, 227

    for i in range(1):
        t = Thread(target=detect_lift, args=(graph, x, y, WIDTH, HEIGHT, input_q, output_q))
        t.daemon = True
        t.start()

    while True: 
        cv2.imshow('Image Window', rgb_images)
            
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    print("shutdown program...")
    cv2.destroyAllWindows()
    
