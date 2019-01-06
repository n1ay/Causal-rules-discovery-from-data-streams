import numpy as np

def transform_list_into_categorical_vector_list(lst, classes):
    return [[1 if val == i else 0 for i in range(classes) ] for val in lst]

def transform_categorical_vector_list_into_list(lst):
    return [sublist.index(max(sublist)) for sublist in lst]

def reshape_data_to_lstm(data, time_step):
  res = []
  for i in range(len(data)):
    for step in reversed(range(time_step)):
      res.append(data[max(i-step, 0)])

  res = np.asarray(res)
  res = res.reshape(data.shape[0], time_step, data.shape[1])
  return res

