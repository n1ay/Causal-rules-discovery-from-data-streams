import argparse
import pandas as pd
from pgmpy.models import BayesianModel
import networkx as nx
import matplotlib.pyplot as plt
from dataset_predict.metrics import present_results
from config import test_data_percent

draw_options = {
    'node_color': 'blue',
    'node_size': 1400,
    'alpha': 0.3,
    'width': 1,
    'arrowstyle': '->',
    'arrowsize': 25
}

model_memory_window = 5

def create_model():
    return BayesianModel([
        ('v_00', 'v_01'),
        ('v_00', 'v_20'),
        ('v_01', 'v_02'),
        ('v_01', 'v_21'),
        ('v_02', 'v_03'),
        ('v_02', 'v_22'),
        ('v_03', 'v_04'),
        ('v_03', 'v_23'),
        ('v_04', 'v_05'),
        ('v_04', 'v_24'),
        ('v_10', 'v_11'),
        ('v_10', 'v_20'),
        ('v_11', 'v_12'),
        ('v_11', 'v_21'),
        ('v_12', 'v_13'),
        ('v_12', 'v_22'),
        ('v_13', 'v_14'),
        ('v_13', 'v_23'),
        ('v_14', 'v_15'),
        ('v_14', 'v_24'),
        ('v_05', 'v_25'),
        ('v_15', 'v_25'),
        ('v_20', 'v_21'),
        ('v_21', 'v_22'),
        ('v_22', 'v_23'),
        ('v_23', 'v_24'),
        ('v_24', 'v_25'),
    ])


def add_leading_zeros(number):
    result = str(number)
    for i in range(len(str(model_memory_window)) - len(str(number))):
        result = '0' + result
    return result


def prepare_data(df, model_params):
    values = df.values
    data = pd.DataFrame()
    for i in range(model_params):
        for j in range(model_memory_window + 1):
            data['v_{0}{1}'.format(i, add_leading_zeros(j))] = values[j: len(df) - model_memory_window + j, i]
    return data


def main():
    # CLI parser
    parser = argparse.ArgumentParser(description='Bayesian Network-Test Tool.')
    parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
    args = parser.parse_args()

    # load dataset
    df = pd.read_csv(args.input)
    model_params = len(df.columns)
    data = prepare_data(df, model_params)
    data_train = data.iloc[0:int(len(data) * (100 - test_data_percent) / 100), :]
    data_test = data.iloc[len(data_train):, -1:]
    data_test_predict = data.iloc[len(data_train):, :-1]

    print('Loaded data: ', args.input, '\ndata_train.shape: ', data_train.shape, '\ndata_test_predict.shape: ', data_test_predict.shape)

    model = create_model()
    model.fit(data_train)
    predicted_data = model.predict(data_test_predict)
    nx.drawing.nx_pylab.draw_networkx(model, **draw_options)
    plt.show()
    present_results(data_test, predicted_data, 'Bayesian Model')

if __name__ == '__main__':
    main()
