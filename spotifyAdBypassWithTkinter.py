import threading
from win32api import keybd_event, MapVirtualKey
import win32gui
import subprocess
import time
import re
import os
import tkinter as tk


PATH = "C:\\Users\\{}\\AppData\\Roaming\\Spotify\\Spotify.exe".format(os.getlogin())

HANDLE = None
class SpotifyBypass:

    def __init__(self, callback=None):
        self.windowHandle = None
        self.callback = callback
        self.artist = None
        self.title = None
        self.SONG_DATA_RE = re.compile(r'(.+) - (.+)')
        self.PROCESS = None
        self._stopScraping = threading.Event()
        self.details = []
        self.openSpotify(path=PATH)

        self.updateWindowHandle()

        if (self.callback):
            threading.Thread(target=self._updater, args=(self.callback, self._stopScraping)).start()

    def getArtistAndTitle(self):
        return {'artist': self.artist, 'title': self.title}

    @property
    def windowHandle(self):
        return self._windowHandle

    @windowHandle.setter
    def windowHandle(self, value):
        self._windowHandle = value

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = str(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = str(value)

    def stopScraping(self):
        self._stopScraping.set()

    @staticmethod
    def playPause():
        keybd_event(0xB3, MapVirtualKey(0xB3, 0))

    @staticmethod
    def restartSong():
        # ## Restart the song
        keybd_event(0xB1, MapVirtualKey(0xB1, 0))

    @staticmethod
    def nextSong():
        # ## Restart the song
        keybd_event(0xB0, MapVirtualKey(0xB0, 0))

    def openSpotify(self, path):

        self.PROCESS = subprocess.Popen(path)
        time.sleep(4)
        self.playPause()

    def closeSpotify(self):
        self.PROCESS.terminate()
        time.sleep(3)

    def updateWindowHandle(self, callback=None):
        def getSpotifyWindowHandle(hwnd, details):
            name = win32gui.GetWindowText(hwnd)
            className = win32gui.GetClassName(hwnd)

            if className == 'Chrome_WidgetWin_0' and len(name) > 0:
                details.append(name)
                self.windowHandle = hwnd
                global HANDLE
                HANDLE = hwnd
        win32gui.EnumWindows(getSpotifyWindowHandle, self.details)
        windowText = win32gui.GetWindowText(self.windowHandle)

        if not windowText:
            self.details = []
            win32gui.EnumWindows(getSpotifyWindowHandle, self.details)

        if (callback):
            callback()

    def songUpdater(self, callback=None):
        windowText = win32gui.GetWindowText(self.windowHandle)

        if windowText.startswith('Advertisement') or windowText == 'Spotify':
            self.details = []
            self.closeSpotify()
            self.openSpotify(path=PATH)
            self.nextSong()
            self.updateWindowHandle()

        if (not windowText):
            self.stopScraping()
            self.windowHandle = None
            self.details = []
            self.updateWindowHandle()
            self.playPause()
        artistTitle = self.SONG_DATA_RE.match(windowText)

        if artistTitle:
            artist = artistTitle.group(1)
            title = artistTitle.group(2)

            if self.artist != artist or self.title != title:
                self.artist = artist
                self.title = title

                if callback:
                    callback(self.getArtistAndTitle())
                else:
                    self.stopScraping()

    def _updater(self, callback, isScraping):
        while not isScraping.is_set():
            self.songUpdater(callback)
            time.sleep(2)


def printSong(songDict):
    print(songDict["artist"].encode('utf-8'), '-', songDict["title"].encode('utf-8'), )

trackName = None
def SongNamesDisplayer(label):
    def display():
        global trackName
        trackName = win32gui.GetWindowText(HANDLE)

        label.config(text=str(trackName))
        label.after(1000, display)
    display()

app = tk.Tk()

canvas = tk.Canvas(app, height=250, width=250)
canvas.pack()

open = tk.Button(app, text="Open Spotify", padx=10, pady=5, command=SpotifyBypass(printSong),)
open.pack()

playPause = tk.Button(app, text="Play/Pause Spotify", padx=10, pady=5, command=SpotifyBypass.playPause)
playPause.pack()
repeatSong = tk.Button(app, text="Repeat Song", padx=10, pady=5, command=SpotifyBypass.restartSong)
repeatSong.pack()
nxtSong = tk.Button(app, text="Next Song", padx=10, pady=5, command=SpotifyBypass.nextSong)
nxtSong.pack()
song = tk.Label(canvas, width=120, height=20, font="Helvetica 16 bold italic", fg="dark green")
song.pack()
SongNamesDisplayer(song)

app.mainloop()