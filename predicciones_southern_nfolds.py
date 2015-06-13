# coding: utf-8

#get_ipython().magic(u'pylab inline')
import sklearn as sk
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.grid_search import GridSearchCV, ParameterGrid
from sklearn.metrics import r2_score, make_scorer,mean_absolute_error,\
explained_variance_score, mean_squared_error

from sklearn import cross_validation

from measure_performance import measure_performance, scoring

path = "/home/pedro/univs/doctorado/tesis/tesis/material tesis/datasets/modelo_minas/"
filename = sys.argv[1]


# Load the data
data = pd.read_csv(path + filename)

# Choose The target for prediction and remove the unnecessary data
# Some rows removed because they are outliers
data = data.drop(data.index[[0,1,2,3,4,5,6]]) #38,32,33,42,63,64,65,66,67]])

target = 'Utilidad'
data_target = data[target]
data = data[[#'TM Mineral Cuajone',
             'Ley cobre Cuajone',
             'Porc Recuperacion Cuajone',
             #'TM Mineral Toquepala',
             'Ley cobre Toquepala',
             'Porc Recuperacion Toquepala',
             'Catodos Sulfuros',
             #'TM Mineral Toquepala Oxidos',
             #'TM Mineral Cuajone Oxidos',
             'Ley Toquepala Oxidos',
             'Ley Cuajone Oxidos',
             'Con Toquepala',
             'Con Cuajone',
             'Porc Recuperacion Lix', 'Catodos Oxidos',
             #'PrecioxCatodos',
             'Gasto financiero',
             'Precio'
             ]]

columns = list(data.columns.values)

# Scale the data
scalerX = StandardScaler().fit(data)
scalery = StandardScaler().fit(data_target)

data = scalerX.transform(data)
data_target = scalery.transform(data_target)

# The range of C
Crange = range(1,50)
Grange = np.linspace(0,0.1,11)
kernel = 'rbf'
epsilon = [0.05]

#{'C': np.arange(1, 100, 0.5), 'gamma':np.arange(0,1, 0.002),
#            'kernel': ['rbf']}
#{'C': [0.1, 1, 10, 100, 1000], 'kernel': ['linear']},
#{'C': [0.1, 1, 10, 100, 1000], 'gamma': [1, 0.1, 0.01, 0.001, 0.0001], 'kernel': ['rbf']},
#{'C': range(1, 1000), 'kernel': ['linear']},
#{'C': range(1,100), 'gamma':np.logspace(-2, 1, 12),
# 'kernel': ['rbf'], 'epsilon':np.linspace(0,1,9)},
#{'C': range(1, 1000), 'gamma':10.0 ** np.arange(-5, 4), 'kernel': ['rbf']},
#{'C': np.linspace(1, 100, num=1000), 'gamma':np.linspace(0.001,2, num=200 ),
#'kernel': ['rbf']},
#{'C': np.linspace(1, 100, num=1000), 'gamma':np.linspace(0.001,2, num=200 ),
#'kernel': ['sigmoid']},
#{'C': np.arange(1, 100, 1), 'epsilon':np.arange(0,1,0.1) ,
#'gamma':np.arange(0,1, 0.005 ), 'kernel': ['rbf']} #error 0.2
#{'C': range(1,100), 'gamma':np.linspace(0, 1, 9),
# 'kernel': ['rbf'], 'epsilon':np.linspace(0,1,9)},
#{'C': 10.0**np.arange(-2,9), 'gamma':10.0**np.arange(-5,4),
# 'kernel': ['rbf']},
param_grid = [
  {'C':Crange ,'gamma':Grange ,'kernel': [kernel], 'epsilon':epsilon}
]

# The number of folds, we use leave one out
num_folds = len(data)
cv = cross_validation.KFold(len(data), n_folds=num_folds, random_state=0)

# The scorer for the GridSearch
custom_scorer = make_scorer(measure_performance, scalery=scalery,
                verbose=False, greater_is_better=False)

scores = [custom_scorer]

print "Iterate over: ", scores
print ""

for score in scores:

    clfh = GridSearchCV(SVR(), param_grid, cv=cv,
                       scoring=score)
    clfh.fit(data, data_target)

    # evaluate decision function in a grid

    print "Scoring: ", score
    print ""


    print("Best parameters set found on development set: ")
    print ""
    print clfh.best_estimator_
    print ""

    statistics = []

    # Scorer for the cross validation. We add statistics parameter
    # to obtain the mean of the principal scores
    custom_scorer = make_scorer(measure_performance, scalery=scalery,
                                   verbose=False, scores=statistics)

    #measure_performance(data_target, clfh.predict(data), scalery)
    clf = clfh.best_estimator_

    cross_validation.cross_val_score(clf, data,
                                 data_target, cv=cv,
                                 scoring=custom_scorer)

    promedios = scoring(statistics)

    # Write results in a text file
    results_file = open('results.txt', 'a')
    results_file.write(str(columns)+'\n')
    results_file.write(str(target)+'\n')
    results_file.write("num folds: "+str(target)+'\n')
    results_file.write(str(clf)+'\n')
    results_file.write(str(promedios)+'\n\n')
    results_file.close()

    print columns
    print target
    print "num folds:", num_folds
    print "Promedio: ", promedios
    print ""
    print "---------------------------------------------"

    # plot the results
    #results = [g[1] for g in clfh.grid_scores_]
    #plt.semilogx(Grange, results)
    #plt.show()

