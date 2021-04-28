# -*- coding: utf-8 -*-
"""

@author: Sarah
"""

import requests, json, time, re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
from langdetect import detect


# function to remove stop-words from a string containing 1 or more words
stop_words = set(stopwords.words('english')) 
def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in stop_words])

# function to stem word from a string containing 1 or more words
stem = PorterStemmer()
def stem_words(text):
    return " ".join([stem.stem(word) for word in text.split()])

authors = []
count = 0
filenumber = 1
with open('authorData.json') as json_data:
    jsonData = json.load(json_data)
    for info in jsonData:
        time.sleep(.5)
        name = info["author"]
        count += 1
        print(count, name)
        
        urlname = name.replace(" ", "_")
        urlpre = "https://dblp.org/search/publ/api?q=author:"
        urlpost = ":&format=json"
        url = urlpre + urlname + urlpost
        keepTrying = True
        tryCount = 0
        while keepTrying:
            try:
                response = requests.get(url, timeout=5)
                authorInfo = response.json()
                keepTrying = False
            except:
                time.sleep(5)
                if tryCount > 2:
                    break
                tryCount += 1
        
        total_pubs = int(authorInfo["result"]["hits"]["@total"])
        if total_pubs == 0:
            print(url)
            time.sleep(1)
            urlname = name.replace("_", " ")
            url = urlpre + urlname + urlpost
            keepTrying = True
            tryCount = 0
            while keepTrying:
                try:
                    response = requests.get(url, timeout=5)
                    authorInfo = response.json()
                    keepTrying = False
                except:
                    time.sleep(5)
                    if tryCount > 2:
                        break
                        tryCount += 1
            total_pubs = int(authorInfo["result"]["hits"]["@total"])
            if total_pubs == 0:
                print(name, "ERROR")
                print(url)
                continue
        
        author = {}
        author["name"] = name
        author["pid"] = "unknown"
        author["gender"] = info["gender"]
        author["gender probability"] = info["probability"]
        author["gender count"] = info["count"]
        author["total publications"] = total_pubs
        author["publications"] = list()
        
        publist = authorInfo["result"]["hits"]["hit"]
        
        totalPosition = 0
        pageCount = 0
        totalPages = 0
        total_authors = 0
        most_recent_pub = 0
        all_titles = ""
        
        for p_index in range(len(publist)):
        
            publication = authorInfo["result"]["hits"]["hit"][p_index]["info"]
            pubJSON = {}
            try:
                title = publication["title"]
                pubJSON["title"] = title
                if title != "":
                    translation = ""
                    try:
                        # detect the language of the title,
                        # if it is not in english, try to translate it
                        # using the DeepL API
                        lang = detect(title) 
                        if lang != 'en':
                            key = "401d5e0d-b25c-3c35-38df-66282b9de986"
                            url = "https://api.deepl.com/v1/translate?auth_key="+key+"&text="+title+"&target_lang=EN"
                            response = requests.get(url, timeout=5)
                            trans = response.json()
                            title = trans['translations'][0]['text']
                            pubJSON["translation"] = title

                    except Exception as e: 
                        print(e, "ERROR")

                # clean the titles further by set them
                # to lower case, removing non-alphabetic characters,
                # removing stop words and stemming
                title = title.lower()    
                title = title.strip()
                title = re.sub("[^A-Za-z]+", ' ', title)
                title = remove_stopwords(title)
                title = stem_words(title)
                all_titles += title + " "
                pubJSON["cleaned title"] = title
            except:
                pubJSON["title"] = "title unavailable"
                pubJSON["cleaned title"] = ""
            
            authlist = publication["authors"]["author"]
            pubJSON["authors"] = list()
            
            auth_position = 0
            if type(authlist) is list:
                for index in range(len(authlist)):
                    auth_info = {}
                    auth_info["name"] = authlist[index]["text"]
                    auth_info["pid"] = authlist[index]["@pid"]
                    if authlist[index]["text"] == name:
                        author["pid"] = authlist[index]["@pid"]
                        auth_position = index
                    pubJSON["authors"].append(auth_info)
            else:
                author["pid"] = authlist["@pid"]
                auth_info = {}
                auth_info["name"] = authlist["text"]
                auth_info["pid"] = authlist["@pid"]
                pubJSON["authors"].append(auth_info)
            
            total_authors += len(pubJSON["authors"])
            pubJSON["author position"] = auth_position
            totalPosition += auth_position
            
            for key in publication:
                if key != "title" and key != "authors":
                    pubJSON[key] = publication[key]
                    if(key == "pages"):
                        pageCount += 1
                        #print(pubJSON[key])
                        pageNo = pubJSON[key].split("-")
                        if(len(pageNo) == 2):
                            if ":" in pageNo[0]:
                                pageNo[0] = pageNo[0][pageNo[0].index(":")+1:]
                            if ":" in pageNo[1]:
                                pageNo[1] = pageNo[1][pageNo[1].index(":")+1:]
                            try:
                                pubJSON["total pages"] = int(pageNo[1])-int(pageNo[0])
                                totalPages += pubJSON["total pages"] 
                            except:
                                pageCount -= 1
                        else:
                            pubJSON["total pages"] = 1
                            totalPages += pubJSON["total pages"]
                    if key == "year":
                        try:
                            if int(publication["year"]) > most_recent_pub:
                                most_recent_pub = int(publication["year"])
                        except:
                            pass
                       
            author["publications"].append(pubJSON)
        if(pageCount != 0):
            average_pages = totalPages/pageCount
            author["average pages"] = average_pages
        author["average position"] = totalPosition/len(publist)
        author["average authors"] = total_authors/len(publist)
        if most_recent_pub > 0:
            author["recent publication"] = most_recent_pub
        author["title(string)"] = info["titles"]
        author["cleaned titles"] = info["cleanedTitles"]
        author["all titles"] = all_titles
        authors.append(author)
        if count % 1000 == 0:
            with open('extra_data/authorExtraData' + str(filenumber) +'.json', 'w') as outfile:
                json.dump(authors, outfile, indent=4)
                filenumber += 1
                authors = []

with open('extra_data/authorExtraData' + str(filenumber) +'.json', 'w') as outfile:
    json.dump(authors, outfile, indent=4) 