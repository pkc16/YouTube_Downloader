# Simple app which takes in a YouTube URL and downloads the video (with audio) or audio only

from tkinter import *
from pytube import YouTube
import configparser
import os

class SimpleWindow(object):

    def __init__(self, window):
        self.window = window
        self.window.wm_title("YouTube Downloader Application")
        self.create_labels(window)
        self.create_fields(window)
        self.save_to_directory = self.get_config_data()

    def create_labels(self, window):
        lblURL = Label(window, text="URL")
        lblURL.grid(row=1, column=0)

    def create_fields(self, window):
        self.url_text = StringVar(window)
        self.entURL = Entry(window, width=80, textvariable=self.url_text)
        self.entURL.grid(row=1, column=1)

        btnVideo = Button(window, text="Download full video", width=18, command=self.download_video)
        btnVideo.grid(row=4, column=1, sticky=W)

        btnAudio = Button(window, text="Download audio only", width=18, command=self.download_audio)
        btnAudio.grid(row=5, column=1, sticky=W)

    def download_video(self):
        video = YouTube(self.url_text.get()).streams.get_highest_resolution()
        video.download(self.save_to_directory)

    def download_audio(self):
        # get the highest bitrate audio
        audio = YouTube(self.url_text.get()).streams.get_audio_only()
        filename = audio.download(self.save_to_directory)

        # rename the file so it has .mp3 suffix
        base = os.path.splitext(filename)[0]
        os.rename(filename, base + '.mp3')

    def get_config_data(self):
        # get parameters from config file
        # first get the current directory
        cur_dir = os.path.dirname(__file__)

        # generate the absolute filepath of the output file
        config_filename = "yt_downloader_config.txt"
        config_filepath = os.path.join(cur_dir, config_filename)

        # now get the info from the config file
        parser = configparser.ConfigParser()
        parser.read_file(open(config_filepath))
        return parser.get('Settings', 'download_directory')



window = Tk()
simple_app = SimpleWindow(window)
window.geometry("600x150+300+300")  #(window width x window height + position right + position down)
window.grid_rowconfigure(3, minsize=20)
window.grid_rowconfigure(0, minsize=20)

window.mainloop()