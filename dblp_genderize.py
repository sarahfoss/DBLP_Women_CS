# -*- coding: utf-8 -*-
"""

@author: Sarah Foss

 Iterate through the author & title tinyDB
 generated with dblp_parser.py.
 
 Using Genderize.io's API, predict the author's
 gender using their first name.
 
 Because of the daily limit of 1000 gender prediction,
 save the already processed names and gender info into a JSON file, 
 then, retrieve the name and info from the JSON file if it has 
 already been predicted.
 
 Clean the titles list string by translating to english if necessary,
 set to lowercase, remove non-alphabetic characters, remove stop word,
 and stem the words.
 
 
"""

import requests, json, re
from tinydb import TinyDB, Query
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
from langdetect import detect

# API key from DeepL Pro (language translation)
key = "401d5e0d-b25c-3c35-38df-66282b9de986"

# function to remove stop-words from a string containing 1 or more words
stop_words = set(stopwords.words('english')) 
def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in stop_words])

# function to stem word from a string containing 1 or more words
stem = PorterStemmer()
def stem_words(text):
    return " ".join([stem.stem(word) for word in text.split()])


author = []
authorFemale = []

db = TinyDB('names.json')
FName = Query()


with open('db.json') as json_data:
    
    # load an entry from the tinyDB
    jsonData = json.load(json_data) 
    for data in jsonData['_default'].values():
        if 'name' in data:
            
            # retrieve the first name of the author
            firstName = data['name'].split(' ', 1)[0]
            
            # if the first name has not alredy been processed,
            # predict the gender info from Genderize.io API
            # and save the info into tinyDB
            if not db.contains(FName.name == firstName):
                url = "https://api.genderize.io?name="+firstName
                response = requests.get(url, timeout=5)
                genderInfo = response.json()
                
                try:
                    if genderInfo['gender'] is None:
                        genderInfo['gender'] = "None"
                    db.insert({
                        "name": firstName,
                        "gender":genderInfo['gender'],
                        "probability":genderInfo['probability'],
                        "count":genderInfo['count']
                        })
                
                except:
                    #print(genderInfo, "break")
                    continue
            
            # otherwise, load the info from tinyDB
            else:
                try:
                    item = db.get(FName.name == firstName)
                    item = str(item)
                    item = item.replace("\'", "\"")
                    genderInfo = json.loads(item)
                except:
                    #print(genderInfo, "break")
                    continue
            
            if data['title'] is not None:
                cTitles = data['title']
                translation = ""
                try:
                    # detect the language of the title,
                    # if it is not in english, try to translate it
                    # using the DeepL API
                    lang = detect(cTitles) 
                    if lang != 'en':
                        url = "https://api.deepl.com/v1/translate?auth_key="+key+"&text="+cTitles+"&target_lang=EN"
                        response = requests.get(url, timeout=5)
                        trans = response.json()
                        cTitles = trans['translations'][0]['text']
                        print(cTitles)
                        translation = cTitles
                except Exception as e: 
                    print(e, "ERROR")

                # clean the titles further by set them
                # to lower case, removing non-alphabetic characters,
                # removing stop words and stemming
                cTitles = cTitles.lower()    
                cTitles = cTitles.strip()
                cTitles = re.sub("[^A-Za-z]+", ' ', cTitles)
                cTitles = remove_stopwords(cTitles)
                cTitles = stem_words(cTitles)
            gender = genderInfo['gender']
            if gender == "None":
                gender = "unknown"
            
            # create JSON object and store
            JSONobj = {
                "author":data['name'],
                #"titles":data['title'].strip("; ").split("; "),
                "titles":data['title'],
                "cleanedTitles":cTitles,
                "gender":gender,
                "probability":genderInfo['probability'],
                "count":genderInfo['count']
                
                }
            if translation != "":
                
                JSONobj["translation"] = translation
                
            author.append(JSONobj)
            if genderInfo['gender'] == 'female' and genderInfo['probability'] >= 0.9 and genderInfo['count'] > 20:
                authorFemale.append(JSONobj)
                    
with open('authorFemaleData.json', 'w') as outfile:
        json.dump(authorFemale, outfile, indent=4)
        
with open('authorData.json', 'w') as outfile:
        json.dump(author, outfile, indent=4)