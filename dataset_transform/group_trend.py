import operator
from globals import *
from trend import Trend, TrendList
from collections import Counter

class GroupTrend:
    def __init__(self, trend_list, values, _from, _to, attribute_order=[]):
        self.trend_list=trend_list
        self._from=_from
        self._to=_to
        self.length=_to-_from
        self.values=values
        if attribute_order != []:
            self.attribute_order=attribute_order
        else:
            self.attribute_order = [(trend_list.attribute, _from)]

    def merge(self, group_trend):
        self._to+=group_trend.length
        self.length+=group_trend.length
        self.attribute_order+=group_trend.attribute_order

    def __str__(self):
        return '(Values: {0.values}, From: {0._from}, To: {0._to}, Length: {0.length}, Attribute order: {0.attribute_order})'.format(self)

    def __copy__(self):
        return GroupTrend(self.trend_list, self.values.copy(), self._from, self._to, self.attribute_order.copy())

    __repr__ = __str__

class GroupTrendList:
    def __init__(self, trend_list):
        self.attribute=trend_list.attribute
        self.trend_list=self.create_list(trend_list)

    def __str__(self):
        s="Attribute: "+self.attribute+"\n["
        for i in self.trend_list:
            if i!=self.trend_list[-1]:
                s+=str(i)+",\n"
            else:
                s += str(i)
        s+="]"
        return s

    #trend_list here is TrendList class
    def create_list(self, trend_list):
        i=0
        new_list=[]
        for i in trend_list.trend_list:
            values = Counter()
            values[self.attribute]=i.value
            new_list.append(GroupTrend(i.trend_list, values, i._from, i._to))
        return new_list

    __repr__ = __str__