import operator
from globals import *
from collections import Counter

class Cluster:
    def __init__(self, cluster_list, value, _from, _to):
        self.cluster_list = cluster_list
        self._from = _from
        self._to = _to
        self.value = value
        self.length = _to-_from

    def try_append(self, value):
        if value==self.value:
            self._to+=1
            self.length+=1
            return True
        else:
            return False

    def try_append_cluster(self, cluster):
        if cluster.value==self.value:
            self._to+=cluster.length
            self.length+=cluster.length
            return True
        else:
            return False

    def __str__(self):
        return '(Value: {0.value}, From: {0._from}, To: {0._to}, Length: {0.length})'.format(self)

    __repr__ = __str__

class ClusterList:
    def __init__(self, attribute, data, merge_at_once=False, merge_threshold=2):
        self.attribute = attribute
        self.data = data
        self.cluster_list = self.create_list(data)
        if merge_at_once:
            self.cluster_list = self.merge(self.cluster_list, merge_threshold)

    def create_list(self, data):
        lst = []
        j = -1
        for i in data:
            if j>=0:
                if not(lst[j].try_append(i)):
                    lst.append(Cluster(self, i, lst[j]._to, lst[j]._to+1))
                    j+=1
            else:
                lst.append(Cluster(self, i, 0, 1))
                j+=1
        return lst

    #can be optimized: but its quite fast (faster than O(n*logn))
    def merge(self, lst, merge_threshold):
        mlst=lst.copy()
        i=0
        while i<len(mlst):
            add_to = 0
            if merge_threshold >= 1:
                if mlst[i].length <= merge_threshold:
                    if i > 0:
                        if i < len(mlst)-1:
                            if mlst[i - 1].length > merge_threshold*2+2 and mlst[i - 1].length >= mlst[i + 1].length:
                                add_to=-1
                            elif mlst[i + 1].length > merge_threshold*2+2 and mlst[i + 1].length > mlst[i - 1].length:
                                add_to=1
                        else:
                            if mlst[i - 1].length > merge_threshold*2+2:
                                add_to = -1
                    elif i < len(mlst)-1:
                        if mlst[i + 1].length > merge_threshold*2+2:
                            add_to = 1

                    if add_to==-1:
                        mlst[i - 1].length+=mlst[i].length
                        mlst[i - 1]._to+=mlst[i].length
                        mlst.remove(mlst[i])
                        i-=1
                        self.merge_same_value(mlst, i)
                        if i>1:
                            i-=2
                            self.merge_same_value(mlst, i)
                    elif add_to==1:
                        mlst[i + 1].length+=mlst[i].length
                        mlst[i + 1]._from-=mlst[i].length
                        mlst.remove(mlst[i])
                        i-=1
                        self.merge_same_value(mlst, i)
                        if i>1:
                            i-=2
                            self.merge_same_value(mlst, i)
            i+=1
        return mlst

    def merge_same_value(self, mlst, i):
        while (i >= 0 and i < len(mlst) - 1 and mlst[i].try_append_cluster(mlst[i + 1])):
            mlst.remove(mlst[i + 1])

    def __str__(self):
        s="Attribute: "+self.attribute+"\n["
        for i in self.cluster_list:
            if i!=self.cluster_list[-1]:
                s+=str(i)+",\n"
            else:
                s += str(i)
        s+="]"
        return s

    __repr__ = __str__