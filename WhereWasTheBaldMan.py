import cv2
import twitchdl
import youtube_dl
import PIL
import subprocess
import pytesseract
import re
import time
import sqlite3

from PIL import ImageFilter, ImageEnhance
from PIL import Image
from twitchdl import commands
from twitchdl import twitch

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (D)\Tesseract-OCR\tesseract.exe'
max_download_attempts = 10
channel_name = "aurateur"

print("\nWhere Was The Bald Man? - sup3rgh0st\n")

print("Looking up the latest VOD on the channel '"+channel_name+"'...")

# Get the URL of the latest VOD...
print("Looking up user...")
user = twitch.get_user(channel_name)
if not user:
    print("User {} not found.".format(channel_name))
    exit()

print("Loading videos...")
videos = twitch.get_channel_videos(user["id"], 1, 0, "time")
count = len(videos['videos'])
if not count:
    print("No videos found")
    exit()

vod_id = videos['videos'][0]["_id"][1:]
vod_url = videos['videos'][0]["url"]

#test url
#vod_id = "532684964"
#vod_url = "https://www.twitch.tv/videos/532684964"

print("  VOD ID: " + vod_id)
print("  VOD URL: " + vod_url)

output_file = []
output_video_name = vod_id + ".mp4"
try:
    output_filename = vod_id + ".txt"
    output_file = open(output_filename, "x")
except:
    print("A Record of this VOD already exists! Exiting...")
    exit()

print("Found the latest VOD! Downloading...")

video = cv2.VideoCapture()
attempt_count = 1
while True:
    command = "youtube-dl " + vod_url + " -o " + output_video_name + " -c -R 10"
    print("  Starting SubProcess using the command '" + command + "'")
    p = subprocess.Popen(command, shell=True)
    p.wait()
    print ("Done downloading the VOD!")

    video = cv2.VideoCapture(output_video_name)
    if (video.isOpened() == False):
        print("Unable to open the downloaded video '" + output_video_name + "'")
        if attempt_count <= max_download_attempts:
            print("Retrying... Attempt " + str(attempt_count))
            continue
        else:
            print("Hit Max Retry Count. Quitting.")
            output_file.close()
            exit()
    break

video_fps = video.get(cv2.CAP_PROP_FPS)
video_framecount = video.get(cv2.CAP_PROP_FRAME_COUNT)
video_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
video_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

print("VOD FPS: " + str(video_fps))
print("VOD Framecount: " + str(video_framecount))
print("VOD Resolution: " + str(video_width) + " x " + str(video_height))

framecount = 0
level_code_list = {}
while(video.isOpened()):
    video.set(cv2.CAP_PROP_POS_FRAMES, framecount)
    ret, frame = video.read()
    framecount += (int(video_fps) * 2)
    
    if(framecount % (int(video_fps) * 100) == 0):
        print("Progress: "+ str(int((framecount/video_framecount)* 100) ) + "%")
    
    if ret == True:
        print(".", end = '', flush=True)
        pil_frame = Image.fromarray(frame)
        pil_frame = pil_frame.filter(ImageFilter.CONTOUR)
        pil_frame = pil_frame.filter(ImageFilter.SMOOTH)

        frame_text = pytesseract.image_to_string(pil_frame)
        level_code = re.search('[A-Z,0-9]{3}[-][A-Z,0-9]{3}[-][A-Z,0-9]{3}', frame_text)
        if(level_code):
            save_name = "frame" + str(framecount) + ".png"
            pil_frame.save(save_name, format='png')
            level_code = level_code.group(0)
            print(level_code)
            if level_code not in level_code_list:
                level_code_list[level_code] = framecount
    else:
        break

video.release()

print("\nFound " + str(len(level_code_list)) + " Levels Played!")

# Open a Connection to the ID Database
conn = sqlite3.connect('ids.db')
cur = conn.cursor()

for id in level_code_list:
    output_file.write(id + " @ " + str(level_code_list[id]) + "\n")
    print(id + " @ " + str(level_code_list[id]))
    
    # Write the Level ID to the ID Database
    db_ins = (id,vod_id,level_code_list[id])
    cur.execute("INSERT INTO IDS (LevelId, VodId, FrameNumber) VALUES(?,?,?)", db_ins)

conn.commit()
conn.close()

output_file.close()














