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
from logger import logger


class Player:
    def __init__(self, audio_path, video_path, width, height, fps):
        self.logo_index = 0
        point_path = str.split(sys.argv[1], '.rgb')[0]+'.pkl'
        if os.path.exists(point_path):
            self.logo_array = pickle.load(open(point_path, "rb"))
            logger.i('Loaded logo positions from % s' % point_path)
        else:
            self.logo_array = []
        self.f = wave.open(audio_path, "rb")
        f = self.f
        self.chunk = int(f.getframerate()/fps)
        self.p = pyaudio.PyAudio()
        p = self.p
        self.stream = p.open(format=p.get_format_from_width(
            f.getsampwidth()), channels=f.getnchannels(), rate=f.getframerate(), output=True)
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
        self.label2 = Label(self.root, image=self.tkImage)
        self.label2.pack()
        self.button_fast_backword = Button(
            self.root, text='<<', command=self.fast_backword)
        self.button_play = Button(self.root, text='PLAY', command=self.start)
        self.button_pause = Button(self.root, text='PAUSE', command=self.pause)
        self.button_fast_forword = Button(
            self.root, text='>>', command=self.fast_forword)
        self.button_stop = Button(self.root, text='STOP', command=self.stop)

        self.button_fast_backword.pack(side=LEFT)
        self.button_play.pack(side=LEFT)
        self.button_pause.pack(side=LEFT)
        self.button_fast_forword.pack(side=LEFT)
        self.button_stop.pack(side=LEFT)
        self.label1 = Label(self.root, text="")
        self.label1.pack(side=RIGHT)
        self.root.mainloop()

    def fast_forword(self):
        self.index = self.index+150  # 5s
        self.old = self.index-1
        if self.index >= self.frameNum:
            self.index = self.frameNum-1
        while len(self.logo_array) > self.logo_index and self.index > self.logo_array[self.logo_index][0]:
            self.logo_index = self.logo_index+1

    def fast_backword(self):
        self.index = self.index-150  # 5s
        self.old = self.index-1
        if self.index < 0:
            self.index = 0
        while self.logo_index > 0 and self.index <= self.logo_array[self.logo_index-1][0]:
            self.logo_index = self.logo_index-1

    def read_wav(self):
        self.f = wave.open(self.audioPath, "rb")
        f = self.f
        self.p = pyaudio.PyAudio()
        p = self.p
        self.stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                             channels=f.getnchannels(),
                             rate=f.getframerate(),
                             output=True)

    def videoplayer(self):
        if(self.index >= self.frameNum):
            self.stop()
        if self.state:
            self.root.after(1, self.videoplayer)
        if self.state and self.index > self.old:
            self.old = self.index
            self.pilImage = self.video_io.read_frame(self.index)
            self.label1.configure(text="")
            # (index,logo, points)
            if(len(self.logo_array) > self.logo_index and (self.index-self.logo_array[self.logo_index][0]) < 2 and (self.index-self.logo_array[self.logo_index][0]) > -1):
                points = np.array(self.logo_array[self.logo_index][2])
                self.pilImage = cv2.cvtColor(
                    np.asarray(self.pilImage), cv2.COLOR_RGB2BGR)
                cv2.polylines(self.pilImage, [points], 1, (0, 0, 255), 5)
                self.pilImage = Image.fromarray(
                    cv2.cvtColor(self.pilImage, cv2.COLOR_BGR2RGB))
                self.logo_index = self.logo_index+1
                self.label1.configure(text=self.logo_array[self.logo_index][1])
            self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
            self.label2.configure(imag=self.tkImage)

    def audioplayer(self):
        while self.state:
            if int(self.index*self.f.getframerate()/self.fps) > self.f.getnframes():
                self.stop()
            else:
                self.f.setpos(int(self.index*self.f.getframerate()/self.fps))
                self.data = self.f.readframes(self.chunk)
                self.index = self.index+1
                self.stream.write(self.data)

    def start(self):
        logger.d("start")
        if self.state == 0:
            self.state = 1
            try:
                _thread.start_new_thread(self.videoplayer, ())
                _thread.start_new_thread(self.audioplayer, ())
            except:
                logger.e("Error: unable to start thread")

    def pause(self):
        logger.d("pause")
        self.state = 0

    def stop(self):
        logger.d("stop")
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
    logger.set_level('i')
    width = 480
    height = 270
    fps = 30
    player = Player(sys.argv[2], sys.argv[1], width, height, fps)
