
import json

dic = {'ARABIC':'ar','CYRILLIC':'ru','BENGALI':'bn','LATIN':'en','CJK':'cmn','GREEK':'el',
       'GUJARATI':'gu','DEVANAGARI':'hi','KANNADA':'kn','MALAYALAM':'ml','GURMUKHI':'pa',
       'TAMIL':'ta','TELUGU':'te','THAI':'th'}

file = 'lang_dict.json'
with open(file, 'w') as f: 
    json.dump(dic, f)

#with open(file, 'r') as f:
#    shortened = json.load(f)