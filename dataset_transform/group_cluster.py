import operator
from globals import *
from cluster import Cluster, ClusterList
from collections import Counter

class GroupCluster:
    def __init__(self, cluster_list, values, _from, _to, attribute_order=[]):
        self.cluster_list=cluster_list
        self._from=_from
        self._to=_to
        self.length=_to-_from
        self.values=values
        if attribute_order != []:
            self.attribute_order=attribute_order
        else:
            self.attribute_order = [(cluster_list.attribute, _from)]

    def merge(self, group_cluster):
        self._to+=group_cluster.length
        self.length+=group_cluster.length
        self.attribute_order+=group_cluster.attribute_order

    def __str__(self):
        return '(Values: {0.values}, From: {0._from}, To: {0._to}, Length: {0.length}, Attribute order: {0.attribute_order})'.format(self)

    def __copy__(self):
        return GroupCluster(self.cluster_list, self.values.copy(), self._from, self._to, self.attribute_order.copy())

    __repr__ = __str__

class GroupClusterList:
    def __init__(self, cluster_list):
        self.attribute=cluster_list.attribute
        self.cluster_list=self.create_list(cluster_list)

    def __str__(self):
        s="Attribute: "+self.attribute+"\n["
        for i in self.cluster_list:
            if i!=self.cluster_list[-1]:
                s+=str(i)+",\n"
            else:
                s += str(i)
        s+="]"
        return s

    #cluster_list here is ClusterList class
    def create_list(self, cluster_list):
        i=0
        new_list=[]
        for i in cluster_list.cluster_list:
            values = Counter()
            values[self.attribute]=i.value
            new_list.append(GroupCluster(i.cluster_list, values, i._from, i._to))
        return new_list

    __repr__ = __str__