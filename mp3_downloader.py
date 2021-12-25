import tkinter
import traceback
import youtube_dl
import re
import os
from tkinter import filedialog
from pytube import Playlist



def downloader(url: str):
    if "/playlist?list=" in url:
        while True:
            playlist = Playlist(url)
            if len(playlist.video_urls) == 0:
                print("\n--------------------------------------------------------------------------------------------------\n| There was an error, please make sure you entered a valid link to a playlist that is not empty. | \n--------------------------------------------------------------------------------------------------\n")
                url = input("Enter the youtube link you want to download: ")
                downloader(url)
            else:
                break          
        while True:
            yes_no = input("This is a playlist! Would you like to specify a custom download range? Yes/No\n")
            if yes_no.casefold() != "no" and yes_no.casefold() != "yes":
                print("\n----------------------------------------------\n| Error: Invalid response, please try again! | \n----------------------------------------------\n")
                continue
            break
        if yes_no.casefold() == "yes":
            pattern = r"(https:\/\/www\.youtube\.com\/watch\?v=[A-Za-z0-9-_]{11}).*"
            while True:
                try:
                    first_video = re.fullmatch(pattern,input("Enter the url of the song in the playlist you want to start downloading from: ")).group(1)
                    playlist_min_range = playlist.index(first_video)
                    break
                except:
                    print("\n------------------------------------------------------------------------\n| This url cannot be found in the playlist you gave, please try again! |\n------------------------------------------------------------------------\n")
            while True:
                try:
                    last_video = re.fullmatch(pattern,input("Enter the url of the song in the playlist you want to download to: ")).group(1)
                    playlist_max_range = playlist.index(last_video) + 1
                    break
                except:
                    print("\n------------------------------------------------------------------------\n| This url cannot be found in the playlist you gave, please try again! |\n------------------------------------------------------------------------\n")
            playlist = playlist[playlist_min_range: playlist_max_range]
        for video_url in playlist:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{downloads_path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'updatetime': False #sets the "Date Modified" for the file that's downloaded to be the current time (This is a default sort option used by File Explorer on Windows)
            }
            while True:
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                        break
                except Exception as e:
                    print(e)
                    traceback.print_exc()
        print("Done downloading mp3 files") # open the downloads_path automatically for user convenience
        os.startfile(downloads_path)
        return
    else:
        print("Downloading URL")
        ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{downloads_path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'updatetime': False #sets the "Date Modified" for the file that's downloaded to be the current time (This is a default sort option used by File Explorer on Windows)
            }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try_counter = 0
            while True:
                #sometimes theres some error that doesn't allow a video to be downloaded properly, happens rarely so I let it try 3 times before asking for another link
                if try_counter == 3:
                    print("\n------------------------------------------------------\n| Error: This url cannot be found, please try again! |\n------------------------------------------------------\n")
                    url = input("Enter the youtube link you want to download: ")
                    downloader(url)
                try:
                    try_counter += 1
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        print("Getting video information...")
                        mp3_file = ydl.extract_info(url=url, download=False)
                        ydl.download([url])
                        break
                except:
                    if try_counter == 3:
                        continue
                    print("Something went wrong, trying again.")
        print("Download is complete!")
        os.startfile(rf"{downloads_path}/{mp3_file['title']}.mp3") # play the downloaded file automoatically for user convenience
    return

tkinter.Tk().withdraw()
url = input("Enter the youtube link you want to download: ")
downloads_path = filedialog.askdirectory(title = "Choose a location to download your songs to")
print("Download path: " + downloads_path)
if not downloads_path:
    exit("\n---------------------------------\n| No path given. Shutting down! |\n---------------------------------\n")
downloader(url)
