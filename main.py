import datetime
import json
import re
import pyttsx3
import random as rd
import requests
import threading
import time
import webbrowser
import wolframalpha
from urllib.request import urlopen
import geocoder
import speech_recognition as sr
from kivy.clock import mainthread, Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatIconButton
from pyjokes import pyjokes
from wikipedia import wikipedia

Window.size = (325, 600)
intents = requests.get("http://127.0.0.1:5000/intents").json()
assname = ("I am TAR U C Voice Assistance.")
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 190)  # default rate is 200 word per minute
engine.setProperty('voice', voices[0].id)  # allow to change the voices
r = sr.Recognizer()
r.dynamic_energy_threshold = True
KV = '''
# Menu item in the DrawerList list.
ScreenManager:
    HomeScreen:
    ProfileScreen:

<HomeScreen>:
    name:'home'
    canvas.before:
        Color:
            rgba: 56/255,40/255,81/255,1
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        orientation:'vertical'
        MDToolbar:
            title : 'Voice Assistance'
            right_action_items : [["dots-vertical", lambda x : print('Test press')]]
            # right_action_items : [["dots-vertical", lambda x : app.set_screen('TODO')]]
        MDBoxLayout:
            size_hint_y:.25
            pos: (0,root.height - 60)
            padding:dp(15)
            MDBoxLayout:
                orientation:"vertical"
                MDGridLayout:
                    cols:2
                    padding:[dp(35),dp(15),dp(20),dp(15)]
                    spacing:dp(22)
                    MDLabel:
                        text:"Chue Jun Wen"
                        font_style:"H5"
                        color: 1,1,1,1
                        halign:'center'
                    MDIconButton:
                        user_font_size: "10sp"
                        on_press: root.manager.current = 'profile'
                        icon:"arrow_right.png"
                MDGridLayout:
                    cols:2
                    padding:[dp(30),dp(15),dp(15),dp(5)]
                    spacing:dp(20)
                    MDTextFieldRound:
                        id: searchInput
                        padding:dp(10)
                        hint_text: "Search now"
                        width:250
                        on_text:app.change_text(self)
                        normal_color : [1,1,1,1]
                    MDIconButton:
                        user_font_size: "5sp"
                        spacing:dp(5)
                        on_press: app.call_assistance()
                        icon:"microphone.png"
                MDFillRoundFlatIconButton:
                    icon:'magnify'
                    text:'Search'
                    pos_hint:{'center_x':0.5, 'center_y':0.5}
                    size_hint: None, None
                    font_size: 14
                    on_press: app.call_search() 
        MDGridLayout:
            size_hint_y:.5
            cols:2
            padding:[dp(15),dp(5),dp(15),dp(235)]
            spacing:dp(15)

            ElementCard:
                image:"notification.png"
                text:"Maintenance"
                # on_press:  root.manager.current = 'profile'
            ElementCard:
                image:"notification.png"
                text:"Notification"
                # on_press:  print("test")

<ProfileScreen>:
    name:'profile'
    MDBoxLayout:
        orientation : 'vertical'
        pos: (0,root.height - 60)
        MDToolbar:
            title : 'Voice Assistance'
            left_action_items : [["arrow-left", lambda x : app.set_screen('home')]]


    Image:
        size_hint: None, None
        size: 250, 250
        pos_hint:{'center_x':0.5, 'center_y':0.65}
        source: "profile.jpg"
    MDLabel:
        text: "Chue Jun Wen"
        font_style: "Subtitle1"
        size_hint_y: None
        halign: 'center'
        valign: 'middle'
        pos_hint:{'center_x':0.5, 'center_y':0.4}
        height: self.texture_size[1]
    MDLabel:
        text: "Email: chuejw-wm18@student.tarc.edu.my"
        size_hint_y: None
        halign: 'center'
        valign: 'middle'
        pos_hint:{'center_x':0.5, 'center_y':0.35}
        font_style: "Caption"
        height: self.texture_size[1]
    MDLabel:
        text: "Gender: Male"
        size_hint_y: None
        halign: 'left'
        valign: 'middle'
        padding_x: 100
        pos_hint:{'center_x':0.5, 'center_y':0.3}
        font_style: "Caption"
        height: self.texture_size[1]
    MDLabel:
        text: "Phone: 012-9301876"
        size_hint_y: None
        halign: 'left'
        valign: 'middle'
        padding_x: 100
        pos_hint:{'center_x':0.5, 'center_y':0.25}
        font_style: "Caption"
        height: self.texture_size[1]
    MDFillRoundFlatIconButton:
        on_press: root.manager.current = 'home'
        text:"Logout"
        icon:"logout"
        pos_hint:{'center_x':0.5, 'center_y':0.1}


<ElementCard@MDCard>:
    md_bg_color:69/255,55/255,86/255,1
    padding:dp(15)
    spacing:dp(15)
    radius:dp(25)
    ripple_behavior: True
    image:''
    text:""
    items_count:""
    subtext:''

    orientation:'vertical'
    Image:
        source:root.image
    MDBoxLayout:
        orientation:'vertical'
        MDLabel:
            halign:"center"
            text:root.text
            color: 1,1,1,1
            font_style:"Body1"
        MDLabel:
            halign:"center"
            font_style:"Caption"
            text:root.subtext
        MDLabel:
            halign:"center"
            text:root.items_count
<Popup>:
    first_label: 'Voice Assistance'
    size_hint:(None,None)
    size:(300,300)
    auto_dismiss:False
'''


class HomeScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class Popup(Popup):
    labelID = StringProperty('Trying to get this to update')
    pop_is_open = False

    def close(self):
        self.dismiss()

    def on_open(self):
        self.pop_is_open = True

    def on_dismiss(self):
        self.pop_is_open = False

class VoiceAssistance(MDApp):
    pop = Popup(title='Voice Assistance',
                auto_dismiss=False,
                size_hint=(None, None),
                size=(300, 400),
                background_color=(0, 0, 0, 1)
                )
    searching_pop = Popup(title='Search',
                          auto_dismiss=False,
                          size_hint=(None, None),
                          size=(300, 300),
                          background_color=(0, 0, 0, 1)
                          )
    first_lbl = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.25},
                          size_hint_y=None,
                          height=30,
                          readonly=True,
                          size=(120, 150),
                          font_size=sp(12)
                          )
    second_lbl = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.75},
                           height=30,
                           size_hint_y=None,
                           readonly=True,
                           size=(120, 150),
                           font_size=sp(12)
                           )
    search_lbl = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.60},
                           height=30,
                           size_hint_y=None,
                           readonly=True,
                           size=(120, 230),
                           font_size=sp(12)
                           )
    search_text = ""
    status_assistance = False
    paused = False
    stop = threading.Event()

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Red"
        # VA Layout initialization
        layoutAssistance = BoxLayout(orientation='vertical')
        floatLayoutAssistance = FloatLayout(size=(300, 300))
        btnAssistance = ImageButton(
            source='animation.gif',
            on_press=lambda x: self.close_assistance(),
            size_hint=(None, None),
            size=(80, 80),
            pos_hint={'center_x': 0.5},
            anim_loop=-1,
            anim_delay=0,
        )
        floatLayoutAssistance.add_widget(self.second_lbl)
        floatLayoutAssistance.add_widget(self.first_lbl)
        layoutAssistance.add_widget(floatLayoutAssistance)
        layoutAssistance.add_widget(btnAssistance)

        # Search Layout initialization
        layoutSearch = BoxLayout(orientation='vertical')
        floatLayoutSearch = FloatLayout(size=(300, 300))
        btnClose = MDFillRoundFlatIconButton(
            # source='animation.gif',
            on_press=lambda x: self.close_search(),
            size_hint=(None, None),
            size=(80, 80),
            pos_hint={'center_x': 0.5},
            text='Close',
            icon='close'
            # anim_loop=-1,
            # anim_delay=0,
        )
        floatLayoutSearch.add_widget(self.search_lbl)
        layoutSearch.add_widget(floatLayoutSearch)
        layoutSearch.add_widget(btnClose)

        self.pop.add_widget(layoutAssistance)
        self.searching_pop.add_widget(layoutSearch)
        return Builder.load_string(KV)

    def set_screen(self, screen_name):
        self.root.current = screen_name

    def close_assistance(self):
        self.pop.dismiss()
        self.status_assistance = False
        self.start_third_thread()
        threading.Thread(target=self.listen_wake_word).start()

    def close_search(self):
        self.searching_pop.dismiss()
        self.search_lbl.text = ""
        self.start_third_thread()
        threading.Thread(target=self.listen_wake_word).start()

    def call_assistance(self):
        self.pop.open()
        self.status_assistance = True
        self.clear_message()
        self.start_second_thread()

    def change_text(self, instance):
        self.search_widget = instance
        self.search_text = instance.text

    def call_search(self):
        if self.search_text is not "":
            self.stop_listening(wait_for_stop=False)
            self.search_lbl.text = ""
            self.searching_pop.open()
            self.paused = False
            self.thread_search = threading.Thread(target=self.check_query, args=(self.search_text.lower(), "SEARCH"))
            self.thread_search.start()
            self.search_widget.text = ""

    def start_second_thread(self):
        threading.Thread(target=self.start_assistance).start()

    def start_third_thread(self):
        threading.Thread(target=self.stop_speak).start()

    @mainthread
    def refresh(self, text, to):
        if to == "ASSISTANCE":
            if self.first_lbl.text == "":
                self.first_lbl.text = str(text)
            else:
                self.second_lbl.text = self.first_lbl.text
                self.first_lbl.text = str(text)
        else:
            self.search_lbl.text = str(text)

    def clear_message(self):
        self.first_lbl.text = ""
        self.second_lbl.text = ""
        self.search_lbl.text = ""

    def wishMe(self, to):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speech = "Good Morning Sir!"

        elif hour >= 12 and hour < 18:
            speech = "Good Afternoon Sir!"
        else:
            speech = "Good Evening Sir!"
        self.refresh(speech + " " + assname + " How can i Help you, Sir", to)
        self.speak(speech + assname + "How can i Help you, Sir")

    def speak(self, text):
        words = text.split("\n")
        while words:
            if not self.paused and (self.pop.pop_is_open or self.searching_pop.pop_is_open):
                word = words.pop(0)
                engine.say(word)
                engine.runAndWait()
            elif self.paused:
                words = []

    def stop_speak(self):
        self.paused = True

    def start_assistance(self):
        self.pop.on_open()  # call for setting value
        self.paused = False  # for ensure next function can speech
        self.wishMe("ASSISTANCE")
        while self.status_assistance and self.pop.pop_is_open:
            self.paused = False
            query = self.takeCommand().lower()
            self.check_query(query, "ASSISTANCE")

    def check_query(self, query, to):
        if 'wikipedia' in query:
            self.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            print(query)
            if query is not None:
                try:
                    results = wikipedia.summary(query)
                    self.speak("According to Wikipedia")
                    print(results)
                    self.refresh("Assistance: " + results, to)
                    self.speak(results)
                except Exception as e:
                    e = 'Please provide more information that you want to know'
                    print(e)
                    self.refresh("Assistance: " + e, to)
                    self.speak(e)

        elif ('what is' in query and 'what is your name' not in query) or (
                'who is' in query and 'who is me' not in query):
            self.refresh("Assistance: Searching " + query + " in google now", to)
            self.speak("searching " + query + " in google now")
            webbrowser.open_new_tab("https://www.google.com/search?q=" + query.replace('what is', ''))

        elif 'open youtube' in query:
            self.refresh("Assistance: " + "tell me what you want to search in youtube\n", to)
            self.speak("tell me what you want to search in youtube\n")
            query = self.takeCommand().lower()
            self.refresh("Assistance: Searching " + query + " in youtube now", to)
            self.speak("searching " + query + " in youtube now")
            webbrowser.open_new_tab("https://www.youtube.com/results?search_query=" + query)

        elif 'open google' in query:
            self.refresh("Assistance: Here you go to Google", to)
            self.speak("Here you go to Google\n")
            webbrowser.open_new_tab("https://www.google.com")

        elif 'what time now' in query or \
                'current time' in query or \
                'current date and time' in query or \
                'current date' in query:
            if 'what time now' in query or 'current time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M %p")
            else:
                strTime = datetime.datetime.now().strftime("%H:%M%p of %d %B %Y")
            self.refresh("Assistance: " + "The time is " + strTime, to)
            self.speak("the time is" + strTime.replace(':', ''))

        elif 'how are you' in query:
            print("I am fine, Thank you")
            print("How are you, Sir")
            self.refresh("Assistance: I am fine, Thank you. How are you, Sir", to)
            self.speak("I am fine, Thank you")
            self.speak("How are you, Sir")

        elif 'fine' in query:
            self.refresh("Assistance: " + "It's good to know that your fine", to)
            self.speak("It's good to know that your fine")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            self.refresh("Assistance: " + joke, to)
            self.speak(joke)

        elif "calculate" in query:
            app_id = "EW266K-HTWUT92JP8"
            client = wolframalpha.Client(app_id)
            query = query.replace('calculate', '').strip()
            print(query)
            res = client.query(query)
            answer = next(res.results).text
            print("The answer is " + answer)
            self.refresh("Assistance: " + "The answer is " + answer, to)
            self.speak("The answer is " + answer)

        elif 'search' in query:
            query = query.replace("search ", "")
            self.refresh("Assistance: " + "Searching " + query + " in google now", to)
            self.speak("Searching " + query + "in google now")
            webbrowser.open_new_tab("https://www.google.com/search?q=" + query)

        elif 'play' in query:
            if 'play any music' in query or 'play music' in query:
                html_content = requests.get("https://www.youtube.com/results?search_query=music")
                position = rd.randint(0, 20)
            else:
                query = query.replace("play ", "")
                html_content = requests.get("https://www.youtube.com/results?search_query="+query)
                position = 0  # first result in searching
            self.refresh("Assistance: " + "Open music to you now.", to)
            self.speak("Open music to you now.")
            search_results = re.findall(r'"\/watch\?v=(.{11})', html_content.text)
            music_id = search_results[position]
            webbrowser.open_new("http://www.youtube.com/watch?v={}".format(music_id))

        elif 'news' in query:
            try:
                jsonObj = urlopen(
                    '''https://newsapi.org/v2/top-headlines?country=my&apiKey=4764dea8b356464bafad667bd831126b''')
                data = json.load(jsonObj)
                count = 1
                self.refresh("Assistance: Here are some top news from the times of malaysia", to)
                self.speak('here are some top news from the times of malaysia')
                print('''=============== TIMES OF MALAYSIA ============''' + '\n')

                for new in data['articles']:
                    if not self.paused and (self.pop.pop_is_open or self.searching_pop.pop_is_open):
                        title = str(new['title'])
                        description = str(new['description'])
                        url = str(new['urlToImage'])
                        if url != "None":
                            webbrowser.open_new(url)
                            url = "No photo url provided."
                        if description == "None":
                            description = "No description provided."
                        print(title + "\n" + description + "\n" + url + "\n")
                        self.refresh("Assistance: " + "Title of news is " + title + "\nDescription: " + description, to)
                        self.speak(title+"\n"+description)
                        time.sleep(2)
                        count += 1
                        # validate numbers of news has been speak out
                        if count > 4:
                            break
                    else:
                        self.paused = True
                        break
            except Exception as e:
                print(str(e))

        elif "where is" in query or\
                "how to go" in query or \
                    "locate to" in query:
            query = query.replace("where is", "").replace("how to go","").replace("locate to","")
            location = query.strip()
            self.refresh("Assistance: " + "User asked to Locate " + location, to)
            self.speak("User asked to Locate")
            self.speak(location)
            webbrowser.open("https://www.google.com/maps/search/" + location)

        elif "hi" in query:
            self.wishMe(to)

        elif "weather" in query:
            # get user current location address
            g = geocoder.ip('me')
            # get weather information
            api_key = "S7JJTUVZ2GPGA2DBZJCPYTAGW"
            weather_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
            complete_url = weather_url + g.city + "?unitGroup=us&key=" + api_key
            response = requests.get(complete_url)
            x = response.json()
            if x != None:
                y = x["days"][0]
                date = y["datetime"]
                current_temperature = "{:.2f}".format(float((int(y["temp"]) - 32) * 5 / 9))
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                weather_description = y["description"]
                result = "\nCurrent city: " + g.city +"\nTemperature: " + str(
                    current_temperature) + "°C\nAtmospheric pressure (in hPa unit): " + str(
                    current_pressure) + "\nHumidity (in percentage): " + str(
                    current_humidiy) + "\nDescription: " + str(weather_description)
                print(g.city)
                print(result)
                self.refresh("Assistance: " + result, to)
                self.speak(g.city)
                self.speak("current temperature is" + current_temperature + "°celsius")
                self.speak(weather_description)
            else:
                self.refresh("City Not Found", to)
                self.speak(" City Not Found ")

        # most asked question from google Assistant
        elif "will you be my girlfriend" in query or "will you be my boyfriend" in query:
            self.refresh("I'm not sure about, may be you should give me some time.", to)
            self.speak("I'm not sure about, may be you should give me some time")

        elif "how are you" in query:
            self.refresh("I'm fine, glad you me that.", to)
            self.speak("I'm fine, glad you me that")

        elif "i love you" in query:
            self.refresh("It's hard to understand.", to)
            self.speak("It's hard to understand")

        else:
            res = self.getResponse(query, intents)
            respon = rd.choice(res['responses'])
            self.refresh("Assistance: " + respon, to)
            print(respon)
            self.speak(
                respon.replace("TARUC", "TAR U C")
                    .replace("/", "or")
                    .replace("SAM", "S A M")
                    .replace("ATAR", "A T A R")
            )
            if "don't listen" in query \
                    or "stop listening" in query \
                    or "bye" in query \
                    or "goodbye" in query \
                    or "nice chatting with you" in query \
                    or "exit" in query \
                    or "close" in query:
                self.status_assistance = False
                self.close_assistance()
                self.close_search()

    def getResponse(self, query, intents_json):
        list_of_intents = intents_json['intents']
        result = None
        for i in list_of_intents:
            for a in i['patterns']:
                if (a.lower() in query.lower()):
                    result = i
                    # print(result['tag']) // For checking purpose
                    return result

        if result is None:
            result = i
        return result

    def takeCommand(self):
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            # remove noise from the audio resource
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            # speech_recognition_ai = SpeechRecognitionAI()
            # query = speech_recognition_ai.start_speech_recognition(debug=True)
            print("User said:" + query)
            self.refresh("User:" + query, "ASSISTANCE")
        except Exception as e:
            print(e)
            return "None"
        return query

    def on_start(self):
        threading.Thread(target=self.listen_wake_word).start()

    def listen_wake_word(self):
        self.listenBG = True
        while self.listenBG:
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in')
                if query == 'hello':
                    self.listenBG = False
                    self.call_assistance()
                else:
                    self.listenBG = True
            except Exception as e:
                print(e)

if __name__ == '__main__':
    VoiceAssistance().run()

