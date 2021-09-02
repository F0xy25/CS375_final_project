#!/usr/bin/python
from numpy.lib.npyio import load
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np 
import pandas as pd 
import pickle
import sys
from PIL import Image
import os
import sys

#kick of instance to lambda function that is called through API Gateway
#TODO: Need to make folders in code that contain the downloaded models, as tf.hub naturally loads to var folder and
#thus fails when /var is cleared after a few days

def predict():
    #probs better to replace with dictionary of urls
    if sys.argv[1] == 'POSE':
        #load from tensorhub
        print("pose")
        #url_link = "https://tfhub.dev/google/movenet/multipose/lightning/1"

        image = tf.io.read_file(sys.argv[2])
        image = tf.compat.v1.image.decode_jpeg(image)
        image = tf.expand_dims(image, axis=0)
        #resize and pad the image to keep the aspect ratio and fit the expected size
        image = tf.cast(tf.image.resize_with_pad(image, 256, 256), dtype=tf.int32)
        
        direct = os.getcwd()
        mdl = hub.load(direct+"/ML_models/movenet_multipose_lightning_1")
        movenet = mdl.signatures['serving_default']

        #Run model inference
        outputs = movenet(image)
        #output is a [1,1,17,3] tensor
        keypoints = outputs['output_0']
        print(keypoints)

    elif sys.argv[1] == "FOOD":
        #https://tfhub.dev/google/seefood/segmenter/mobile_food_segmenter_V1/1
        format_data = []
        img_data = Image.open(sys.argv[2])
        print('Opened Image')
        img_data = np.array(img_data)
        #print(img_data)
        img_data = tf.image.convert_image_dtype(img_data,tf.float32)

        #resize image
        img_data = tf.image.resize_with_crop_or_pad(img_data, 513,513)
        #print(test_image)
        #print(test_image_arr)
        #print(tf.shape(test_image).numpy())
        img_data = tf.reshape(img_data, [1, 513, 513, 3])

        print("Food")
        direct = os.getcwd()
        detector = hub.load(direct+"/ML_models/seefood_segmenter_mobile_food_segmenter_V1_1").signatures["default"]
        print("Model Loaded")
        detector_output = detector(img_data)
        print("Image Processed")
        print(detector_output)
        #return detector_output
        
    elif sys.argv[1] == 'MOBILENET':
        #https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2
        #requires tf.uint8 image of shape [1, height, width, 3]
        #load from tensorhub
        print("mobilenet")
        format_data = []
        img_data = Image.open(sys.argv[2])
        print('Opened Image')
        img_data = np.array(img_data)
        #print(img_data)

        print(type(img_data[0][0]))
        format_data.append(img_data)
        image_tensor = tf.convert_to_tensor(format_data, dtype=tf.uint8)
        #url_link = '"https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"'
        direct = os.getcwd()
        detector = hub.load(direct+"/ML_models/ssd_mobilenet_v2_2")
        detector_output = detector(image_tensor)
        print(detector_output)
        class_ids = detector_output["detection_classes"]
        print(class_ids)

    #elif sys.argv[1] == 'LANDMARKS':
        #https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_north_america_V1/1
        #url_link = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_north_america_V1/1'

    #    print("landmark NA")
    #    format_data = []
    #    image = tf.io.read_file(sys.argv[2])
    #    image = tf.expand_dims(image, axis=0)
    #   #resize and pad the image to keep the aspect ratio and fit the expected size
    #    image = tf.cast(tf.image.resize_with_pad(image, 321, 321), dtype=tf.int32)
        #scale to 321 x 321, and normalize to 0,1
    #    image = image/255
    
    #    direct = os.getcwd()
    #    detector = hub.load(direct+ "/ML_models/on_device_vision_classifier_landmarks_classifier_north_america_V1_1")
    #    print("Model Loaded")
    #    detector_output = detector(image)
    #    print("Image Processed")
    #    print(detector_output)


    #elif sys.argv[1] == 'RCNN':
        #https://tfhub.dev/tensorflow/faster_rcnn/resnet50_v1_1024x1024/1
        #convert image to tensor,
    #    print("rcnn")
    #    format_data = []
    #    img_data = Image.open(sys.argv[2])
    #    print('Opened Image')
    #    img_data = np.array(img_data)
        #print(img_data)

    #    print(type(img_data[0][0]))
    #    format_data.append(img_data)
    #    image_tensor = tf.convert_to_tensor(format_data, dtype=tf.uint8)
    #    print("Image_converted")
        #changed to local download of model to prevent /var deletion
    #    direct = os.getcwd()
    #    detector = hub.load(direct+"/ML_models/faster_rcnn_resnet50_v1_1024x1024_1")
    #    print("Model Loaded")
    #    detector_output = detector(image_tensor)
    #    print("Image Processed")
    #    print(detector_output)
    #    return detector_output
    #else:
    #    print("No model Selected")
    
    return "Completed"

#if models are not locally downloaded into the ML_models folder, do this process at this point
def model_check():
    #model path
    model_folder_path = "/ML_models"
    if os.listdir(model_folder_path+"/faster_rcnn_resnet50_v1_1024x1024_1") == 0:
        os.system("")
    if os.listdir(model_folder_path + "/ssd_mobilenet_v2_2") == 0:
        os.system("")
    



if __name__=='__main__':
    #We need to run the app to run the server

    #print arguments
    print("Printing Arguments...")
    print(sys.argv[0],sys.argv[1],sys.argv[2])

    #open image and load into variable
    #usr_image = Image.open(sys.argv[2])
    
    predict()
    #print(output)
    