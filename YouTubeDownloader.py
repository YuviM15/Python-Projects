from pytube import YouTube

link = "https://youtu.be/wQ-GmWy_zmM?si=Us2txUpOaT4NYDGx"
yt = YouTube(link)

# print("Title:", yt.title)
print("Downloading...")

stream = yt.streams.filter(res="1080p", file_extension="mp4").first()
if stream is None:
    print("1080p not available, downloading the highest resolution.")
    stream = yt.streams.get_highest_resolution()

download_path = r"C:\Users\yuvra\Videos"
stream.download(download_path, filename="Testing.mp4")
print("Done!")

