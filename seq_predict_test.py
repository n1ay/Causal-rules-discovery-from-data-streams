import numpy as np
import pandas as pd
import argparse
import time
import sys;

sys.path.append('./dataset_transform/');
sys.path.append('./dataset_predict/')
from dataset_transform.cluster import Cluster, ClusterList
from dataset_transform.group_cluster import GroupCluster, GroupClusterList
from dataset_transform.group_stream import GroupStream
from sklearn.model_selection import KFold
from dataset_predict.kfold_data import *
from dataset_predict.metrics import *
from dataset_predict.classifier import Classifier

parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
args = parser.parse_args()

# dataset
df = pd.read_csv(args.input)

# number of folds
K = 10
X_train, X_test, = kfold_data(df, K)
y_test = [X_test[i][df.columns[-1]] for i in range(len(X_test))]

classifier = Classifier(lookup=1, merge_threshold=2, fade_threshold=2)
classifier.fit_kfolded(X_train, X_test)

# full prediction of kfolded data set
prediction_kfolded = classifier.predict_kfolded()
print_metrics(get_metrics_full(y_test, prediction_kfolded, mean=True))
