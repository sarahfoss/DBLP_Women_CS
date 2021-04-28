# -*- coding: utf-8 -*-
"""

@author: Sarah Foss

 Gather all the author's names and publication titles
 from the DBLP xml file.
 
 Available at: https://dblp.org/xml/


"""

from lxml import etree as et
from tinydb import TinyDB, Query
from tinydb.operations import add


filename = 'DBLP/dblp.xml'

# create/empty the db
db = TinyDB('db.json')
db.truncate()

# incrementally load the DBLP data 
tree = et.iterparse(filename, load_dtd=True)

auth = []
Author = Query()

# parse the DBLP xml database
for action, elem in tree:
    
    if elem.tag  == "author":
        # add the author and empty title string to the tinyDB database
        ath = elem.text
        if not db.contains(Author.name == ath):
            db.insert({'name': ath, 'title': ''})
        auth.append(ath)
    elif elem.tag == "title":
        
        # add the title to the author's title string
        for x in auth:
            if elem.text is not None:
                title = elem.text + "; "
                db.update(add('title', title), Author.name == x)
        auth = []        


    

        
        


