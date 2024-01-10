import cv2
import face_recognition
import os
from tkinter import messagebox
import time
from tkinter import *
from tkvideo import tkvideo

import pyttsx3, threading

def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech

    # Convert text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()



def load_known_faces(directory='./faces'):
    known_faces = []
    known_names = []

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            face_image = face_recognition.load_image_file(os.path.join(directory, filename))
            face_encoding = face_recognition.face_encodings(face_image)[0]
            known_faces.append(face_encoding)
            known_names.append(os.path.splitext(filename)[0])

    return known_faces, known_names

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def gui():
    global root,flag
    try:
        root = tk.Tk()
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load('1.gif')
        root.attributes('-topmost', True)
        root.attributes("-fullscreen", True)
        root.attributes('-alpha',0.5)
        root.overrideredirect(True)
        root.mainloop()
     
    except:
        root = tk.Toplevel()
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load('1.gif')
        root.attributes('-topmost', True)
        root.attributes("-fullscreen", True)
        root.attributes('-alpha',0.5)
        root.overrideredirect(True)
        root.mainloop()
    while True:
        if flag:
            return
def face_recognition_realtime():
    global root,flag
    flag = False
    threading.Thread(target=gui).start()
    
    # Load known faces and names
    known_faces, known_names = load_known_faces()
    start_time = time.time()
    # Open video capture
    video_capture = cv2.VideoCapture(0)

    while time.time()-start_time<10:
        # Capture each frame from the webcam
        ret, frame = video_capture.read()

        # Find face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            # Check if the face matches any known face
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

                # Close the window and show a popup message
                video_capture.release()
                cv2.destroyAllWindows()
                text_to_speech(f"Welcome back, Sir!")
               
                root.destroy()
                flag = True
                return True
            else:    
                video_capture.release()
                cv2.destroyAllWindows()
                text_to_speech("You are not autherized to access this area")
                
                root.destroy()
                pyautogui.hotkey('alt', 'f4')
                flag = True
                return False

    else:
        video_capture.release()
        cv2.destroyAllWindows()
        text_to_speech("You are not autherized to access this area")

        root.destroy()
        pyautogui.hotkey('alt', 'f4')
        flag = True
        return False
    
    

