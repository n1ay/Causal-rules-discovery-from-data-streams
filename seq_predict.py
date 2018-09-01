import numpy as np
import pandas as pd
import argparse
import time
import sys; sys.path.append('./dataset_transform/'); sys.path.append('./dataset_predict/')
from cluster import Cluster, ClusterList
from group_cluster import GroupCluster, GroupClusterList
from group_stream import GroupStream
from sklearn.model_selection import KFold
from kfold_data import *
from metrics import *
from classifier import Classifier


parser = argparse.ArgumentParser(description='Sequence Predict Tool.')
parser.add_argument('-i','--input', help='Input file name with csv sequence',required=True)
args = parser.parse_args()

#dataset
df = pd.read_csv(args.input)

#number of folds
K = 10
X_train, X_test, = kfold_data(df, K)
y_test = [X_test[i][df.columns[-1]] for i in range(len(X_test))]

classifier = Classifier(lookup=1, merge_threshold=2, fade_threshold=2)
classifier.fit_kfolded(X_train, X_test)

#full prediction of kfolded data set
prediction_kfolded=classifier.predict_kfolded()
print_metrics(get_metrics_full(y_test, prediction_kfolded, mean=True))

'''
#preparing data for single stream prediction
#just data split in half
df1 = df[0:int(len(df)/2)]
df2 = df[int(len(df)/2):]
df2 = df2[df2.columns[:-1]]

#prediction of single stream
classifier.fit(df1)
prediction = classifier.predict(df2)
print_metrics(get_metrics(df1[df1.columns[-1]], prediction))
'''