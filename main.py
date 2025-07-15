# face_login/main.py
import subprocess
import os

subprocess.run(["python", "register/register_gui.py"])
os.system("face_lock/face_lock.py")
