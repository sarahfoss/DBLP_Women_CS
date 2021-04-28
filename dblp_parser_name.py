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


filename = 'DBLP/dblpcp.xml'

# create/empty the db
db = TinyDB('dbnamesonly.json')
db.truncate()

# incrementally load the DBLP data 
tree = et.iterparse(filename, load_dtd=True)

Author = Query()

# parse the DBLP xml database
for action, elem in tree:
    
    if elem.tag  == "author":
        # add the author string to the tinyDB database
        ath = elem.text
        if not db.contains(Author.name == ath):
            db.insert({'name': ath})

      


    

        
        


