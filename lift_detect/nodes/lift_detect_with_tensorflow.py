#!/usr/bin/env python
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import tensorflow as tf
from threading import Thread
from multiprocessing import Queue


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
            classNumber = int(out[0][:3].argmax())
            print "predicted class: ", classNumber

            if classNumber == 1:
                print 'It is an Open Lift'
            elif classNumber == 2:
                print 'It is a Closed Lift'
            # elif classNumber == 3:
            #     print 'It is an Open Door'
            # elif classNumber == 4:
            #     print 'It is a Closed Door'
        
    # return classNumber

if __name__ == "__main__":
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.3
    config.gpu_options.allow_growth = True

    graph = load_graph('../models/model.pb')
    x = graph.get_tensor_by_name('prefix/data:0')
    y = graph.get_tensor_by_name('prefix/prob:0')
    WIDTH, HEIGHT = 227, 227

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # ret, frame = cap.read()

    input_q = Queue(5)
    output_q = Queue()
    for i in range(1):
        t = Thread(target=detect_lift, args=(graph, x, y, WIDTH, HEIGHT, input_q, output_q))
        t.daemon = True
        t.start()

    while True: 
        ret, frame = cap.read()
        input_q.put(frame)

        # if output_q.empty():
        #     pass
        # else: 
            # cv2.imshow('Image Window', frame)
            # # frame_np = np.array(frame)
            
            # # img_gpu = self.cudaImg()

            # # classNumber = detect_lift(graph, x, y, WIDTH, HEIGHT, frame)

            # k = cv2.waitKey(1) & 0xFF
            # if k == 27:
            #     break
        cv2.imshow('Image Window', frame)
            
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    