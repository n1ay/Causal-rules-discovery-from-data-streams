import numpy as np
import pandas as pd
from trend import Trend, TrendList
from group_trend import GroupTrend, GroupTrendList
from sklearn.model_selection import KFold

def kfold_data(df, folds:int=10, merge_at_once:bool=True, merge_threshold:int=2):

    #no shuffle is a must - shuffling timeseries without timestamps is not what we want
    kf = KFold(n_splits=folds, shuffle=False)
    kf.get_n_splits(df)

    X_train, X_test, y_train, y_test = [], [], [], []
    X_tll_train, X_tll_test, X_attr = [], [], df.columns[:-1]
    for train_index, test_index in kf.split(df):
        tl_train, gl_train, tl_test, gl_test = [], [], [], []
        j = 0
        for i in df.columns:
            tl_train.append(TrendList(i, np.array(df[i][train_index]), merge_at_once=merge_at_once, merge_threshold=merge_threshold))
            tl_test.append(TrendList(i, np.array(df[i][test_index]), merge_at_once=merge_at_once, merge_threshold=merge_threshold))
            j += 1

        X_train.append(df.iloc[train_index])
        X_test.append(df.iloc[test_index])

        X_tll_train.append(tl_train)
        X_tll_test.append(tl_test)

    return (X_train, X_test), \
           (X_tll_train, X_tll_test, X_attr), \