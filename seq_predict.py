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
from classifier import Classifier

parser = argparse.ArgumentParser(description='Sequence Transform Tool.')
parser.add_argument('-i','--input', help='Config input file name',required=True)
args = parser.parse_args()

df = pd.read_csv(args.input)

#tll, gll are abbreviations for TrendList list and GroupTrendList list
(X_train, X_test), \
(X_tll_train, X_tll_test, X_attr) =\
kfold_data(df, 10, merge_at_once=True, merge_threshold=2)

classifier = Classifier(X_train=X_train, X_test=X_test, X_tll_train=X_tll_train, X_tll_test=X_tll_test)
classifier.fit()

print(classifier.X_gsl_train[0])