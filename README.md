# SpotifyAdBypass

<li>How to use SpotifyAdBypass</li><br>
  
    $ pip install spotifybypassv2
      pip install pywin32
  
 # if git clone, use 
    $ pip install pywin32
# Usage<br>

<h5>Make sure to keep Spotify closed as the program will auto open Spotify application.</h5>

Note : 
Use the Spotify  .exe installer do not use the Spotify's microsoft application


    
    from spotifyadbypassv2 import spotifyBypassv2 as spfy
    
    def printSong(artistTitle):
        print(artistTitle["artist"].encode('utf-8'), '-', artistTitle["title"].encode('utf-8'), )

    #instantiate with a printSong callback
    
    byPass = spfy.SpotifyBypass(printSong)
