import numpy as np
import pandas as pd
import argparse
import time
from trend import Trend, TrendList
from group_trend import GroupTrend, GroupTrendList
from group_stream import GroupStream
import copy

class Classifier:
    def __init__(self, X_train, X_test, X_tll_train, X_tll_test, lookup=1, fade_threshold=2):
        self.X_train=X_train
        self.X_test=X_test
        self.X_tll_train=X_tll_train
        self.X_tll_test=X_tll_test
        self.columns = X_train[0].columns
        self.lookup=lookup
        self.fade_threshold=fade_threshold
        self._fit()

    def _fit(self):
        self.X_gll_train, self.X_gll_test = [], []
        self.X_gsl_train, self.X_gsl_test = [], []
        self.X_gsld_train, self.X_gsld_test = [], []
        for i in range(len(self.X_train)):
            X_gl_train, X_gl_test = [], []
            for j in range(len(self.X_train[0].columns)):
                X_gl_train.append(GroupTrendList(self.X_tll_train[i][j]))
                X_gl_test.append(GroupTrendList(self.X_tll_test[i][j]))

            self.X_gll_train.append(X_gl_train)
            self.X_gll_test.append(X_gl_test)

            X_gsl_train = GroupStream(self.X_gll_train[i])
            X_gsl_test = GroupStream(self.X_gll_test[i])
            X_gsl_train.fade_shorts(fade_threshold=self.fade_threshold, inplace=True)
            X_gsl_test.fade_shorts(fade_threshold=self.fade_threshold, inplace=True)
            self.X_gsl_train.append(X_gsl_train)
            self.X_gsl_test.append(X_gsl_test)

            self.X_gsld_train.append(copy.copy(self.X_gsl_train[i]))
            self.X_gsld_train[i].drop_attribute(self.columns[-1], inplace=True, merge=True)
            self.X_gsld_test.append(copy.copy(self.X_gsl_test[i]))
            self.X_gsld_test[i].drop_attribute(self.columns[-1], inplace=True, merge=True)

    #full prediction of stream for X = X_test
    def predict(self):
        pass

    def predict_value(self, test_idx):
        lst = []
        for i in range(len(self.X_gsld_test[test_idx].rules_stream)-self.lookup):
            lst.append(self.lookup_value(test_idx, i))

        return lst

    #TODO:
    #Dodać odpowiednie łączenie, bo elementy obok siebie się powtarzają
    #Dodać w momecie nie wykrycia zależności, żeby korzystało ze zwykłej reguły pojednyczej
    #Jak to nie działa to wtedy random z dziedziny y
    def lookup_value(self, test_idx, idx):
        X = []
        for j in range(self.lookup + 1):
            X.append(self.X_gsld_test[test_idx].rules_stream[idx+j])
        best_vals = []
        best_similarity = 0
        for i in range(len(self.X_gsld_train[test_idx].rules_stream)-len(X)):
            vals = []
            same = True
            for j in range(len(X)):
                for k in self.columns[:-1]:
                    if X[j].values[k]!=self.X_gsld_train[test_idx].rules_stream[i+j].values[k]:
                        same=False
                        break
            if same:
                for j in range(len(X)):
                    vals.append(self.X_gsld_train[test_idx].rules_stream[i+j])
                sim=self.similarity(X, vals)
                if sim > best_similarity:
                    best_vals = vals
                    best_similarity = sim
        if best_vals == []:
            raise Exception('PredictException', 'Can\'t lookup prediction for values: {0}. No such values in training set'.format(X))
        return best_vals

    def similarity(self, lst_test, lst):
        if len(lst_test)==1:
            return min(lst_test[0].length/lst[0].length, 1/(lst_test[0].length/lst[0].length))
        ratio01 = (lst_test[1].length/lst_test[0].length)/(lst[1].length/lst[0].length)
        ratio0 = lst_test[0].length/lst[0].length
        ratio1 = lst_test[1].length/lst[1].length
        val = 2*min(ratio01,1/ratio01)+min(ratio0,1/ratio0)+min(ratio1,1/ratio1)
        if len(lst_test)>2:
            return val + self.similarity(lst_test[1:], lst[1:])
        elif len(lst_test)==2:
            return val
