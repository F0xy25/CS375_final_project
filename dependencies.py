import sys
import os
import subprocess

#install boto3, tensorflow, PIL, 


subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'tensorflow'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'tensorflow_hub'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'Pillow'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'boto3'])

subprocess.check_call([sys.executable, 'cp', os.getcwd()+"/Key/aws_key.txt", "~./aws/credentials" ])