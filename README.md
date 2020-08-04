# SpotifyAdBypass

<li>How to use SpotifyAdBypass</li><br>
  
    $ pip install spotifyadbypassv2
  
 # if git clone, use 
    $ pip install win32gui
# Usage<br>

<h5>Make sure to keep Spotify closed as the program will auto open Spotify application.</h5>

Note : 
Use the Spotify  .exe installer do not use the Spotify's microsoft application

<<<<<<< HEAD
    from spotifyadbypassv2 import SpotifyBypassv2
=======
    from spotifyadbypassv2 import SpotifyBypass as spfy
>>>>>>> 930302a466a8eeb2de1cab27831fc840b8beadd0

    def printSong(artistTitle):
        print(artistTitle["artist"].encode('utf-8'), '-', artistTitle["title"].encode('utf-8'), )

    #instantiate with a printSong callback
<<<<<<< HEAD
    byPass = SpotifyBypassv2(printSong)
=======
    byPass = spfy.SpotifyBypass(printSong)
>>>>>>> 930302a466a8eeb2de1cab27831fc840b8beadd0
