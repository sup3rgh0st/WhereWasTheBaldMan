# WhereWasTheBaldMan?
 Find out what levels your favorite Twitch Streamer played last. Currently configured to pull the latest video from everyone's favorite bad man, Aurateur.
 Uses pyTesseract to scrub through downloaded Twitch VODs hunting for Mario Maker level ids. After its done searching, it will spit out a text file with the code and the timestamp where it first appeared in the video.
 The script will early bail if there is already a text output associated with the VOD that's queued to be searched.

## Setup:
  Change "pytesseract.pytesseract.tesseract_cmd =" to point to your installation path of Tesseract
  Run the python script with Python 3 in its own folder with a copy of FFMPEG.exe next to it. Change "channel_name =" to point to the Twitch streamer of choice. 

## Dependencies:
  Use 'pip install' for everything; it runs on python magic: cv2, twitchdl, youtube_dl, PIL, pytesseract* (Requires some setup, follow the instructions on https://pypi.org/)
 
cheer100 Happy Birthday! 🙌🙌🙌🙌🙌🙌🙌🙌🙌 RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
