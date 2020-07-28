# -*- coding: utf-8 -*-
"""sentiment-analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T6YrEw463EPXLxclfIEKWsEXvAxMvGI-

**Movie Review Sentiment Analysis**

**Section 1: Building the classifier**

Our dataset is tab separated; therefore, we use the delimiter as \t to denote a tab separated dataset. If you load your dataset at this point you’ll get some errors at a later point due to the quotation marks found in the reviews. In order to avoid these errors we add quoting = 3 parameter which tells pandas to ignore the quotation marks.
"""

import numpy as np
import pandas as pd
df = pd.read_csv('imdb_labelled.tsv', delimiter = '\t', engine='python', quoting = 3)

"""We shall use the re python utility to remove punctuation marks. We use the NLTK utility to remove stop words and the WordNetLemmatizer utility from NLTK to reduce the words to their dictionary root form."""

import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

"""The next step is to create an empty corpus in which we append all the words in the reviews. A corpus is simply a collection of words.

**In the next stage, we create a for-loop that goes through all the reviews and does the following:**

1) Removes punctuation marks. We do this by specifying letters we don’t want to remove (i.e letters from a-z. We specify this using a caret [^]).

2) After removing punctuation marks, we prevent two words from merging together by specifying space as the second parameter. This will ensure that the removed character is replaced with a space.

3) Convert the words to lowercase.

4) Split the words into a list of words.

5) Convert the words to their root form by Lemmatization.

6) Remove common words in English using stop words. We convert the stop words into a set to make the algorithm go through them faster. This is especially useful when dealing with massive data sets.

7) Join the words back using a space.

8) Append the words to our empty corpus list.
"""

corpus = []
for i in range(0, 1000):
  review = re.sub('[^a-zA-Z]', ' ', df['Review'][i])
  review = review.lower()
  review = review.split()
  lemmatizer = WordNetLemmatizer()
  review = [lemmatizer.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
  review = ' '.join(review)
  corpus.append(review)

"""Creating a Bag of Words model"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 2000) # convert a collection of text documents to a matrix of token counts
X = cv.fit_transform(corpus).toarray()    # returns an array
y = df.iloc[:, 1].values

"""We divide the number of occurrences of each word in a document by the total number of words as a way of normalization. These new features are called **tf, short for Term Frequencies**.

Very common words usually tend to have a higher tf. However, some of these words might not be so important in determining whether a review is positive or negative. The way we deal with this issue is by downscaling the weights for common words that are less informative than words that occur less in the corpus.
This downscaling is called **tf–idf for “Term Frequency times Inverse Document Frequency”**.
"""

from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer()
X = tf_transformer.fit_transform(X).toarray()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfVectorizer = TfidfVectorizer(max_features =2000)
X = tfidfVectorizer.fit_transform(corpus).toarray()

"""Splitting dataset into training set and test set"""

from sklearn.model_selection import train_test_split
X_train, X_test , y_train, y_test = train_test_split(X, y , test_size = 0.20)

"""Fitting a Classifier"""

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

"""Making predictions and printing a confusion matrix"""

predictions = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, predictions)
print(cm)
accuracy_score(y_test, predictions)

"""**Section 2: Section 2: Using Flask to host the model**

In order to bring our model to production, we need to save our classifier and our TfidfVectorizer for use in production. Python allows us to do this using the pickle Python module. 

 The Python utility used for pickling and unpickling is known as **joblib**.
"""

from sklearn.externals import joblib
joblib.dump(tfidfVectorizer, 'tfidfVectorizer.pkl')
joblib.dump(classifier, 'classifier.pkl')