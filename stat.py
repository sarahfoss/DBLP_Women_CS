# -*- coding: utf-8 -*-
"""

@author: Sarah
"""
import json
import pandas as pd

     
df = pd.read_json('authorFemaleExtraDataClassified.json')

columns=["median", "mean"]
index=["Number of publications of female authors",
       "Number of pages per publications of female authors",
       "Number of authors per publications of female authors",
       "Position of female authors on publications"]
data = []
data.append([df['total publications'].median(), df['total publications'].mean()])
data.append([df['average pages'].median(), df['average pages'].mean()])
data.append([df['average authors'].median(), df['average authors'].mean()])
data.append([df['average position'].median(), df['average position'].mean()])

stats = pd.DataFrame(data, columns=columns, index=index)

stats.to_csv("stats.csv")

    
