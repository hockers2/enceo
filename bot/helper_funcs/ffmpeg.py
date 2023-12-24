import logging
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

import asyncio
import os
import time
import re
import json
import subprocess
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.helper_funcs.display_progress import (
  TimeFormatter
)
from bot.localisation import Localisation
from bot import (
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    DOWNLOAD_LOCATION,
    crf,
    resolution,
    audio_b,
    preset,
    codec,
    watermark,
    pid_list
)

async def convert_video(video_file, output_directory, total_time, bot, message, chan_msg):
    # https://stackoverflow.com/a/13891070/4723940
    kk = video_file.split("/")[-1]
    aa = kk.split(".")[-1]
    out_put_file_name = kk.replace(f".{aa}", ".mkv")
    #out_put_file_name = video_file + "_compressed" + ".mkv"
    progress = output_directory + "/" + "progress.txt"
    with open(progress, 'w') as f:
      pass
   ## -metadata title='@HG_Anime [Join https://t.me/HG_Anime]' -vf drawtext=fontfile=Italic.ttf:fontsize=20:fontcolor=black:x=15:y=15:text='HG Anime'
   ## "-metadata", "title=@HG_Anime", "-vf", "drawtext=fontfile=njnaruto.ttf:fontsize=20:fontcolor=black:x=15:y=15:text=" "",
     - vf
     - eq=gamma=1.4:saturation=
    #lol 😂
    crf.append("28")
    codec.append("libx264")
    resolution.append("854x480")
    preset.append("veryfast")
    audio_b.append("40k")
    watermark.append('-vf "drawtext=fontfile=font.ttf:fontsize=29:fontcolor=white:bordercolor=black@0.50:x=w-tw-10:y=10:box=1:boxcolor=black@0.5:boxborderw=6:text= "Telegram~@HG_Anime')
    file_genertor_command = f"""ffmpeg -hide_banner -loglevel quiet -progress '''{progress}''' -i '''{video_file}''' -filter_complex "drawtext=fontfile=njnaruto(1).ttf:fontsize=20:fontcolor=white:bordercolor=black@0.50:x=w-tw-10:y=10:box=1:boxcolor=black@0.5:boxborderw=6:text='':enable='between(t,0,15)':alpha='if(lt(t,14)\,1\,if(lt(t\,15)\,(1-(t-14))/1\,0))', drawtext=fontfile=njnaruto(1).ttf:text='':bordercolor=black@0.50:borderw=5:fontcolor=white:fontsize=20:x=w-((2*w-200)*(t-615)/60):y=lh+0.5:enable='between(t, 615,680)':alpha='if(lt(t,679)\,1\,if(lt(t\,680)\,(1-(t-679))/1\,0))'[out1]" -metadata:s:a:0 title="" -metadata:s:a:1 title="" -metadata:s:s:0 title="" -metadata:s:s:1 title="" -map [out1] -map 0:a? -map 0:s? -map 0:t? -metadata title="ᴛᴇʟᴇɢʀᴀᴍ~ʜɢ_ᴀɴɪᴍᴇ" -c:v {codec[0]} -crf {crf[0]} -c:s copy -pix_fmt yuv420p -s {resolution[0]} -b:v 150k -c:a libopus -b:a {audio_b[0]} -preset {preset[0]}  '''{out_put_file_name}''' -y"""
 #Done !!
    COMPRESSION_START_TIME = time.time()
    process = await asyncio.create_subprocess_shell(
          file_genertor_command,
          # stdout must a pipe to be accessible as process.stdout
           stdout=asyncio.subprocess.PIPE,
           stderr=asyncio.subprocess.PIPE,
          )
    #stdout, stderr = await process.communicate()

    LOGGER.info("ffmpeg_process: "+str(process.pid))
    pid_list.insert(0, process.pid)
    status = output_directory + "/status.json"
    with open(status, 'r+') as f:
      statusMsg = json.load(f)
      statusMsg['pid'] = process.pid
      statusMsg['message'] = message.message_id
      f.seek(0)
      json.dump(statusMsg,f,indent=2)
    # os.kill(process.pid, 9)
    isDone = False
    while process.returncode != 0:
      await asyncio.sleep(3)
      with open(DOWNLOAD_LOCATION + "/progress.txt", 'r+') as file:
        text = file.read()
        frame = re.findall("frame=(\d+)", text)
        time_in_us=re.findall("out_time_ms=(\d+)", text)
        progress=re.findall("progress=(\w+)", text)
        speed=re.findall("speed=(\d+\.?\d*)", text)
        if len(frame):
         frame = int(frame[-1])
        else:
          frame = 1;
        if len(speed):
          speed = speed[-1]
        else:
          speed = 1;
        if len(time_in_us):
          time_in_us = time_in_us[-1]
        else:
          time_in_us = 1;
        if len(progress):
          if progress[-1] == "end":
            LOGGER.info(progress[-1])
            isDone = True
            break
        execution_time = TimeFormatter((time.time() - COMPRESSION_START_TIME)*1000)
        elapsed_time = int(time_in_us)/1000000
        difference = math.floor( (total_time - elapsed_time) / float(speed) )
        ETA = "-"
        if difference > 0:
          ETA = TimeFormatter(difference*1000)
        percentage = math.floor(elapsed_time * 100 / total_time)
        progress_str = "♻️ <b>ᴘʀᴏᴄᴇssɪɴɢ:</b> {0}%\n[{1}{2}]".format(
            round(percentage, 2),
            ''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]),
            ''.join([UN_FINISHED_PROGRESS_STR for i in range(10 - math.floor(percentage / 10))])
            )
        stats = f'⚡ <b>ᴇɴᴄᴏᴅɪɴɢ ɪɴ ᴘʀᴏɢʀᴇss</b>\n\n' \
                f'🕛 <b>ᴛɪᴍᴇ ʟᴇғᴛ:</b> {ETA}\n\n' \
                f'{progress_str}\n'
        