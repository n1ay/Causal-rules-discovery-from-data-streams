from group_stream import GroupStream

class Rule:
    def __init__(self, value_from, value_to):
        self.value_from=value_from
        self.value_to=value_to

    def __str__(self):
        return '{0.value_from}->{0.value_to}'.format(self)

    __repr__=__str__

class RulesStream:
    def __init__(self, group_stream:GroupStream, output_format=[]):
        self.group_stream=group_stream
        self.attributes={}
        self.values=[[] for _ in group_stream.rules_stream[0].values.keys()]
        self.transform_stream(group_stream)
        self.output_format=output_format

    def extract_rules(self, group_trend1, group_trend2):
        rules_dict={}
        for i in group_trend1.values.keys():
            rules_dict[i]=Rule(group_trend1.values[i], group_trend2.values[i])

        return rules_dict

    def add_rules(self, rules_dict):
        for i in rules_dict.keys():
            self.values[self.attributes[i]].append(rules_dict[i])

    def transform_stream(self, group_stream):
        idx=0
        for i in group_stream.rules_stream[0].values.keys():
            self.attributes[i]=idx
            idx+=1
        for i in range(len(group_stream.rules_stream)-1):
            rules_dict=self.extract_rules(group_stream.rules_stream[i], group_stream.rules_stream[i+1])
            self.add_rules(rules_dict)

    def __str__(self):
        if self.output_format==[]:
            for i in self.attributes.keys():
                self.output_format.append(i)
        str=''
        for i in range(len(self.output_format)):
            if i < len(self.output_format)-1:
                str+='{0},'.format(self.output_format[i])
            else:
                str += '{0}\n'.format(self.output_format[i])

        for i in range(len(self.values[0])):
            for j in range(len(self.output_format)):
                if j < len(self.output_format) - 1:
                    str+='{0},'.format(self.values[self.attributes[self.output_format[j]]][i])
                else:
                    str += '{0}\n'.format(self.values[self.attributes[self.output_format[j]]][i])
        return str


    __repr__=__str__

