# import io
# from gtts import gTTS
# from pydub import AudioSegment
# from pydub.playback import play

# def speak(text, speed=1.3): 
    
#     tts = gTTS(text=text, lang="en", slow=False)

#     mp3_buffer = io.BytesIO()

#     tts.write_to_fp(mp3_buffer)

#     mp3_buffer.seek(0)

#     audio = AudioSegment.from_mp3(mp3_buffer)

#     faster_audio = audio.speedup(playback_speed=speed)

#     play(faster_audio)

from gtts import gTTS
import os

def speak(text, speed=1.2):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("response.mp3")
        
        os.system(f"ffmpeg -i response.mp3 -filter:a 'atempo={speed}' fast.mp3 -y -loglevel quiet")
        # -i response.mp3 = input file
        # -filter:a 'atempo=1.3' = speed up audio by 1.3x
        # fast.mp3 = sped up output file
        # -y = overwrite without asking
        # -loglevel quiet = print nothing to terminal
        
        os.system("mpg123 -q fast.mp3")
        # play the sped up version quietly
        
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")
        if os.path.exists("fast.mp3"):
            os.remove("fast.mp3")
        # clean up both files after playing
        
    except Exception as e:
        print(f"[Speaker error: {e}]")