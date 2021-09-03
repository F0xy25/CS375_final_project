#!/usr/bin/python

import logging
import boto3 
import sys
import os
import json
from PIL import Image
from botocore.exceptions import ClientError
from botocore.config import Config


def create_folder(folder_name, bucket_name="cs375ml"):
    
    s3_client.put_object(Bucket=bucket_name, Key=(folder_name+'/'))

def imbed_folder(parent,folder_name,bucket_name="cs375ml"):
    
    s3_client.put_object(Bucket=bucket_name, Key=(parent+'/'+ folder_name + '/'))

def put_file(filename,folder ,new_file,bucket_name="cs375ml"):
    print("Filename:",filename)
    print("Folder:",folder)
    print("New_file:",new_file)
    orig_folder = sys.argv[3]
    splt_orig_folder = orig_folder.split(".")
    new_path =  str(folder)+'/'+str(new_file)
    print(new_path)
    s3_client.upload_file(filename, bucket_name,new_path)

def get_file():
    #from path, get files from a subdirectory associated with the user, 
    username = 3


def folder_check(s3,username):
    #bucket = s3.Bucket('cs375ml')
    #folders = bucket.list("","/")
    folders = s3_client.list_objects_v2(Bucket='cs375ml', Delimiter='/', Prefix='')
    print(folders)
    for folder in folders:
        if folder == username:
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
        print("NO AWS KEY FOUND")
        print("EITHER INSERT KEY INTO Final_project_code/Key, or ask Gavin Fox (gdf28@drexel.edu) for key")
    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3',aws_access_key_id=key_vals[0], aws_secret_access_key=key_vals[1])
    print("AWS CONNECTED")
    return s3, s3_client

if __name__ == "__main__":
    #arguments are, username, image file location

    #where file is located: /temp_image
    file_folder = os.getcwd()+"/temp_img"


    print(sys.argv[0],sys.argv[1],sys.argv[2])

    [s3, s3_client] = configure()
    already_user = folder_check(s3, sys.argv[1])
    if already_user == True:
        print("ALREADY USER")
        filename = sys.argv[2]
        split_name = filename.split(".")
        orig_folder = sys.argv[3]
        splt_orig_folder = orig_folder.split(".")
        #imbed_folder(sys.argv[1], split_name[0])
        put_file((file_folder+"/"+sys.argv[2]),(sys.argv[1]+"/"+splt_orig_folder[0]), sys.argv[2])
    else:
        print("NEW USER")
        filename = sys.argv[2]
        split_name = filename.split(".")
        orig_folder = sys.argv[3]
        splt_orig_folder = orig_folder.split(".")
        create_folder(sys.argv[1])
        #imbed_folder(sys.argv[1], split_name[0])
        put_file((file_folder+"/"+sys.argv[2]),(sys.argv[1]+"/"+splt_orig_folder[0]), sys.argv[2])