# -*- coding: utf-8 -*-
"""NeuralNetworks(BLSTM).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lS04GseJDVaddNGCn2HVezPSnggF6Scq

**PROBLEM STATEMENT**

Employment scams are on the rise. According to CNBC, the number of employment scams doubled in 2018 as compared to 2017. Economic stress and the coronavirus impact have significantly reduced job availability and job loss for many individuals. This lead to high unemployment rate. In addition, the scams on job postings allow scammers to gain access to personal information, such as bank account details.Many people are falling prey to these scammers using the desperation that is caused by an unprecedented incident.

Hence, with classification model and the use of Natural Language Processing (NLP) , we aim to find an effective model that separate fraudulent and real job postings.
"""

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Nlp library
import re
import nltk
from nltk.corpus import stopwords
import nltk as nlp
from sklearn.feature_extraction.text import CountVectorizer

# sklearn Library
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import explained_variance_score

#Tenserflow Library
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from tensorflow.keras.layers import Embedding,  Bidirectional
from tensorflow.keras.preprocessing.sequence import pad_sequences
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv("/content/fake_job_postings.csv")

"""Check for null values"""

df.isnull().sum()

corr = df.corr().fraudulent
corr

"""Filling all the null values with a blank"""

df.fillna(" ", inplace = True)



df['text'] = df['title'] + " " + df['department'] + \
             " " + df['company_profile'] + " " + \
             df['description'] + " " + \
             df['requirements'] + " " +\
             df['benefits'] + " " +\
             df['function'] + " " +\
             df['required_experience']+ " "+\
             df["required_education"]+ " " +\
             df["industry"]

"""Drop all the columns that is irrelevant for our processing"""

df=df.drop(columns = ['job_id','title','location','department', 'telecommuting',
                             'salary_range','company_profile','description','requirements','benefits','employment_type',
                             'required_experience','required_education','industry','function'])

df.head()

import nltk
nltk.download('punkt')
import nltk
nltk.download('stopwords')
import nltk
nltk.download('wordnet')

"""Preprocessing the data"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer


# Tokenization
df['text'] = df['text'].apply(lambda x: word_tokenize(x.lower()))

# Remove stop words
stop_words = set(stopwords.words('english'))
df['text'] = df['text'].apply(lambda x: [word for word in x if word not in stop_words])

# Lemmatization
lemmatizer = WordNetLemmatizer()
df['text'] = df['text'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

# Remove punctuation and non-alphanumeric characters
df['text'] = df['text'].apply(lambda x: [word for word in x if word.isalnum()])

# Join tokens back into strings
df['text'] = df['text'].apply(lambda x: ' '.join(x))

text_list= df['text']

"""Max_features specifies that only top 10000 frequently occuring words in the training dataset will be used as features."""

max_features = 10000

df['word count'] = [len(i.split(' ')) for i in df['text']]

sent_length = df['word count'].max()

sent_length

"""The tokenizer is an object that will be used to convert the text into a sequence of integers that can be fed into a neural network."""

from tensorflow.keras.preprocessing.text import one_hot, Tokenizer
# create the tokenizer
t = Tokenizer(num_words = max_features)
# fit the tokenizer on the documents
t.fit_on_texts(text_list)

"""This is a method that takes in the list of strings and converts each string into a sequence of integers."""

encoded_docs = t.texts_to_sequences(text_list)

embedded_docs=pad_sequences(encoded_docs,padding='post',maxlen=sent_length)
print(embedded_docs)

"""Specifying the target variable"""

X=embedded_docs
y=df['fraudulent']

X.shape,y.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3, random_state= 32)

print("X_train shape: ",X_train.shape)
print("X_test shape : ",X_test.shape )
print("y_train shape: ",y_train.shape)
print("y_test shape : ",y_test.shape)

"""Embedding vector features is a hyperparameter that is used to specify the size of the vector used to represent each word in the text.

I tried using BLSTM as the accuracy was more and it took lesser computational time compared to lstm
"""

embedding_vector_features=100
model1=Sequential()
model1.add(Embedding(max_features,embedding_vector_features,input_length=sent_length))
model1.add(Bidirectional(LSTM(30)))
model1.add(Dense(1,activation='sigmoid'))
model1.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model1.summary())

hist = model1.fit(X_train, y_train, epochs = 10, batch_size = 32, validation_data=(X_test,y_test))

plt.plot(hist.history['val_loss'], color='b', label="validation loss")
plt.plot(hist.history['loss'], color='red', label="loss")
plt.title("Model Loss")
plt.xlabel("Number of Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.plot(hist.history['val_accuracy'], color='b', label="validation accuracy")
plt.plot(hist.history['accuracy'], color='red', label="accuracy")
plt.title("Model Accuracy")
plt.xlabel("Number of Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

def eval_metrics(actual, prediction):
    print("Accuracy Score: {}".format(accuracy_score(actual, prediction)))
    print("Recall Score: {}".format(recall_score(actual, prediction)))
    print("f1 Score: {}".format(f1_score(actual, prediction)))

y_pred = model1.predict(X_test)

y_train_pred = model1.predict(X_train)

#print(confusion_matrix(y_test, y_pred))

"""If you need to use binary classification metrics but your target variable is continuous, you can convert it into a binary category by setting a threshold"""

y_pred = (y_pred > 0.5)

y_train_pred = (y_train_pred > 0.5)

print(confusion_matrix(y_test, y_pred))

print(classification_report(y_test, y_pred))

eval_metrics(y_test, y_pred)

model1.save("fake-final-classification.h5")

!pip install streamlit

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import streamlit as st
import re
import nltk
from nltk.corpus import stopwords
import nltk as nlp
from sklearn.feature_extraction.text import CountVectorizer

# Load the saved model
model = load_model("/content/fake-final-classification.h5")

# Preprocess the input text
def preprocess_text(text):
    text = re.sub("[^a-zA-Z]", " ", text)
    text = text.lower()
    text = re.sub("[^a-zA-Z]", " ", text)
    text = text.lower()
    text = text.strip()
    text = nltk.word_tokenize(text)
    text = [word for word in text if not word in set(stopwords.words("english"))] # dropping stopwords
    lemma = nlp.WordNetLemmatizer()
    text = [lemma.lemmatize(word) for word in text]
    text = " ".join(text)
    text = text.replace('  ',' ')
    return text

# Make a prediction function

def predict(text):

    preprocessed_text = preprocess_text(text)
    encoded_text = t.texts_to_sequences([preprocessed_text])
    padded_text = pad_sequences(encoded_text, padding='post', maxlen=sent_length)
    prediction = model.predict(padded_text)
    st.write(prediction)

    if prediction > 0.5:
        return ("This job posting is **fraudulent**.")
    else:
        return ("This job posting is **NOT Fraudulent**")

# Example usage
text = input(('Enter the job description:'))
prediction = predict(text)
print(prediction)

