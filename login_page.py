from tkinter import *
from tkinter import messagebox
import cv2
import subprocess
import pandas as pd

def giris():
    if (E1.get() == "admin") and (E2.get() == "1234"):
        L3['text'] = "Giriş Başarılı..."
        open_camera()
    else:
        L3['text'] = "Hatalı Giriş!"
        messagebox.showerror("Hata Başlık", "Hatalı Giriş")

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Hata Başlık", "Kamera açılamadı.")
        return

    # Video kaydediciyi ayarla
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('../opencvli/kayit.avi', fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()

        if not ret:
            messagebox.showerror("Hata Başlık", "Kamera görüntüsü alınamadı.")
            break

        # Görüntüyü kaydet
        out.write(frame)

        cv2.imshow("Kamera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kaydediciyi ve kamerayı serbest bırak
    out.release()
    cap.release()
    cv2.destroyAllWindows()

    # Giriş penceresini gizle
    window.withdraw()

    # photo_form.py dosyasını başlat
    subprocess.Popen(["python", "main.py"])

    # Giriş penceresini kapat
    window.quit()

window = Tk()
window.title("Kullanıcı Giriş Ekranı")
window.geometry("390x220")
window.resizable(width=False, height=False)

L3 = Label(window)
L3.place(x=148, y=200)

L1 = Label(window, text="Kullanıcı Adı")
L1.place(x=75, y=15)

E1 = Entry(window, width=25)
E1.place(x=77, y=45)

L2 = Label(window, text="Şifre")
L2.place(x=75, y=80)

E2 = Entry(window, textvariable=StringVar(), show='*', width=25)
E2.place(x=77, y=110)

bt = Button(window, text="Giriş Yap", padx="20", pady="5", command=giris)
bt.place(x=75, y=150)

window.mainloop()
