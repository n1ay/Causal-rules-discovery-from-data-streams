from collections import Counter
from dataset_transform.group_cluster import GroupCluster, GroupClusterList
from dataset_transform.cluster import Cluster, ClusterList
import pandas as pd
from typing import List
import copy
from dataset_transform.globals import *


class GroupStream:
    def __init__(self, cluster_lists: List[GroupClusterList], rules_stream=[]):
        self.cluster_lists = cluster_lists
        if rules_stream == []:
            self.rules_stream = self.build_stream()
        else:
            self.rules_stream = rules_stream

    def build_stream(self):
        counter = Counter()
        lengths = Counter()

        stream = []
        for i in range(len(self.cluster_lists)):
            lengths[i] = len(self.cluster_lists[i].cluster_list)
            counter[i] = 0

        while True:
            end = True
            intercept_check_list = []
            for i in range(len(self.cluster_lists)):
                intercept_check_list.append(self.cluster_lists[i].cluster_list[counter[i]])
            ret = self.intersect(intercept_check_list)
            if ret != None:
                stream.append(ret)

            for i in range(len(self.cluster_lists)):
                if counter[i] != lengths[i] - 1:
                    end = False
                    break

            if end:
                break

            counter[0] += 1
            for i in range(len(self.cluster_lists) - 1):
                if counter[i] > lengths[i] - 1:
                    counter[i] = 0
                    counter[i + 1] += 1

        return stream

    # this can be optimized a lot
    def intersect(self, intercept_cluster_list):
        if intercept_cluster_list[0] == None or (len(intercept_cluster_list) > 1 and intercept_cluster_list[1] == None):
            return None
        elif len(intercept_cluster_list) == 1:
            return intercept_cluster_list[0]
        elif len(intercept_cluster_list) == 2:
            f1 = intercept_cluster_list[0]._from
            t1 = intercept_cluster_list[0]._to
            f2 = intercept_cluster_list[1]._from
            t2 = intercept_cluster_list[1]._to
            ret, other = None, None
            if f1 >= t2 or f2 >= t1:
                return None
            elif f1 >= f2 and f1 < t2:
                ret = copy.copy(intercept_cluster_list[0])
                other = intercept_cluster_list[1]
            elif f2 > f1 and f2 < t1:
                ret = copy.copy(intercept_cluster_list[1])
                other = intercept_cluster_list[0]

            ret._to = min(ret._to, other._to)
            ret.length = ret._to - ret._from
            for i in other.values.keys():
                ret.values[i] = other.values[i]
            ret.attribute_order += other.attribute_order
            return ret
        else:
            ret2 = self.intersect(intercept_cluster_list[0:2])
            return self.intersect([ret2] + intercept_cluster_list[2:])

    def __copy__(self):
        return GroupStream(cluster_lists=self.cluster_lists.copy(), rules_stream=copy.deepcopy(self.rules_stream))

    def __str__(self):
        ret = "Rules: \n"
        for i in self.rules_stream:
            ret += '{0} \n'.format(i)
        return ret

    # merge=True works only when used with inplace=True
    def drop_attribute(self, attribute, inplace=False, merge=False):
        gs = self.rules_stream.copy()

        for i in gs:
            del i.values[attribute]

        if inplace:
            self.rules_stream = gs
            if merge:
                self.rules_stream = self.merge(True)
        return gs

    def merge(self, inplace=False):
        gs = self.rules_stream.copy()

        for i in range(len(gs) - 1):
            while (i < len(gs) - 1):
                merge = True
                for j in gs[0].values.keys():
                    if gs[i].values[j] != gs[i + 1].values[j]:
                        merge = False
                        break
                if merge:
                    gs[i].merge(gs[i + 1])
                    gs.remove(gs[i + 1])
                else:
                    break

        if inplace:
            self.rules_stream = gs
        return gs

    def decompose(self, attribute, lst=[]):
        if lst == []:
            lst = self.rules_stream
        ret = []
        for i in lst:
            for j in range(i.length):
                ret.append(i.values[attribute])

        df = pd.DataFrame({attribute: ret})
        return df

    def find_fade_candidate(self, lst, index, fade_to_threshold) -> int:
        prev_length = -1
        next_length = -1
        if index > 0:
            if lst[index - 1].length > fade_to_threshold:
                prev_length = lst[index - 1].length
        if index < len(lst) - 1:
            if lst[index + 1].length > fade_to_threshold:
                next_length = lst[index + 1].length

        if prev_length >= next_length and prev_length != -1:
            return -1
        elif prev_length < next_length and next_length != -1:
            return +1
        else:
            return 0

    def fade_shorts(self, fade_threshold=2, inplace=False):

        flst = copy.deepcopy(self.rules_stream)
        if fade_threshold < 1:
            return flst

        fade_to_threshold = fade_threshold * 2 + 2
        i = 0
        while i < len(flst):
            if flst[i].length <= fade_threshold:
                add_to = self.find_fade_candidate(flst, i, fade_to_threshold)

                if add_to == -1:
                    flst[i - 1].length += flst[i].length
                    flst[i - 1]._to += flst[i].length
                    flst.remove(flst[i])
                    i -= 1

                elif add_to == 1:
                    flst[i + 1].length += flst[i].length
                    flst[i + 1]._from -= flst[i].length
                    flst.remove(flst[i])
                    i -= 1
            i += 1
        if inplace:
            self.rules_stream = flst
        return flst

    __repr__ = __str__
