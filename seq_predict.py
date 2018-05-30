import numpy as np
import pandas as pd
import argparse
import time
import sys; sys.path.append('./dataset_transform/'); sys.path.append('./dataset_predict/')
from trend import Trend, TrendList
from group_trend import GroupTrend, GroupTrendList
from group_stream import GroupStream
from sklearn.model_selection import KFold
from kfold_data import *
from metrics import *
from classifier import Classifier

### DELET DIS ###################
def print_list(lst):
    for i in lst:
        print(i, '\n')
#################################


parser = argparse.ArgumentParser(description='Sequence Transform Tool.')
parser.add_argument('-i','--input', help='Config input file name',required=True)
args = parser.parse_args()

#dataset
df = pd.read_csv(args.input)

#number of folds
K = 10
X_train, X_test, = kfold_data(df, K)

classifier = Classifier(X_train=X_train, X_test=X_test, lookup=1, merge_threshold=2, fade_threshold=2)

y_test = [X_test[i][classifier.columns[-1]] for i in range(len(X_test))]

#prints used only for testing purposes
#print(classifier.X_gsl_train[0])
#print_list(classifier.X_gsl_test[0])
#print(classifier.X_gsld_test[0])

#v=classifier.predict_value(0)
#print_metrics(get_metrics(X_test[0][classifier.columns[-1]], v))

#
prediction=classifier.predict()
print_metrics(get_metrics_full(y_test, prediction, mean=True))