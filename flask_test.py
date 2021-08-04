from flask import Flask, render_template, request, send_file, send_from_directory, jsonify
from numpy.lib.npyio import load
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np 
import pandas as pd 
import pickle
import sys
from PIL import Image





app = Flask(__name__, static_folder='static',template_folder='templates')
print("App Loaded", file=sys.stdout)

@app.route("/",methods=['POST','GET'])
def main():
    if request.method == 'GET':
        return render_template('index.html')

@app.route("/predict",methods=['POST','GET'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    
    if request.method == 'POST':
        print("POST REQUEST MADE", file=sys.stdout)
        #features = [x for x in request.body.values()]
        #print(features, file=sys.stdout)
        
        print(request.get_json(), file=sys.stdout)

        request_json = request.get_json()

        #probs better to replace with dictionary of urls
        if request_json['model'] == 'resnet':
            #load from tensorhub
            url_link = ''
        elif request_json['model'] == 'mobilenet':
            #load from tensorhub
            url_link = ''
        elif request_json['model'] == 'U-net':
            #load model from .h5py
            url_link = ''
        elif request_json['model'] == 'COCO':
            url_link = ''
        elif request_json['model'] == 'RCNN':
            #convert image to tensor,
            format_data = []
            img_data = Image.open("change this to file from request")
            img_data = np.array(img_data)
            print(img_data)

            print(type(img_data[0][0]))
            format_data.append(img_data)
            image_tensor = tf.convert_to_tensor(format_data, dtype=tf.uint8)
            detector = hub.load("https://tfhub.dev/tensorflow/faster_rcnn/resnet50_v1_1024x1024/1")
            detector_output = detector(image_tensor)
            return detector_output
            
        
        return



if __name__=='__main__':
    #We need to run the app to run the server
    app.run(debug=False)