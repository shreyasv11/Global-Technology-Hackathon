import sys
import os
import google.cloud.texttospeech as tts
from locale_detection import name_to_locale

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="involuted-ratio-349909-1bd15b3693bf.json"

#Returns all list of unique languages given a voice
def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set

#Returns language_codes/locales that GCP supports
def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)
    return sorted(list(languages))

#Returns the genders of voices supported for the language_code given
def list_genders(language_code):
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    voices = sorted(response.voices, key=lambda voice: voice.name)
    return sorted(list(set("MALE" if voice.ssml_gender==1 else "FEMALE" for voice in voices if voice.language_codes==[language_code])))
    
#Returns available voices - language_code must be one of list_languages() , ssml_gender must be one of list_languages(language_code)
def list_voices(language_code,ssml_gender):
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    voices = sorted(response.voices, key=lambda voice: voice.name)
    return [voice.name for voice in voices if voice.ssml_gender==(1 if ssml_gender=="MALE" else 2) and "Wavenet" in voice.name and voice.language_codes==[language_code]]

#The following is a method which takes the name and voice as inputs and returns the audio output as bytes (called by the FLASK Application)
#voice_name should be one of list_voices() method and pitch should be in range[-20.0,20.0] (inclusive) and speed should be in range[0.25,4.0] (inclusive)
def text_to_wav(text,voice_name=None,pitch=0,speed=1):
    if voice_name is None:
        locale = name_to_locale(text)
        gender=list_genders(locale)[0]
        voice_name=list_voices(locale,gender)[0]
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16,pitch=pitch,speaking_rate=speed)
    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content