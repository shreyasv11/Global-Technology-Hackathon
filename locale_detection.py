import requests
import unicodedata2
import google.cloud.texttospeech as tts
import os
import json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="involuted-ratio-349909-1bd15b3693bf.json"

def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set
client = tts.TextToSpeechClient()
response = client.list_voices()
available = unique_languages_from_voices(response.voices)
available = sorted(list(available))
available[19], available[20] = available[20], available[19]
available[34], available[35] = available[35], available[34]
available[38], available[39] = available[39], available[38]

languages = []
for i in available:
    languages.append(i[:len(i)-3])

file = 'shortened.json'
with open(file, 'r') as f:
    shortened = json.load(f)
countries = []
for i in shortened:
    countries.append(i[-2:])

file = 'mapping.json'
with open(file, 'r') as f:
    mapping = json.load(f)
    

def detect_language(name):
    file = 'lang_dict.json'
    with open(file, 'r') as f:
        dic = json.load(f)
    ch = name[0]
    temp = unicodedata2.name(ch)
    temp = temp.split(' ')
    key = temp[0]
    if key in dic:
        return dic[key]
    return 'en'
    


def name_to_locale(name, pref_name=None):
    
    if pref_name:
        pref_name.lstrip(' ')
        lang = detect_language(pref_name)
        if lang != 'en':
            j = languages.index(lang)
            return available[j]
    
    try:
        name = name.lower()
        name = name.strip()
        name.replace('.','')
        name = name.replace(" ", "%20")
        url = "https://v2.namsor.com/NamSorAPIv2/api2/json/country/" + name
        headers = {
         "Accept": "application/json",
         "X-API-KEY": "b9bdc7453da5291f8d606c3d790f1836"
        }
        response = requests.request("GET", url, headers=headers)
        js = response.json()
        coun = js['country']
    except:
        coun = 'US'
    if coun in mapping:
        coun = mapping[coun]
    else:
        coun = 'US'
    if coun not in countries:
        coun = 'US'
    j = countries.index(coun)
    return shortened[j]