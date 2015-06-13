# coding: utf-8

#get_ipython().magic(u'pylab inline')
import sklearn as sk
import numpy as np
import pandas as pd
import sys

from sklearn.cross_validation import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.grid_search import GridSearchCV, ParameterGrid
from sklearn.metrics import r2_score
from sklearn import feature_selection

from sklearn.metrics import explained_variance_score, mean_absolute_error, \
                            mean_squared_error, r2_score

def train_and_evaluate(clf, x_train, y_train):
    """Train the selected model with the train data
       and evaluate.
    """

    clf.fit(x_train, y_train)

    print "Coefficient of determination on training set:",clf.score(x_train, y_train)


def measure_performance(X,y,clf):
    """Measure perfomance of the selected model"""

    y = scalery.inverse_transform(y)
    y_pred = scalery.inverse_transform(clf.predict(X))

    mae = np.mean(np.abs(y_pred - y))
    rmse = np.sqrt(np.mean((y_pred - y)**2))
    rae = round(np.sum(np.abs(y_pred - y))/np.sum(np.abs(y - np.mean(y))),2)
    rrse = round(np.sqrt(np.sum((y_pred - y)**2)/np.sum((y - np.mean(y))**2)),2)
    r2 = r2_score(y, y_pred)

    print "Mean absolute error: ", mae
    print "Root Mean Square Error: ", rmse
    print "Relative absolute error: ", rae
    print "Root relative squared error : ", rrse
    print "Number of instances: ", len(y)
    print "Variance score:", r2

    return {'mae':mae, 'rmse':rmse, 'rae':rae, 'rrse':rrse, 'r2':r2}


# Load the data
path = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/modelo_minas/datos/"
test_filename = "test.csv"

# Load the data
data = pd.read_csv(path + test_filename)

# Choose The target for prediction and remove from data
data_target = data['Utilidad']
data = data.drop(['Utilidad'], axis=1)

# Columns to be written in the results
columns = list(data.columns.values)

# The range of C
Crange = range(1,50)
Grange = np.linspace(0,0.1,11)
#Grange = [0.01]
kernel = 'rbf'
epsilon = [0.05]

# The percentage of data used as a test and training
test_percentage = 0.30
size_train = int(len(data) - len(data)*test_percentage)

x_train = data[:size_train]
x_test = data[size_train:]
y_train = data_target[:size_train]
y_test = data_target[size_train:]

# Scale the data
scalerX = StandardScaler().fit(x_train)
scalery = StandardScaler().fit(y_train)

x_train = scalerX.transform(x_train)
y_train = scalery.transform(y_train)
x_test = scalerX.transform(x_test)
y_test = scalery.transform(y_test)

# Print max and min values of the scaled data
#print np.max(x_train), np.min(x_train), np.mean(x_train), np.max(y_train), np.min(y_train), np.mean(y_train)
#print ""

param_grid = [
  {'C':Crange ,'gamma':Grange ,'kernel': [kernel], 'epsilon':epsilon}]

scores = ['mean_absolute_error', 'mean_squared_error']



print "Iterate over: ", scores
print ""

for score in scores:
    clf = GridSearchCV(SVR(), param_grid, cv=5,
                       scoring=score, n_jobs=2)
    clf.fit(x_train, y_train)

    print "Scoring: ", score
    print ""

    print "Coefficient of determination on training set:",clf.score(x_train, y_train)

    print("Best parameters set found on development set: ")
    print ""
    print clf.best_estimator_
    print ""
    print clf.scorer_
    print ""

    print("Detailed classification report:")
    print ""
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print ""

    #print "Variance score: ", explained_variance_score(y_test, y_pred)
    #print "Mean absolute error: ", mean_absolute_error(y_test, y_pred)
    #print "mean_squared_error: ", mean_squared_error(y_test, y_pred)
    #print "Regression score: ", r2_score(y_test, y_pred)
    mp = measure_performance(x_test, y_test, clf)
    print ""
    print "---------------------------------------------"


    # Write results in a text file
    results_file = open('results_1fold.txt', 'a')
    results_file.write(str(columns)+'\n')
    results_file.write(str(clf)+'\n')
    results_file.write(str(mp)+'\n\n')
    results_file.close()
