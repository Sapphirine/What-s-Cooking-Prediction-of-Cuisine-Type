from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import pandas as pd
import json

if __name__=='__main__':
    dic = {}
    lab = 0
    y = []

    train = json.load(open('train.json'))
    train, test = train_test_split(train, test_size=0.25, random_state=34)
    train_data = [" ".join(doc['ingredients']).lower() for doc in train]
    test_data = [" ".join(doc['ingredients']).lower() for doc in test]

    lb = LabelEncoder()
    y = lb.fit_transform([doc['cuisine'] for doc in train])

    tfidf = TfidfVectorizer(binary=True)
    x = tfidf.fit_transform(train_data)
    x_test = tfidf.transform(test_data)
    x = x.astype('float16')
    x_test = x_test.astype('float16')

    print ("Train the model ... ")
    classifier = SVC(C=100, kernel='rbf', degree=3,gamma=1,coef0=1, shrinking=True,tol=0.001,probability=False,
                     cache_size=200, class_weight=None,verbose=False,max_iter=-1, decision_function_shape=None,
                     random_state=None)
    model = OneVsRestClassifier(classifier, n_jobs=8)

    model.fit(x, y)

    y_test = model.predict(x_test)
    y_pred = lb.inverse_transform(y_test)

    print "calculating accurancy..."
    hit = 0.0
    total = 0.0
    for i in range(len(y_pred)):
        if y_pred[i] == test[i]['cuisine']:
            hit += 1
        total += 1

    print hit / total
    print "ok"