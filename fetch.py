#!/usr/bin/python

import logging
import boto3 
import sys
import os
import json
from PIL import Image
from botocore.exceptions import ClientError
from botocore.config import Config

def possible_files(s3,user):
    print("poss_files")
    objs = s3_client.list_objects_v2(Bucket='cs375ml', Prefix=user+"/")
    #print("Obj",objs)
    #print(objs.keys())
    #print("CONTENTS",objs['Contents'])
    file_list = []
    for each in objs['Contents']:
        if ("MOBILENET" in each["Key"] or "FOOD" in each["Key"]): 
            
            #print("EACH",each["Key"])
            filename = each["Key"].split("/")
            #print("filename",filename[-1])
            file_list.append("/temp_img/"+filename[-1])
            with open(os.getcwd()+"/temp_img/"+filename[-1], 'wb') as f:
                s3_client.download_file("cs375ml", each["Key"], os.getcwd()+"/temp_img/"+filename[-1])

            #file = s3_client.get_object(Bucket='cs375ml', Key=each["Key"])
            #s3_client.download_file('cs375ml', (each["Key"]), ("/temp_img/"+filename[-1]))

    return file_list

def folder_check(s3,username):
    #bucket = s3.Bucket('cs375ml')
    #folders = bucket.list("","/")
    folders = s3_client.list_objects_v2(Bucket='cs375ml', Delimiter='/', Prefix='')
    #folders = s3_client.list_objects(Bucket='cs375ml')
    print(folders)
    if 'CommonPrefixes' in folders.keys():
        for folder in folders['CommonPrefixes']:
            #print("Folder",folder["Prefix"])
            if folder['Prefix'] == (username+"/"):
                return True
    else:
        return False

def configure():
    #read config file from /keys
    key_file = os.getcwd()+"/Key/aws_key.txt"
    try:
        keys = open(key_file, "r")
        key_vals = keys.readlines()
    except FileNotFoundError:
        no_file = True
        #print("NO AWS KEY FOUND")
        #print("EITHER INSERT KEY INTO Final_project_code/Key, or ask Gavin Fox (gdf28@drexel.edu) for key")
    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3',aws_access_key_id=key_vals[0], aws_secret_access_key=key_vals[1])
    #print("AWS CONNECTED")
    return s3, s3_client

if __name__ == "__main__":
    #arguments are, username, image file location

    #where file is located: /temp_image
    file_folder = os.getcwd()+"/temp_img"

    #print(type(sys.argv[3]))
    [s3, s3_client] = configure()
    already_user = folder_check(s3, sys.argv[1])
    #print("already user", already_user)
    list_files = possible_files(s3_client, sys.argv[1])
    for each in list_files:
        print(each)
    #print("ALREADY USER",already_user)