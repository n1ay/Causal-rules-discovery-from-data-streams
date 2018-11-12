import numpy as np
import pandas as pd
import argparse
import time
import sys

sys.path.append('./dataset_transform/')
sys.path.append('./dataset_predict/')
from dataset_transform.cluster import Cluster, ClusterList
from dataset_transform.group_cluster import GroupCluster, GroupClusterList
from dataset_transform.group_stream import GroupStream
from sklearn.model_selection import KFold
from dataset_predict.kfold_data import *
from dataset_predict.metrics import *
from dataset_predict.classifier import Classifier

parser = argparse.ArgumentParser(description='Sequence Predict Tool.')
parser.add_argument('-if', '--input_fit', help='Input file name with csv sequence to fit', required=True)
parser.add_argument('-ip', '--input_predict', help='Input file name with csv sequence to predict', required=True)
args = parser.parse_args()

# dataset
df_fit = pd.read_csv(args.input_fit)
df_predict = pd.read_csv(args.input_predict)

classifier = Classifier(lookup=1, merge_threshold=2, fade_threshold=2)

# prediction of single stream
classifier.fit(df_fit)
prediction = classifier.predict(df_predict)
print(prediction)
