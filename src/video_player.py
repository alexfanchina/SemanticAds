import pyaudio
import wave
import os
import _thread
import sys
from video_io import VideoIO
from tkinter import Tk, Label, Button, LEFT
from PIL import Image, ImageTk

class Player:
    def __init__(self, audio_path, video_path, width, height, fps):
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
        self.root =Tk()
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
                print("******video"+str(self.index))
                self.pilImage = self.video_io.read_frame(self.index)
                self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
                self.label2.configure(imag=self.tkImage)

    def audioplayer(self):
        while (self.data and self.state):
            self.data = self.f.readframes(self.chunk)  
            self.index = self.index+1
            print("++++++audio"+str(self.index))
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
        self.video_io = VideoIO(self.videoPath, self.width, self.height)
        self.pilImage = self.video_io.read_frame(self.index)
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label2.configure(imag=self.tkImage)
        self.root.update_idletasks()
        self.read_wav()   


if __name__ == '__main__':
    width = 480
    height =270
    fps = 30
    player = Player(sys.argv[2], sys.argv[1], width, height, fps)





