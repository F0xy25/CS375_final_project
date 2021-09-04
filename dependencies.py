import sys
import os
import subprocess
import shutil
#install boto3, tensorflow, PIL, 


subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'tensorflow'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'tensorflow_hub'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'Pillow'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'boto3'])

print("AWSCLI")
subprocess.check_call([sys.executable, "-m","pip", "install", "awscli"])

#key_file = os.getcwd()+"/Key/aws_key.txt"
#keys = open(key_file, "r")
#key_vals = keys.readlines()
#with open("~/.aws/credentials", "w") as f:
#    f.write(keys)
#    f.close()
#keys.close()
#shutil.copyfile(os.getcwd()+"/Key/aws_key.txt", "~/.aws/credentials")

#ubprocess.check_call([sys.executable,'aws', "configure","{}".format(key_vals[0]),"{}".format(key_vals[1])])


#stream = os.popen("aws configure", mode="w")
#print(key_vals[0])
#stream.write("{}".format(key_vals[0]))
#print(key_vals[1])
#stream.write("{}".format(key_vals[1]))
#stream.write("us-east-1")
#stream.write("json")
#stream.close()
#os.system("echo '{}'".format(key_vals[0]))
#os.system("echo '{}'".format(key_vals[1]))
#subprocess.check_call([sys.executable, "echo", "'{}'".format(key_vals[0])])
#subprocess.check_call([sys.executable, "echo", "'{}'".format(key_vals[1])])
#subprocess.check_call([sys.executable, "echo", "'us-east-1'"])
#subprocess.check_call([sys.executable, "echo", "'json'"])