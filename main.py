from langchain.llms import GooglePalm
import speech_recognition as sr
import pyttsx3
import tkinter as tk
import threading

api_key = "Enter Your Api Key Here"
llm = GooglePalm(google_api_key=api_key, temperature = 0.5)
bot_speech = pyttsx3.init()
voices = bot_speech.getProperty('voices')
bot_speech.setProperty('voice',voices[1].id)
r = sr.Recognizer()

def listen_audio():
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                MyText = r.recognize_google(audio)
                text_label.config(text=f"Your Input: {MyText.strip()}")
                return MyText.strip()
        except sr.RequestError as e:
            return "could not request results!!"
        except sr.UnknownValueError:
            return "Unknown error occured!!"
        finally:
            status_label.config(text="")
        
        
def speak_Btn_action():
    ext = ["close"]
    print(f"Your END-KEY is close. The bot dissapears when you say it.")
    # while True:
        # prompt = input("Enter your prompt: ")
    prompt = listen_audio()
    print("Your Prompt: ", prompt)
    if prompt in  ext:
        txt = "I hope it is useful, feel free to ask more questions. Thankyou!"
        print(txt)
        text_label.config(text=f"Bot response: {txt}")
        root.update()
        bot_speech.say(txt)
        bot_speech.runAndWait()
        root.quit()
    else:
        bot = llm(prompt)
        print("Bot: ",bot)
        text_label.config(text=f"Bot response: {bot}")
        root.update()
        bot_speech.say(bot)
        bot_speech.runAndWait()

def speak_button_thread():
    thread = threading.Thread(target=speak_Btn_action)
    thread.start()

root = tk.Tk()
root.title("Speech To Speech Bot")
root.geometry("900x700")
listen_button = tk.Button(root, text="Speak", command=speak_button_thread)
listen_button.pack(pady=10)
status_label = tk.Label(root, text="")
status_label.pack(pady=5)
text_label = tk.Label(root, text="Bot response: ")
text_label.pack(pady=10)

root.mainloop()