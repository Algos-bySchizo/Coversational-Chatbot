import pyttsx3

def speak(text):
    engine = pyttsx3.init() # stars the text to speech engine 
    
    engine.setProperty("rate",155) #rate = speed of speech 175 = words per minute

    engine.setProperty("volume",1.0)

    engine.say(text)

    engine.runAndWait()
    engine.stop()