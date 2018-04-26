import operator
from collections import Counter

cannot_determine_trend_value='?'

class Trend:
    def __init__(self, trend_list, values_list, _from, _to, prob_threshold, values=Counter(), attribute_order=[]):
        self.trend_list=trend_list
        self._from=_from
        self._to=_to
        self.values_list=values_list
        self.counter=Counter()
        self.prob_threshold=prob_threshold
        self.attribute_order = attribute_order
        if values!=Counter():
            self.values=values
        else:
            self.values=self.calc_trend(prob_threshold)

    def __str__(self):
        if len(self.counter.keys())>0:
            return '(Values: {0.values}, From: {0._from}, To: {0._to}, Counter: {0.counter})'.format(self)
        else:
            return '(Values: {0.values}, From: {0._from}, To: {0._to}, Attribute order: {0.attribute_order})'.format(self)

    def calc_trend(self, prob_threshold):
        if self.attribute_order==[]:
            self.attribute_order.append(self.trend_list.attribute)
        values=Counter()
        for i in self.values_list:
            try:
                self.counter[i]+=1
            except KeyError:
                self.counter[i]=1
        max_key=(max(self.counter.items(), key=operator.itemgetter(1))[0])

        if len(self.values_list < 20):
            min_prob=max(0.6, prob_threshold)
        else:
            min_prob=prob_threshold

        if self.counter[max_key] >= min_prob*len(self.values_list):
            values[self.trend_list.attribute]=max_key
        else:
            values[self.trend_list.attribute]=cannot_determine_trend_value
        return values

    def __copy__(self):
        return Trend(self.trend_list, self.values_list.copy(), self._from, self._to, self.prob_threshold, self.values.copy(), self.attribute_order.copy())

    __repr__ = __str__

class TrendList:
    def __init__(self, attribute, data, prob_threshold, window_size, merge_at_once=False):
        self.attribute=attribute
        self.prob_threshold=prob_threshold
        self.trend_list=self.create_list(data, window_size)
        if merge_at_once:
            self.merge()

    def merge(self):
        i=0
        while(i+1<len(self.trend_list)):
            if(self.trend_list[i].values[self.attribute]==self.trend_list[i + 1].values[self.attribute]):
                self.trend_list[i]._to=self.trend_list[i + 1]._to
                self.trend_list[i].counter=self.trend_list[i].counter+self.trend_list[i+1].counter
                del self.trend_list[i + 1]

            else:
                i+=1

    def __str__(self):
        s="Attribute: "+self.attribute+"\n["
        for i in self.trend_list:
            if i!=self.trend_list[-1]:
                s+=str(i)+",\n"
            else:
                s += str(i)
        s+="]"
        return s

    def create_list(self, data, window_size):
        i=0
        new_list=[]
        while(i<len(data)):
            if i+window_size<=len(data):
                new_list.append(Trend(self, data[i:i+window_size], i, i+window_size-1, self.prob_threshold))
            else:
                new_list.append(Trend(self, data[i:], i, len(data)-1, self.prob_threshold))
            i+=window_size
        return new_list

    __repr__ = __str__