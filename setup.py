# face_login/setup.py
import subprocess
import PyInstaller.__main__

# Register ekranı ve autorun setup çağır
subprocess.run(["python", "main.py"])
subprocess.run(["autorun_setup.bat"])

# Uygulama paketleme
PyInstaller.__main__.run([
    "face_lock/face_lock.py",
    "--name=face_lock",
    "--onefile",
    "--noconsole"
])
