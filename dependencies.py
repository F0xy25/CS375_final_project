import sys
import subprocess

#install boto3, tensorflow, PIL, 


subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'tensorflow'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'Pillow'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'boto3'])