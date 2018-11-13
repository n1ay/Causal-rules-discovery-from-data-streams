def transfrom_list_into_categorical_vector_list(lst, classes):
    return [[1 if val == i else 0 for i in range(classes) ] for val in lst]

def transfrom_categorical_vector_list_into_list(lst):
    return [sublist.index(max(sublist)) for sublist in lst]