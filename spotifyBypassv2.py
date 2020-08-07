import threading
from win32api import keybd_event, MapVirtualKey
import win32gui
import subprocess
import time
import re
import os

PATH = "C:\\Users\\{}\\AppData\\Roaming\\Spotify\\Spotify.exe".format(os.getlogin())


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

    def playPause(self):
        keybd_event(0xB3, MapVirtualKey(0xB3, 0))

    def restartSong(self):
        # ## Restart the song
        keybd_event(0xB1, MapVirtualKey(0xB1, 0))

    def nextSong(self):
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

sp = SpotifyBypass(printSong)