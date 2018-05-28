import numpy as np
import pandas as pd
import argparse
import time
from trend import Trend, TrendList
from group_trend import GroupTrend, GroupTrendList
from group_stream import GroupStream
import copy
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

class Classifier:
    def __init__(self, X_train, X_test, X_tll_train, X_tll_test, lookup=1, fade_threshold=2):
        self.X_train=X_train
        self.X_test=X_test
        self.X_tll_train=X_tll_train
        self.X_tll_test=X_tll_test
        self.columns = X_train[0].columns
        self.lookup=lookup
        self.fade_threshold=fade_threshold
        self.y_values=Counter()
        self._fit()

    def _fit(self):
        self.X_gll_train, self.X_gll_test = [], []
        self.X_gsl_train, self.X_gsl_test = [], []
        self.X_gsld_train, self.X_gsld_test = [], []

        max_workers = min(multiprocessing.cpu_count(), len(self.X_train))
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            processes = []
            for i in range(len(self.X_train)):
                processes.append(executor.submit(self._fit_worker, self.X_tll_train[i], self.X_tll_test[i], self.columns, self.fade_threshold))

            for i in range(len(processes)):
                self.X_gll_train.append(processes[i].result()[0])
                self.X_gll_test.append(processes[i].result()[1])
                self.X_gsl_train.append(processes[i].result()[2])
                self.X_gsl_test.append(processes[i].result()[3])
                self.X_gsld_train.append(processes[i].result()[4])
                self.X_gsld_test.append(processes[i].result()[5])

        for i in self.X_gsl_train[0].rules_stream:
            self.y_values[i.values[self.columns[-1]]]+=i.length

        for i in self.X_gsl_test[0].rules_stream:
            self.y_values[i.values[self.columns[-1]]]+=i.length

    def _fit_worker(self, tll_train, tll_test, columns, fade_threshold):
        X_gl_train, X_gl_test = [], []
        for j in range(len(columns)):
            X_gl_train.append(GroupTrendList(tll_train[j]))
            X_gl_test.append(GroupTrendList(tll_test[j]))

        X_gsl_train = GroupStream(X_gl_train)
        X_gsl_test = GroupStream(X_gl_test)
        X_gsl_train.fade_shorts(fade_threshold=fade_threshold, inplace=True)
        X_gsl_test.fade_shorts(fade_threshold=fade_threshold, inplace=True)

        X_gsld_train = copy.copy(X_gsl_train)
        X_gsld_train.drop_attribute(columns[-1], inplace=True, merge=True)
        X_gsld_test = copy.copy(X_gsl_test)
        X_gsld_test.drop_attribute(columns[-1], inplace=True, merge=True)

        return (X_gl_train, X_gl_test, X_gsl_train, X_gsl_test, X_gsld_train, X_gsld_test)

    #full prediction of stream for X = X_test
    def predict(self):
        lst = []

        max_workers = min(multiprocessing.cpu_count(), len(self.X_train))
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            processes = []
            for i in range(len(self.X_train)):
                processes.append(
                    executor.submit(self.predict_value, i))

            for i in range(len(processes)):
                lst.append(processes[i].result())
        return lst

    def predict_value(self, test_idx):
        lst = []
        if len(self.X_gsld_test[test_idx].rules_stream)==1:
            return self.X_gsl_train[0].decompose(self.columns[-1], self.single_rule_lookup(test_idx, 0))

        for i in range(self.lookup, len(self.X_gsld_test[test_idx].rules_stream)):
            lst+=self.lookup_value(test_idx, i)

        return self.X_gsl_train[0].decompose(self.columns[-1], lst)

    def lookup_value(self, test_idx, idx):
        X = []
        X_len = 0
        for j in range(-self.lookup, 1):
            X.append(self.X_gsld_test[test_idx].rules_stream[idx+j])
            X_len+=X[self.lookup+j].length
        best_vals = []
        best_similarity = 0
        for i in range(len(self.X_gsld_train[test_idx].rules_stream)-len(X)+1):
            vals = []
            same = True
            for j in range(len(X)):
                for k in self.columns[:-1]:
                    if X[j].values[k]!=self.X_gsld_train[test_idx].rules_stream[i+j].values[k]:
                        same=False
                        break
            if same:
                for j in range(len(X)):
                    vals.append(copy.deepcopy(self.X_gsld_train[test_idx].rules_stream[i+j]))
                sim=self.similarity(X, vals)
                if sim > best_similarity:
                    best_vals = vals
                    best_similarity = sim

        #can't find such stream fragment in training set
        #use single rule then
        if best_vals == []:
            if idx == self.lookup:
                vals = []
                for j in range(idx+1):
                    vals+=self.single_rule_lookup(test_idx, j)
                return vals
            else:
                return self.single_rule_lookup(test_idx, idx)
        if idx > self.lookup:
            X_len=X[-1].length

        return self.exchange(test_idx, best_vals, X_len, idx)

    def exchange(self, test_idx, lst, length, idx):
        ret = []
        ret_len = 0
        add_idx=-1
        if idx <= self.lookup:
            add_idx=0

        for i in lst[add_idx:]:
            for j in self.X_gsl_train[test_idx].rules_stream:
                if j._from >= i._from and j._to <= i._to:
                    ret.append(copy.deepcopy(j))
                    ret_len+=j.length

        ratio=length/ret_len
        ret_len=0
        for j in range(len(ret)):
            ret[j].length=round(ret[j].length*ratio)
            if j>0:
                ret[j]._from = ret[j-1]._to
            ret[j]._to=ret[j].length+ret[j]._from
            ret_len+=ret[j].length

        diff = ret_len - length
        if diff > 0:
            for j in range(diff):
                ret[j].length-=1
                if j > 0:
                    ret[j]._from = ret[j - 1]._to
                ret[j]._to = ret[j].length + ret[j]._from
        elif diff < 0:
            for j in range(-diff):
                ret[j].length+=1
                if j > 0:
                    ret[j]._from = ret[j - 1]._to
                ret[j]._to = ret[j].length + ret[j]._from

        return ret

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

    def single_rule_lookup(self, test_idx, idx):
        ref_val = self.X_gsld_test[test_idx].rules_stream[idx]
        best_vals = None
        vals = None
        best_similarity = 0
        for i in range(len(self.X_gsld_train[test_idx].rules_stream)):
            same = True
            for k in self.columns[:-1]:
                if ref_val.values[k] != self.X_gsld_train[test_idx].rules_stream[i].values[k]:
                    same = False
                    break
            if same:
                vals = copy.deepcopy(self.X_gsld_train[test_idx].rules_stream[i])
                sim = self.similarity([ref_val], [vals])
                if sim > best_similarity:
                    best_vals = vals
                    best_similarity = sim

        if best_vals != None:
            best_vals.length = ref_val.length
            return self.exchange(test_idx, [best_vals], ref_val.length, self.lookup+1)

        #even single rule can't be found
        #use mode value then
        else:
            best_vals = copy.deepcopy(ref_val)
            best_vals.values[self.columns[-1]] = self.y_values.most_common(1)[0][0]
            return [best_vals]