
from numpy.lib.npyio import load
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np 
import pandas as pd 
import pickle
import sys
from PIL import Image
import json
import os
import sys

#kick of instance to lambda function that is called through API Gateway


def predict():
    #probs better to replace with dictionary of urls
    if sys.argv[1] == 'resnet':
        #load from tensorhub
        print("resnet")
        url_link = ''
    elif sys.argv[1] == 'mobilenet':
        #load from tensorhub
        print("mobilenet")
        url_link = ''
    elif sys.argv[1] == 'U-net':
        #load model from .h5py
        print("u-net")
        url_link = ''
    elif sys.argv[1] == 'COCO':
        print("coco")
        url_link = ''
    elif sys.argv[1] == 'RCNN':
        #convert image to tensor,
        print("rcnn")
        format_data = []
        img_data = Image.open(sys.argv[2])
        print('Opened Image')
        img_data = np.array(img_data)
        print(img_data)

        print(type(img_data[0][0]))
        format_data.append(img_data)
        image_tensor = tf.convert_to_tensor(format_data, dtype=tf.uint8)
        print("Image_converted")
        detector = hub.load("https://tfhub.dev/tensorflow/faster_rcnn/resnet50_v1_1024x1024/1")
        print("Model Loaded")
        detector_output = detector(image_tensor)
        print("Image Processed")
        return detector_output
    else:
        print("No model Selected")
    
    return "Completed"



if __name__=='__main__':
    #We need to run the app to run the server
    output = predict()
    print(output)