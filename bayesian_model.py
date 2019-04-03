import argparse
import pandas as pd
from pgmpy.models import BayesianModel
import networkx as nx
import matplotlib.pyplot as plt
from dataset_predict.metrics import print_metrics, get_metrics

draw_options = {
    'node_color': 'blue',
    'node_size': 1400,
    'alpha': 0.3,
    'width': 1,
    'arrowstyle': '->',
    'arrowsize': 25
}

model_memory_window = 25
test_data_percent = 10

def create_model():
    return BayesianModel([
        ('v_000', 'v_001'),
        ('v_000', 'v_200'),
        ('v_001', 'v_002'),
        ('v_001', 'v_201'),
        ('v_002', 'v_003'),
        ('v_002', 'v_202'),
        ('v_003', 'v_004'),
        ('v_003', 'v_203'),
        ('v_004', 'v_005'),
        ('v_004', 'v_204'),
        ('v_005', 'v_006'),
        ('v_005', 'v_205'),
        ('v_006', 'v_007'),
        ('v_006', 'v_206'),
        ('v_007', 'v_008'),
        ('v_007', 'v_207'),
        ('v_008', 'v_009'),
        ('v_008', 'v_208'),
        ('v_009', 'v_010'),
        ('v_009', 'v_209'),
        ('v_010', 'v_011'),
        ('v_010', 'v_210'),
        ('v_011', 'v_012'),
        ('v_011', 'v_211'),
        ('v_012', 'v_013'),
        ('v_012', 'v_212'),
        ('v_013', 'v_014'),
        ('v_013', 'v_213'),
        ('v_014', 'v_015'),
        ('v_014', 'v_214'),
        ('v_015', 'v_016'),
        ('v_015', 'v_215'),
        ('v_016', 'v_017'),
        ('v_016', 'v_216'),
        ('v_017', 'v_018'),
        ('v_017', 'v_217'),
        ('v_018', 'v_019'),
        ('v_018', 'v_218'),
        ('v_019', 'v_020'),
        ('v_019', 'v_219'),
        ('v_020', 'v_021'),
        ('v_020', 'v_220'),
        ('v_021', 'v_022'),
        ('v_021', 'v_221'),
        ('v_022', 'v_023'),
        ('v_022', 'v_222'),
        ('v_023', 'v_024'),
        ('v_023', 'v_223'),
        ('v_024', 'v_025'),
        ('v_024', 'v_224'),
        ('v_100', 'v_101'),
        ('v_100', 'v_200'),
        ('v_101', 'v_102'),
        ('v_101', 'v_201'),
        ('v_102', 'v_103'),
        ('v_102', 'v_202'),
        ('v_103', 'v_104'),
        ('v_103', 'v_203'),
        ('v_104', 'v_105'),
        ('v_104', 'v_204'),
        ('v_105', 'v_106'),
        ('v_105', 'v_205'),
        ('v_106', 'v_107'),
        ('v_106', 'v_206'),
        ('v_107', 'v_108'),
        ('v_107', 'v_207'),
        ('v_108', 'v_109'),
        ('v_108', 'v_208'),
        ('v_109', 'v_110'),
        ('v_109', 'v_209'),
        ('v_110', 'v_111'),
        ('v_110', 'v_210'),
        ('v_111', 'v_112'),
        ('v_111', 'v_211'),
        ('v_112', 'v_113'),
        ('v_112', 'v_212'),
        ('v_113', 'v_114'),
        ('v_113', 'v_213'),
        ('v_114', 'v_115'),
        ('v_114', 'v_214'),
        ('v_115', 'v_116'),
        ('v_115', 'v_215'),
        ('v_116', 'v_117'),
        ('v_116', 'v_216'),
        ('v_117', 'v_118'),
        ('v_117', 'v_217'),
        ('v_118', 'v_119'),
        ('v_118', 'v_218'),
        ('v_119', 'v_120'),
        ('v_119', 'v_219'),
        ('v_120', 'v_121'),
        ('v_120', 'v_220'),
        ('v_121', 'v_122'),
        ('v_121', 'v_221'),
        ('v_122', 'v_123'),
        ('v_122', 'v_222'),
        ('v_123', 'v_124'),
        ('v_123', 'v_223'),
        ('v_124', 'v_125'),
        ('v_124', 'v_224'),
        ('v_025', 'v_225'),
        ('v_125', 'v_225'),
        ('v_200', 'v_201'),
        ('v_201', 'v_202'),
        ('v_202', 'v_203'),
        ('v_203', 'v_204'),
        ('v_204', 'v_205'),
        ('v_205', 'v_206'),
        ('v_206', 'v_207'),
        ('v_207', 'v_208'),
        ('v_208', 'v_209'),
        ('v_209', 'v_210'),
        ('v_210', 'v_211'),
        ('v_211', 'v_212'),
        ('v_212', 'v_213'),
        ('v_213', 'v_214'),
        ('v_214', 'v_215'),
        ('v_215', 'v_216'),
        ('v_216', 'v_217'),
        ('v_217', 'v_218'),
        ('v_218', 'v_219'),
        ('v_219', 'v_220'),
        ('v_220', 'v_221'),
        ('v_221', 'v_222'),
        ('v_222', 'v_223'),
        ('v_223', 'v_224'),
        ('v_224', 'v_225'),
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
    parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
    parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
    args = parser.parse_args()

    # load dataset
    df = pd.read_csv(args.input)
    df = df[::10]
    model_params = len(df.columns)
    data = prepare_data(df, model_params)
    data_train = data.iloc[0:int(len(data) * (100 - test_data_percent) / 100), :]
    data_test = data.iloc[len(data_train):, -1:]
    data_test_predict = data.iloc[len(data_train):, :-1]

    print('Loaded data: ', args.input, '\ndata_train.shape: ', data_train.shape, '\ndata_test_predict.shape: ', data_test_predict.shape)

    model = create_model()
    model.fit(data_train)
    predicted_data = model.predict(data_test_predict)
    print('predicted: \n', predicted_data, '\nexpected: \n', data_test)
    nx.drawing.nx_pylab.draw_networkx(model, **draw_options)
    plt.show()
    print_metrics(get_metrics(data_test, predicted_data))
    print('END')

if __name__ == '__main__':
    main()
