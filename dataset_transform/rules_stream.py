from dataset_transform.group_stream import GroupStream


class Rule:
    def __init__(self, value_from, value_to, _from, change_moment, _to):
        self.value_from = value_from
        self.value_to = value_to
        self._from = _from
        self._to = _to
        self.change_moment = change_moment

    def __str__(self):
        return '{0.value_from}->{0.value_to}'.format(self)

    __repr__ = __str__


class RulesStream:
    def __init__(self, group_stream: GroupStream, output_format=[]):
        self.group_stream = group_stream
        self.attributes = {}
        self.values = [[] for _ in group_stream.rules_stream[0].values.keys()]
        self.order = []
        self.transform_stream(group_stream)
        self.output_format = output_format

    def extract_rules(self, group_cluster1, group_cluster2):
        rules_dict = {}
        for i in group_cluster1.values.keys():
            rules_dict[i] = Rule(group_cluster1.values[i], group_cluster2.values[i], group_cluster1._from,
                                 group_cluster1._to, group_cluster2._to)

        order = []
        for i in sorted(group_cluster2.attribute_order, key=lambda tup: tup[1]):
            order.append(i[0])
        return rules_dict, order

    def add_rules(self, rules_dict):
        for i in rules_dict.keys():
            self.values[self.attributes[i]].append(rules_dict[i])

    def transform_stream(self, group_stream):
        idx = 0
        for i in group_stream.rules_stream[0].values.keys():
            self.attributes[i] = idx
            idx += 1
        for i in range(len(group_stream.rules_stream) - 1):
            rules_dict, order = self.extract_rules(group_stream.rules_stream[i], group_stream.rules_stream[i + 1])
            self.add_rules(rules_dict)
            self.order.append(order)

    def format_order(self, order_list):
        str = '('
        for i in range(len(order_list)):
            if i < len(order_list) - 1:
                str += '{0};'.format(order_list[i])
            else:
                str += '{0}'.format(order_list[i])
        str += ')\n'
        return str

    def __str__(self):
        if self.output_format == []:
            for i in self.attributes.keys():
                self.output_format.append(i)
        str = ''
        for i in range(len(self.output_format)):
            if i < len(self.output_format):
                str += '{0},'.format(self.output_format[i])
        str += '[len],(order)\n'

        for i in range(len(self.values[0])):
            for j in range(len(self.output_format)):
                str += '{0},'.format(self.values[self.attributes[self.output_format[j]]][i])
            str += '[{0}]'.format(self.values[0][i]._to - self.values[0][i]._from)
            str += self.format_order(self.order[i])
        return str

    __repr__ = __str__
