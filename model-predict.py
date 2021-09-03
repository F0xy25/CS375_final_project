#!/usr/bin/python
from numpy.lib.npyio import load
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np 
import pandas as pd 
import pickle
import sys
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import os
import sys
import json

#kick of instance to lambda function that is called through API Gateway
#TODO: Need to make folders in code that contain the downloaded models, as tf.hub naturally loads to var folder and
#thus fails when /var is cleared after a few days
#color dictionary used for food visualization
color_dict = {0:[0,0,0],
            1:[0,255,0],
            2:[51,255,51],
            3:[0,140,0],
            4:[100,255,100],
            5:[155,128,0],
            6:[255,0,0],
            7:[128,0,0],
            8:[255,153,153],
            9:[255,204,204],
            10:[127,0,255],
            11:[102,51,0],
            12:[255,255,102],
            13:[255,255,0],
            14:[0,204,102],
            15:[102,102,0],
            16:[0,102,102],
            17:[51,255,153],
            18:[255,229,204],
            19:[255,51,255],
            20:[0,255,255],
            21:[0,0,255],
            22:[153,153,153],
            23:[128,128,128],
            24:[192,192,192],
            25:[96,96,96]
            }

#VISUALIZE FOOD
def tf_load_image(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img

#VISUALIZE FOOD
def create_color_img(mapped):
    output = np.zeros((513,513,3))
    #print(output.shape)
    for i in range(0,512):
        for j in range(0,512):
            mapped_pix = mapped[i,j]
            output[i,j,0] = color_dict[mapped_pix][0]
            output[i,j,1] = color_dict[mapped_pix][1]
            output[i,j,2] = color_dict[mapped_pix][2]

    return output

#VISUALIZE MOBILE
def draw_bounding_box_on_image(image, ymin, xmin, ymax, xmax, color, font, thickness=2, display_str_list=()):
  """Adds a bounding box to an image."""
  draw = ImageDraw.Draw(image)
  im_width, im_height = image.size
  (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
  draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
             (left, top)],
            width=thickness,
            fill=color)

  # If the total height of the display strings added to the top of the bounding
  # box exceeds the top of the image, stack the strings below the bounding box
  # instead of above.
  display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
  # Each display_str has a top and bottom margin of 0.05x.
  total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

  if top > total_display_str_height:
    text_bottom = top
  else:
    text_bottom = top + total_display_str_height
  # Reverse list and print from bottom to top.
  for display_str in display_str_list[::-1]:
    text_width, text_height = font.getsize(display_str)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                    (left + text_width, text_bottom)],
                   fill=color)
    draw.text((left + margin, text_bottom - text_height - margin),
              display_str,
              fill="black",
              font=font)
    text_bottom -= text_height - 2 * margin

#VISUALIZE MOBILE
def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.01):
  """Overlay labeled boxes on an image with formatted scores and label names."""
  colors = list(ImageColor.colormap.values())

  try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                              25)
  except IOError:
    print("Font not found, using default font.")
    font = ImageFont.load_default()

  for i in range(min(boxes.shape[0], max_boxes)):
    if scores[i] >= min_score:
        ymin, xmin, ymax, xmax = tuple(boxes[i])
        display_str = "{}: {}%".format(class_names[i],
                                     int(100 * scores[i]))
        color = colors[hash(class_names[i]) % len(colors)]
        image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
        draw_bounding_box_on_image(
          image_pil,
          ymin,
          xmin,
          ymax,
          xmax,
          color,
          font,
          display_str_list=[display_str])
        np.copyto(image, np.array(image_pil))
  return image


def create_pose_dict(keypoints):
    pose_dict = {}
    
    for i in range(0,6):
        person = keypoints[i]
        if person[55] > .5:
            temp_person = {}
            temp_person['nose'] = person[0,1,2]
            temp_person['left_eye'] = person[3,4,5]
            temp_person['right_eye'] = person[6,7,8]
            temp_person['left_ear'] = person[9,10,11]
            temp_person['right_ear'] = person[12,13,14]
            temp_person['left_shoulder'] = person[15,16,17]
            temp_person['right_shoulder'] = person[18,19,20]
            temp_person['left_elbow'] = person[21,22,23]
            temp_person['right_elbow'] = person[24,25,26]
            temp_person['left_wrist'] = person[27,28,29]
            temp_person['right_wrist'] = person[30,31,32]
            temp_person['left_hip'] = person[33,34,35]
            temp_person['right_hip'] = person[36,37,38]
            temp_person['left_knee'] = person[39,40,41]
            temp_person['right_knee'] = person[42,43,44]
            temp_person['left_ankle'] = person[45,46,47]
            temp_person['right_ankle'] = person[48,49,50]
            pose_dict["person{}".format(i)] = temp_person
        else:
            continue

    return pose_dict

