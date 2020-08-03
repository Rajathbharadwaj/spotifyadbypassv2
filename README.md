# SpotifyAdBypass

<li>How to use SpotifyAdBypass</li><br>
  
    $ pip install spotifyadbypass
    
# Usage<br>

<h5>Make sure to keep Spotify closed as the program will auto open Spotify application.</h5>

Note : 
Use the Spotify  .exe installer do not use the Spotify's microsoft application

    from spotifyadbypass import SpotifyBypass

    def printSong(artistTitle):
        print(artistTitle["artist"].encode('utf-8'), '-', artistTitle["title"].encode('utf-8'), )

    #instantiate with a printSong callback
    byPass = SpotifyBypass(printSong)
