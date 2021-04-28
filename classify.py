# -*- coding: utf-8 -*-
"""

@author: Sarah Foss

 Load the models and the author information
 
 Convert the title strings into count vectors and TF-IDF vectors
 
 Predict the field of study for each author using four models:
     Naive Bayes classifer with count vectors
     Naive Bayes classifer with TF-IDF vectors
     Logistic regression classifier with Count Vectors
     Logistic regression classifier with TF-IDF vectors

 Export result to CSV for visualization with Tableau
"""
import joblib, json
import pandas as pd

db = 'authorData.json'


# load the encoder, vectors, and models
encoder = joblib.load('classifiers/encoder.joblib')

count_vect = joblib.load('classifiers/count_vect.joblib')
tfidf_vect = joblib.load('classifiers/tfidf_vect.joblib')

naive_bayes_cv = joblib.load('classifiers/naive_bayes_cv.joblib')
naive_bayes_tfidf = joblib.load('classifiers/naive_bayes_tfidf.joblib')
linear_classifier_cv= joblib.load('classifiers/logistic_regression_cv.joblib')
linear_classifier_tfidf= joblib.load('classifiers/logistic_regression_tfidf.joblib')


data = []
with open(db) as json_data:
      jsonData = json.load(json_data)
      for item in jsonData:
          data.append(item)


df = pd.DataFrame(data) 

# convert the title strings into count vectors
title_count =  count_vect.transform(df['cleanedTitles'])
title_tfidf =  tfidf_vect.transform(df['cleanedTitles'])

results = df.copy(deep=True)
#results.drop(['cleanedTitles','count'], axis=1, inplace=True)

# Predict the author's field of study with Naive Bayes classifer with count vectors
results['naive_bayes_cv_predition'] = encoder.inverse_transform(naive_bayes_cv.predict(title_count))

# Predict the author's field of study with Naive Bayes classifer with TF-IDF vectors
results['naive_bayes_tfidf_prediction'] = encoder.inverse_transform(naive_bayes_tfidf.predict(title_tfidf))

# Predict the author's field of study with logistic regression classifier with Count Vectors
results['logistic_regression_cv_prediction'] = encoder.inverse_transform(linear_classifier_cv.predict(title_count))

# Predict the author's field of study with logistic regression classifier with TF-IDF vectors
results['logistic_regression_tfidf_prediction'] = encoder.inverse_transform(linear_classifier_tfidf.predict(title_tfidf))

#results.to_json('authorFemaleExtraDataClassified.json', orient="records", indent=4)
results.to_csv('results.csv',encoding="utf-8")

