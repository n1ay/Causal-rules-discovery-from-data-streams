import unittest
from dataset_transform.cluster import ClusterList, Cluster


class ClusterTest(unittest.TestCase):

    def test_create_list1(self):
        attribute = 'test'
        values = [1, 1, 1, 1, 1]
        clusterList = ClusterList(attribute, values)
        self.assertEqual(len(clusterList.cluster_list), 1)

    def test_create_list2(self):
        attribute = 'test'
        values = [1, 2, 2, 2, 1]
        clusterList = ClusterList(attribute, values)
        self.assertEqual(len(clusterList.cluster_list), 3)

    def test_try_append_cluster1(self):
        cluster1 = Cluster(None, 1, 0, 2)
        cluster2 = Cluster(None, 1, 0, 5)
        success = cluster1.try_append_cluster(cluster2)
        self.assertEqual(success, True)
        self.assertEqual(cluster1.length, 7)

    def test_try_append_cluster2(self):
        cluster1 = Cluster(None, 1, 0, 2)
        cluster2 = Cluster(None, 2, 0, 1)
        success = cluster1.try_append_cluster(cluster2)
        self.assertEqual(success, False)
        self.assertEqual(cluster1.length, 2)

    def test_merge1(self):
        attribute = 'test'
        values = [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
        clusterList = ClusterList(attribute, values, merge_at_once=True, merge_threshold=1)
        self.assertEqual(len(clusterList.cluster_list), 1)
        self.assertEqual(clusterList.cluster_list[0].value, 1)
        self.assertEqual(clusterList.cluster_list[0].length, len(values))

    def test_merge2(self):
        attribute = 'test'
        values = [1, 2, 3, 4, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        clusterList = ClusterList(attribute, values, merge_at_once=True, merge_threshold=1)
        self.assertEqual(len(clusterList.cluster_list), 1)
        self.assertEqual(clusterList.cluster_list[0].value, 1)
        self.assertEqual(clusterList.cluster_list[0].length, len(values))

    def test_merge3(self):
        attribute = 'test'
        values = [5, 5, 5, 5, 5, 1, 2, 3, 4, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        clusterList = ClusterList(attribute, values, merge_at_once=True, merge_threshold=1)
        self.assertEqual(len(clusterList.cluster_list), 2)
        self.assertEqual(clusterList.cluster_list[0].value, 5)
        self.assertEqual(clusterList.cluster_list[0].length, 9)
        self.assertEqual(clusterList.cluster_list[1].value, 1)
        self.assertEqual(clusterList.cluster_list[1].length, 19)


if __name__ == '__main__':
    unittest.main()
