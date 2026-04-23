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