import numpy as np


def transform_list_into_categorical_vector_list(lst, classes):
    return [[1 if val == i else 0 for i in range(classes)] for val in lst]


def transform_categorical_vector_list_into_list(lst):
    return [sublist.index(max(sublist)) for sublist in lst]


def reshape_data_to_lstm(data, backward_time_step, forward_time_step):
    res = []
    for i in range(0, len(data)):
        for step in reversed(range(1, backward_time_step + 1)):
            res.append(data[max(i - step, 0)])

        res.append(data[i])

        for step in range(1, forward_time_step + 1):
            res.append(data[min(i + step, data.shape[0] - 1)])

    res = np.asarray(res)
    res = res.reshape(data.shape[0], backward_time_step + 1 + forward_time_step, data.shape[1])
    return res
