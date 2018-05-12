from collections import Counter
from trend import Trend, TrendList
from predict_trend import PredictTrend
from typing import List
import copy
from globals import *

class GroupStream:
    def __init__(self, trend_lists:List[TrendList]):
        self.trend_lists=trend_lists
        self.rules_stream=self.build_stream()

    def build_stream(self):
        counter=Counter()
        lengths=Counter()

        stream=[]
        for i in range(len(self.trend_lists)):
            lengths[i]=len(self.trend_lists[i].trend_list)
            counter[i]=0

        while True:
            end=True
            intercept_check_list=[]
            for i in range(len(self.trend_lists)):
                intercept_check_list.append(self.trend_lists[i].trend_list[counter[i]])
            ret=self.intersect(intercept_check_list)
            if ret!=None:
                stream.append(ret)

            for i in range(len(self.trend_lists)):
                if counter[i]!=lengths[i]-1:
                    end=False
                    break

            if end:
                break

            counter[0]+=1
            for i in range(len(self.trend_lists)-1):
                if counter[i]>lengths[i]-1:
                    counter[i]=0
                    counter[i+1]+=1

        return stream

    def intersect(self, intercept_trend_list):
        if intercept_trend_list[0]==None or (len(intercept_trend_list) > 1 and intercept_trend_list[1] == None):
            return None
        elif len(intercept_trend_list)==1:
            return intercept_trend_list[0]
        elif len(intercept_trend_list)==2:
            f1=intercept_trend_list[0]._from
            t1=intercept_trend_list[0]._to
            f2=intercept_trend_list[1]._from
            t2=intercept_trend_list[1]._to
            ret, other = None, None
            if f1>=t2 or f2>=t1:
                return None
            elif f1>=f2 and f1<t2:
                ret=copy.copy(intercept_trend_list[0])
                other=intercept_trend_list[1]
            elif f2>f1 and f2<t1:
                ret=copy.copy(intercept_trend_list[1])
                other = intercept_trend_list[0]

            ret._to=min(ret._to, other._to)
            ret.counter = Counter()
            for i in other.values.keys():
                ret.values[i]=other.values[i]
            ret.attribute_order+=other.attribute_order
            return ret
        else:
            ret2=self.intersect(intercept_trend_list[0:2])
            return self.intersect([ret2] + intercept_trend_list[2:])

    def drop_undefined(self, on_copy=True):
        if on_copy:
            lst = self.rules_stream.copy()
        else:
            lst = self.rules_stream
        filtered_list = []
        add=True
        for i in lst:
            for j in i.values.keys():
                if i.values[j]==cannot_determine_trend_value:
                    add=False
                    break
            if add:
                filtered_list.append(i)
            add=True
        return filtered_list

    def get_predict_rules(self, on_copy=True, drop_undefined_first=True):
        if on_copy:
            lst = self.rules_stream.copy()
        else:
            lst = self.rules_stream
        if drop_undefined_first:
            lst=self.drop_undefined()
        predict_rules_list = []
        for i in lst:
            predict_rules_list.append(PredictTrend(i))
        return predict_rules_list

    def __str__(self):
        ret="Rules: \n"
        for i in self.rules_stream:
            ret+='{0} \n'.format(i)
        return ret

    __repr__=__str__