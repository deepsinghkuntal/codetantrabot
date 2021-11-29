import speech_recognition as sr

def detectAudio(): #function that is called to convert audio into text
    r = sr.Recognizer()
    mic = sr.Microphone(device_index = 2)
    result = ""
    try:
        with mic as source:
            audio = r.listen(source , timeout=5 , phrase_time_limit= 15 )
        print("Analyzing for the text")
        result = r.recognize_google(audio)
        print(result)
    except:
        print("Its all good speak something into the mic")


def micro():
    recog = sr.Recognizer()
    mic = sr.Microphone()

    with mic:
        print("Listening")
        audio = recog.listen(mic, timeout=5, phrase_time_limit=15)

    recognized = recog.recognize_google(audio)
    print(recognized)
    return recognized

text = micro()