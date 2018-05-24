import numpy as np
import pandas as pd
import argparse
import time
from trend import Trend, TrendList
from group_trend import GroupTrend, GroupTrendList
from group_stream import GroupStream

class Classifier:
    def __init__(self, X_train, X_test, X_tll_train, X_tll_test):
        self.X_train=X_train
        self.X_test=X_test
        self.X_tll_train=X_tll_train
        self.X_tll_test=X_tll_test

    def fit(self):
        self.X_gll_train, self.X_gll_test = [], []
        self.X_gsl_train, self.X_gsl_test = [], []
        for i in range(len(self.X_train)):
            X_gl_train, X_gl_test = [], []
            for j in range(len(self.X_train[0].columns)):
                X_gl_train.append(GroupTrendList(self.X_tll_train[i][j]))
                X_gl_test.append(GroupTrendList(self.X_tll_test[i][j]))

            self.X_gll_train.append(X_gl_train)
            self.X_gll_test.append(X_gl_test)

            self.X_gsl_train.append(GroupStream(self.X_gll_train[i]))
            self.X_gsl_test.append(GroupStream(self.X_gll_test[i]))

    def predict(self, X):
        pass