def draw_pose(image,pose_dict,new_filename):
    image = image.astype(np.uint8)
    image = image*255
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    
    for each_person in pose_dict.keys():
        for each_anchor in each_person.keys():
            [x,y,c] = pose_dict[each_person][each_anchor]
            draw.ellipse((x-5,y-5,x+5,y+5),fill="Green",outline="Green")
        #draw lines connecting points
        #draw.line([pose_dict[each_person]["nose"][0],pose_dict[each_person]["nose"][1],pose_dict[each_person]["left_eye"][0],pose_dict[each_person]["left_eye"][0]])

    #im_width, im_height = image.size
    #(left, right, top, bottom) = (xmin * im_width, xmax * im_width,
    #                            ymin * im_height, ymax * im_height)
    #raw.line([(left, top), (left, bottom), (right, bottom), (right, top),
    #         (left, top)],
    #        width=thickness,
    #        fill=color)
    new_filename = os.getcwd()+"/temp_img/"+new_filename
    image.save(new_filename, format='JPEG', quality=100)

    return 
def pose_visualize(image,keypoints, new_filename):
    #take POSE model output, save necessary info to
    #1,5,56
    #first 17*3 are keypoints y,x,confidence
    pose_dict = create_pose_dict(keypoints[0])
    
    draw_pose(image[0].numpy(), pose_dict, new_filename)
     
    return

def food_visualize(results, orig_filename, new_filename, img_data):

    #take food output, store into json file and create visualization image, attach side by side to 
    test = create_color_img(results['food_group_segmenter:semantic_predictions'][0].numpy())
    #unique = np.unique(results['food_group_segmenter:semantic_predictions'].numpy())
    #print(unique)
    test = test*255
    test = test.astype(np.uint8)
    img_data = img_data*255
    img_data = img_data.astype(np.uint8)
    #print(test.shape)
    #print(img_data.shape)
    #print("TEST",test)
    final1 = Image.fromarray(img_data)
    final2 = Image.fromarray(test)
    final = Image.new("RGB", (513*2, 513))
    final.paste(final1, (0,0)) 
    final.paste(final2, (513,0))
    #processed = Image.fromarray(final)
    #save file as filename_processed.jpg
    
    new_filename = os.getcwd()+"/temp_img/"+new_filename
    final.save(new_filename, format='JPEG', quality=100)
    return

def mobile_class_to_name(results):
    d = {}
    orig = results['detection_classes'].numpy()
    dict_loc = os.getcwd()+"/mobile_labels.txt"
    new_list = []
    with open(dict_loc) as f:
        for line in f:
            (key, val) = line.split()
            d[int(key)] = val
    
    for each in range(0, len(orig[0])):
        val = int(orig[0][each])
        #print(val)
        new_list.append(d[val])

    #print("ORIG")
    #print(new_list)
    return new_list



def mobile_visualize(result, orig_filename, new_filename):
    #take mobilenet output and visualize 
    img = tf_load_image(orig_filename)
    #print(result["detection_scores"])
    #temp = result['detection_boxes'].numpy()
    #rint(temp.shape())
    #print(result['detection_boxes'])
    image_with_boxes = draw_boxes(
      img.numpy(), result["detection_boxes"][0],
      mobile_class_to_name(result), result["detection_scores"][0])

    im = Image.fromarray(image_with_boxes)
    im.save(new_filename, format='JPEG',quality=100)
    
    return


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
        #output is a [1,6,56] tensor
        keypoints = outputs['output_0']
        pose_visualize(image,keypoints, sys.argv[3])
        #print(keypoints)

    elif sys.argv[1] == "FOOD":
        #https://tfhub.dev/google/seefood/segmenter/mobile_food_segmenter_V1/1
        format_data = []
        img_data = Image.open(sys.argv[2])
        #print('Opened Image')
        img_data = np.array(img_data)
        #print(img_data)
        img_data = tf.image.convert_image_dtype(img_data,tf.float32)

        #resize image
        img_data1 = tf.image.resize_with_crop_or_pad(img_data, 513,513)
        #print(test_image)
        #print(test_image_arr)
        #print(tf.shape(test_image).numpy())
        img_data = tf.reshape(img_data1, [1, 513, 513, 3])

        #print("Food")
        direct = os.getcwd()
        detector = hub.load(direct+"/ML_models/seefood_segmenter_mobile_food_segmenter_V1_1").signatures["default"]
        #print("Model Loaded")
        detector_output = detector(img_data)
        #print("Image Processed")
        #print(detector_output)
        food_visualize(detector_output,sys.argv[2],sys.argv[3],img_data1.numpy())
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
        mobile_visualize(detector_output, sys.argv[2] ,(os.getcwd()+"/temp_img/"+sys.argv[3]))
        #print(type(detector_output))
        #print(detector_output.keys())
        #class_ids = detector_output["detection_classes"]

        #print(class_ids)

   
    else:
        print("No model Selected")
    
    return "Completed"


if __name__=='__main__':
    #We need to run the app to run the server

    #print arguments
    print("Printing Arguments...")
    print(sys.argv[0],sys.argv[1],sys.argv[2])

    #open image and load into variable
    #usr_image = Image.open(sys.argv[2])
    
    predict()
    #print(output)
    