from collections import Counter
from trend import Trend, TrendList
from group_trend import GroupTrend, GroupTrendList
from typing import List
import copy
from globals import *

class PredictTrend:
    def __init__(self, trend: Trend):
        self.values=trend.values
        self.length=trend._to-trend._from+1

    def join(self, predict_trend, cut_length=False):
        if self==predict_trend:
            return
        if len(self.values.keys()) == len(predict_trend.values.keys()):
            for i in self.values.keys():
                if self.values[i]!=predict_trend.values[i]:
                    return
        self.length+=predict_trend.length
        if cut_length:
            predict_trend.length=0

    def same_values(self, predict_trend, y_arg):
        if len(self.values.keys()) == len(predict_trend.values.keys()):
            for i in self.values.keys():
                if i!=y_arg and self.values[i]!=predict_trend.values[i]:
                    return False
        return True

    def __str__(self):
        return '(Values: {0.values}, Length: {0.length})'.format(self)

    __repr__ = __str__

class PredictTrendList:
    def __init__(self, group_stream):
        self.predict_trend_list=group_stream.get_predict_rules(on_copy=True, drop_undefined_first=False)

    def join_all(self):
        prev_len=len(self.predict_trend_list)
        act_len=0
        while(prev_len!=act_len):
            for i in self.predict_trend_list:
                for j in self.predict_trend_list:
                    i.join(j, True)
                    if j.length == 0:
                        self.predict_trend_list.remove(j)
            prev_len=act_len
            act_len=len(self.predict_trend_list)

    def get_stream_length(self):
        sum=0
        for i in self.predict_trend_list:
            sum+=i.length
        return sum

    def remove_indeterminism(self, y_arg):
        prev_len = len(self.predict_trend_list)
        act_len = 0
        while (prev_len != act_len):
            for i in self.predict_trend_list:
                for j in self.predict_trend_list:
                    if i != j and i.same_values(j, y_arg):
                        if i.length >= j.length:
                            j.length = 0
                        else:
                            i.length = 0
                    if j.length == 0:
                        self.predict_trend_list.remove(j)
            prev_len = act_len
            act_len = len(self.predict_trend_list)

    def __str__(self):
        ret="Rules: \n"
        for i in self.predict_trend_list:
            ret+='{0} \n'.format(i)
        return ret

    __repr__=__str__

