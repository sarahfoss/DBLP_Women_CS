# -*- coding: utf-8 -*-
"""

@author: Sarah Foss

 Split the Wikipedia dataset into training and
 validation datasets.
 
 Encode the labels into integers.
 
 Convert the content strings into count vectors and TF_IDF vectors
 
 Train a Naive-Bayes classifier with both the count vectors and TF_IDF vectors
 
 Train a multinomial logistic regression classifier with both the count 
 vectors and TF_IDF vectors
 
 Save the models into joblib objects


"""

import pandas as pd
from sklearn import model_selection 
from sklearn import preprocessing 
from sklearn import linear_model 
from sklearn import naive_bayes 
from sklearn import metrics 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.feature_extraction.text import CountVectorizer
import joblib


df = pd.read_csv("dataset.csv")

# split the dataset into training and validation datasets 
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(df['content'], df['field'])


# encode the labels into integers
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)
joblib.dump(encoder, 'classifiers/encoder.joblib')

# convert the content strings into count vectors
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(df['content'])
xtrain_count =  count_vect.transform(train_x)
xvalid_count =  count_vect.transform(valid_x)
joblib.dump(count_vect, 'classifiers/count_vect.joblib')

# convert the content strings into TF-IDF vectors
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(df['content'])
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)
joblib.dump(tfidf_vect, 'classifiers/tfidf_vect.joblib')


def train_model(classifier, train_vector, label, valid_vector):
    # train the classfier
    classifier.fit(train_vector, label)
    
    # predict with validation set
    predictions = classifier.predict(valid_vector)
    
    # return the models and the accuracy scores of the models
    return classifier, metrics.accuracy_score(predictions, valid_y)


# Train Naive Bayes classifer with count vectors
naive_bayes_cv, accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_count, train_y, xvalid_count)
print("Naive Bayes classifier with count vectors: ", accuracy)
joblib.dump(naive_bayes_cv, 'classifiers/naive_bayes_cv.joblib')

# Train Naive Bayes classifer with TF-IDF vectors
naive_bayes_tfidf, accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf)
print("Naive Bayes classifier with TF IDF Vectors: ", accuracy)
joblib.dump(naive_bayes_tfidf, 'classifiers/naive_bayes_tfidf.joblib')

# Train logistic regression classifier with count vectors
logistic_regression_cv, accuracy = train_model(linear_model.LogisticRegression(max_iter=10000), xtrain_count, train_y, xvalid_count)
print ("Logistic regression classifier with count vectors: ", accuracy)
joblib.dump(logistic_regression_cv, 'classifiers/logistic_regression_cv.joblib')

# Train logistic regression classifier with TF-IDF vectors
logistic_regression_tfidf, accuracy = train_model(linear_model.LogisticRegression(max_iter=10000), xtrain_tfidf, train_y, xvalid_tfidf)
print ("Logistic regression classifier with TF IDF vectors: ", accuracy)
joblib.dump(logistic_regression_tfidf, 'classifiers/logistic_regression_tfidf.joblib')


