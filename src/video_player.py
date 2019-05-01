from tkinter import Tk, Label, Button, LEFT, RIGHT
from PIL import Image, ImageTk
import pyaudio
import wave
import os
import _thread
import sys
from video_io import VideoIO
import cv2
import numpy as np
import pickle

class Player:
    def __init__(self, audio_path, video_path, point_path, width, height, fps):
        self.logo_index = 0
        if os.path.exists(point_path):
            self.logo_array = pickle.load(open(point_path,"rb"))
        else:
            self.logo_array = []
        self.f = wave.open(audio_path,"rb")
        f = self.f
        self.chunk = int(f.getframerate()/fps)
        self.p = pyaudio.PyAudio() 
        p = self.p
        self.stream = p.open(format = p.get_format_from_width(f.getsampwidth()),channels = f.getnchannels(),rate = f.getframerate(), output = True)  
        self.data = f.readframes(self.chunk)
        self.audioPath = audio_path
        self.videoPath = video_path
        self.width = width
        self.height = height
        self.fps = fps
        self.ImgLength = width*height*3
        self.video_io = VideoIO(video_path, width, height)
        self.frameNum = self.video_io.get_num_frames()
        self.index = 0
        self.root = Tk()
        self.state = 0
        self.old = -1
        self.pilImage = self.video_io.read_frame(self.index)
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label2 = Label(self.root, image = self.tkImage)
        self.label2.pack()
        self.button_play = Button(self.root,text = 'play',command=self.start)
        self.button_pause = Button(self.root,text = 'pause',command=self.pause)
        self.button_stop = Button(self.root,text = 'stop',command=self.stop)
        self.button_play.pack(side=LEFT)
        self.button_pause.pack(side=LEFT)
        self.button_stop.pack(side=LEFT)
        self.label1 = Label(self.root, text="")
        self.label1.pack(side=RIGHT)
        self.root.mainloop()



    def read_wav(self):
        self.f = wave.open(self.audioPath,"rb") 
        f = self.f 
        self.p = pyaudio.PyAudio()  
        p = self.p
        self.stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                    channels = f.getnchannels(),
                                    rate = f.getframerate(), 
                                    output = True)  
               
    def videoplayer(self):
        if self.state:
            self.root.after(1, self.videoplayer)
        if self.state and self.index>self.old:
            if(self.index >= self.frameNum):
                self.stop()
            else:
                self.old = self.index
                self.pilImage = self.video_io.read_frame(self.index)
                self.label1.configure(text="")
                if(len(self.logo_array)>self.logo_index and (self.index-self.logo_array[self.logo_index][0])<2 and (self.index-self.logo_array[self.logo_index][0])>-1):#(index,logo, points)
                    points = np.array(self.logo_array[self.logo_index][2])
                    self.pilImage = cv2.cvtColor(np.asarray(self.pilImage), cv2.COLOR_RGB2BGR) 
                    cv2.polylines(self.pilImage, [points], 1, (0, 0, 255), 5)
                    self.pilImage = Image.fromarray(cv2.cvtColor(self.pilImage,cv2.COLOR_BGR2RGB))
                    self.logo_index = self.logo_index+1
                    self.label1.configure(text=self.logo_array[self.logo_index][1])
                self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
                self.label2.configure(imag=self.tkImage)

    def audioplayer(self):
        while (self.data and self.state):
            self.data = self.f.readframes(self.chunk)  
            self.index = self.index+1
            self.stream.write(self.data)  
        if not self.data:
            self.stop() 

    def start(self):
        print("start")
        if self.state==0:           
            self.state = 1
            try:
                _thread.start_new_thread( self.videoplayer, () )
                _thread.start_new_thread( self.audioplayer, () )
            except:
                print ("Error: unable to start thread")

    def pause(self):
        print("pause")
        self.state = 0

    def stop(self):
        print("stop")
        self.state = 0
        self.old = -1
        self.index = 0
        self.logo_index = 0
        self.pilImage = self.video_io.read_frame(self.index)
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label2.configure(imag=self.tkImage)
        self.root.update_idletasks()
        self.read_wav()
         

if __name__ == "__main__":
    width = 480
    height =270
    fps = 30
    point_path = str.split(sys.argv[1], '.rgb')[0]+'.pkl'
    print(point_path)
    player = Player(sys.argv[2], sys.argv[1], point_path, width, height, fps)




