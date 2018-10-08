import operator
from dataset_transform.globals import *
from collections import Counter

'''
cluster_list - reference to ClusterList which contains this object
rest - self documenting
length = _from - _to, so one length cluster
'''


class Cluster:
    def __init__(self, cluster_list, value, _from, _to):
        self.cluster_list = cluster_list
        self._from = _from
        self._to = _to
        self.value = value
        self.length = _to - _from

    def try_append(self, value):
        if value == self.value:
            self._to += 1
            self.length += 1
            return True
        else:
            return False

    def try_append_cluster(self, cluster):
        if cluster.value == self.value:
            self._to += cluster.length
            self.length += cluster.length
            return True
        else:
            return False

    def force_append_cluster(self, cluster):
        cluster.value = self.value
        self.try_append_cluster(cluster)

    def __str__(self):
        return '(Value: {0.value}, From: {0._from}, To: {0._to}, Length: {0.length})'.format(self)

    __repr__ = __str__


'''
attribute - attribute/feature name
data - list from clusters will be created
merge_at_once - merge clusters if their length is less or equal merge_threshold.
These clusters will be merged to the biggest adjacent cluster which size is bigger then self.threshold_to_append
'''


class ClusterList:
    def __init__(self, attribute, data, merge_at_once=False, merge_threshold=2):
        self.attribute = attribute
        self.data = data
        self.cluster_list = self.create_list(data)
        self.merge_threshold = merge_threshold
        self.threshold_to_append = merge_threshold * 2 + 2
        if merge_at_once:
            self.cluster_list = self.merge(self.cluster_list, merge_threshold)

    def create_list(self, data):
        lst = []
        j = 0

        if len(data) > 0:
            lst.append(Cluster(self, data[0], 0, 1))
        for i in range(1, len(data)):
            if not (lst[j].try_append(data[i])):
                lst.append(Cluster(self, data[i], lst[j]._to, lst[j]._to + 1))
                j += 1
        return lst

    def find_merge_candidate(self, lst, index) -> int:
        prev_length = -1
        next_length = -1
        if index > 0:
            if lst[index - 1].length > self.threshold_to_append:
                prev_length = lst[index - 1].length
        if index < len(lst) - 1:
            if lst[index + 1].length > self.threshold_to_append:
                next_length = lst[index + 1].length

        if prev_length >= next_length and prev_length != -1:
            return -1
        elif prev_length < next_length and next_length != -1:
            return +1
        else:
            return 0

    # can be optimized!
    def merge(self, lst, merge_threshold):
        if merge_threshold < 1:
            return lst
        merged_list = lst.copy()
        i = 0
        while i < len(merged_list):
            if merged_list[i].length <= merge_threshold:
                add_to = self.find_merge_candidate(merged_list, i)

                if add_to == -1:
                    merged_list[i - 1].length += merged_list[i].length
                    merged_list[i - 1]._to += merged_list[i].length
                    merged_list.remove(merged_list[i])
                    i -= 1
                    self.merge_same_value(merged_list, i)
                    if i > 1:
                        i -= 2
                        self.merge_same_value(merged_list, i)

                elif add_to == 1:
                    merged_list[i + 1].length += merged_list[i].length
                    merged_list[i + 1]._from -= merged_list[i].length
                    merged_list.remove(merged_list[i])
                    i -= 1
                    self.merge_same_value(merged_list, i)
                    if i > 1:
                        i -= 2
                        self.merge_same_value(merged_list, i)
            i += 1
        return merged_list

    def merge_same_value(self, merged_list, index):
        while (index >= 0 and index < len(merged_list) - 1 and merged_list[index].try_append_cluster(merged_list[index + 1])):
            merged_list.remove(merged_list[index + 1])

    def __str__(self):
        s = "Attribute: " + self.attribute + "\n["
        for i in self.cluster_list:
            if i != self.cluster_list[-1]:
                s += str(i) + ",\n"
            else:
                s += str(i)
        s += "]"
        return s

    __repr__ = __str__
