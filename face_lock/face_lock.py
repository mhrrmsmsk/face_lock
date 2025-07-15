# face_login/face_lock/face_lock.py
import cv2
import face_recognition
import os
import pickle
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "face_data.pkl")
UNKNOWN_DIR = os.path.join(BASE_DIR, "data", "unknown_faces")
os.makedirs(UNKNOWN_DIR, exist_ok=True)

def load_encodings():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def log_unauthorized(frame):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(UNKNOWN_DIR, f"unknown_{now}.jpg")
    cv2.imwrite(path, frame)

def ask_identity(encodings):
    root = tk.Tk()
    root.withdraw()
    answer = simpledialog.askstring("Kimlik Doğrulama", "Sen kimsin?")
    if not answer:
        return False
    for user in encodings.values():
        if answer.lower() == user["answer"].lower():
            return True
    return False

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def face_unlock(encodings, timeout=5):
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while time.time() - start_time < timeout:
        ret, frame = cap.read()
        if not ret: continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, faces)

        for enc in encs:
            for user in encodings.values():
                match = face_recognition.compare_faces([user["encoding"]], enc, tolerance=0.45)
                if match[0]:
                    cap.release()
                    cv2.destroyAllWindows()
                    return True

        cv2.imshow("Yüz Tanıma", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

if __name__ == "__main__":
    data = load_encodings()
    success = face_unlock(data)

    if not success:
        for attempt in range(3):
            if ask_identity(data):
                exit()
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            log_unauthorized(frame)
        lock_screen()
