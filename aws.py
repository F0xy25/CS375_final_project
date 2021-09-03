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
    new_path =  str(folder)+'/'+str(new_file)
    print(new_path)
    s3_client.upload_file(filename, bucket_name,new_path)


def folder_check(s3,username):
    #bucket = s3.Bucket('cs375ml')
    #folders = bucket.list("","/")
    folders = s3_client.list_objects_v2(Bucket='cs375ml', Delimiter='/', Prefix='')
    #folders = s3_client.list_objects(Bucket='cs375ml')
    print(folders)
    if 'CommonPrefixes' in folders.keys():
        for folder in folders['CommonPrefixes']:
            print("Folder",folder["Prefix"])
            if folder['Prefix'] == (username+"/"):
                return True
    else:
        return False

def compare_hash(s3,user,password):
    search_loc = str(user + '/usr_hash.txt')
    print('Search Loc',search_loc)
    obj = s3_client.get_object(Bucket='cs375ml', Key=str(user + '/usr_hash.txt'))
    print("Obj",obj)
    body = obj['Body'].read()
    print("BODY",body)
    print(password)
    if body.decode('ascii') == password:
        return True
    else:
        return False
    
def place_hash(s3, user, password):
    with open(os.getcwd()+"/tmp/usr_hash.txt","w") as text:
        text.write(password)
        text.close()
    put_file((os.getcwd()+'/tmp/usr_hash.txt'),user, "usr_hash.txt")
    
    #delet temp after done
    os.remove(os.getcwd()+"/tmp/usr_hash.txt")

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

    #print("ARGUMENTS")
    print(sys.argv[0],sys.argv[1],sys.argv[2])
    #print(type(sys.argv[3]))
    [s3, s3_client] = configure()
    already_user = folder_check(s3, sys.argv[1])
    #print("ALREADY USER",already_user)
    if already_user == True:
        if ((sys.argv[3]) == "login"):
            print("USER ALREADY FOUND")
            print("PASS MATCH")
            pass_match = compare_hash(s3, sys.argv[1], sys.argv[2])
            print(already_user)
            print(pass_match)
        
        elif (sys.argv[3] == 'register'):
            #run to break if user already registered
            print("USER ALREADY EXISTS")
            print("False")
            print("False")
        else:
            print("ELSE")
            filename = sys.argv[2]
            split_name = filename.split(".")
            imbed_folder(sys.argv[1], split_name[0])
            put_file((file_folder+"/"+sys.argv[2]),(sys.argv[1]+"/"+split_name[0]), sys.argv[2])
    else:
        
        if (sys.argv[3] == "login"):
            #print("PLACE HASH")
            #place_hash(s3, sys.argv[1], sys.argv[2])
            pass_match = compare_hash(s3, sys.argv[1], sys.argv[2])
            print(already_user)
            print(pass_match)
        elif (sys.argv[3] == 'register'):
            create_folder(sys.argv[1])
            print("PLACE HASH")
            place_hash(s3, sys.argv[1], sys.argv[2])
            print("False")
            print("True")
        else:
            create_folder(sys.argv[1])
            print("ELSE")
            filename = sys.argv[2]
            split_name = filename.split(".")
            create_folder(sys.argv[1])
            imbed_folder(sys.argv[1], split_name[0])
            put_file((file_folder+"/"+sys.argv[2]),(sys.argv[1]+"/"+split_name[0]), sys.argv[2])
