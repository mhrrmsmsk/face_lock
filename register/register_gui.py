# face_login/register/register_gui.py
import cv2
import face_recognition
import tkinter as tk
from tkinter import messagebox
import os
import pickle
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "face_data.pkl")
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

class FaceRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yüz ve Güvenlik Sorusu Kaydı")
        self.cap = cv2.VideoCapture(0)

        self.video_label = tk.Label(root)
        self.video_label.grid(row=0, column=0, columnspan=2)

        tk.Label(root, text="İsim:").grid(row=1, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1)

        tk.Label(root, text="Gizli cevap:").grid(row=2, column=0)
        self.answer_entry = tk.Entry(root, show="*")
        self.answer_entry.grid(row=2, column=1)

        self.save_button = tk.Button(root, text="Kaydet", command=self.save_face)
        self.save_button.grid(row=3, column=0, columnspan=2)

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(10, self.update_frame)

    def save_face(self):
        name = self.name_entry.get().strip()
        answer = self.answer_entry.get().strip()
        if not name or not answer:
            messagebox.showerror("Hata", "İsim ve cevap zorunludur.")
            return

        ret, frame = self.cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)

        if len(faces) != 1:
            messagebox.showwarning("Uyarı", "Kamerada sadece bir yüz görünmeli.")
            return

        encoding = face_recognition.face_encodings(rgb, faces)[0]

        data = {}
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "rb") as f:
                data = pickle.load(f)

        data[name] = {"encoding": encoding, "answer": answer}

        with open(DATA_PATH, "wb") as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

        messagebox.showinfo("Başarılı", "Kayıt tamamlandı.")
        self.root.destroy()

    def __del__(self):
        self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRegisterApp(root)
    root.mainloop()
