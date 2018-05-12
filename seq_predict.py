import numpy as np
import pandas as pd
import argparse
import time
import sys; sys.path.append('./dataset_transform/')
from trend import Trend, TrendList
from group_stream import GroupStream
from sklearn.model_selection import KFold
from predict_trend import PredictTrend, PredictTrendList

parser = argparse.ArgumentParser(description='Sequence Transform Tool.')
parser.add_argument('-i','--input', help='Config input file name',required=True)
args = parser.parse_args()

df = pd.read_csv(args.input)

window_size=50
prob_threshold=0.65

kf = KFold(n_splits=10, shuffle=False)
X = pd.DataFrame()
for i in range(len(df.columns)-1):
    X[(df.columns[i])]=df[df.columns[i]]
y = df[df.columns[-1]]
kf.get_n_splits(X,y)

'''
for train_index, test_index in kf.split(X,y):
    tl = []
    attr = []
    for i in df.columns[:-1]:
        attr.append(i)
        tl.append(TrendList(i, np.array(X[i][train_index]), prob_threshold, window_size, merge_at_once=True))
    print(tl)
'''


'''
tl = []
attr = []
for i in df.columns:
    attr.append(i)
    tl.append(TrendList(i, np.array(df[i]), prob_threshold, window_size, merge_at_once=True))
#print(tl)
'''

'''
gs = GroupStream(tl)
pr = PredictTrendList(gs)
pr.join_all()
pr.delete_indeterministic(df.columns[-1])
print(pr)
'''