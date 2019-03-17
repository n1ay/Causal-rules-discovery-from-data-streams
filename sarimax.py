import pandas as pd
import numpy as np
import argparse
from sklearn.preprocessing import LabelEncoder
from statsmodels.tsa.statespace.sarimax import SARIMAX
import dataset_predict.metrics

test_data_percent = 10

#order = (p, d, q)
SARIMAX_order = (1, 0, 0)


def encode_values(df):
    le = LabelEncoder()
    values = list(set(df.values.reshape(1, -1)[0]))
    le.fit(values)
    classes = len(values)
    encoded_values = le.transform(df.values.reshape(1, -1)[0])
    return encoded_values.reshape(df.shape), classes


def main():
    # CLI parser
    parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
    parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
    args = parser.parse_args()

    # load dataset
    df = pd.read_csv(args.input)
    encoded_df, classes = encode_values(df)
    series = encoded_df[:, (encoded_df.shape[1] - 1):]
    exog = encoded_df[:, 0:(encoded_df.shape[1] - 1)]

    series_train = series[0:int(len(series)*(100 - test_data_percent)/100)]
    series_test = series[len(series_train):]

    exog_train = exog[0:int(len(exog)*(100 - test_data_percent)/100), :]
    exog_test = exog[len(exog_train):, :]

    print('Loaded data: ', args.input, '\nseries_train.shape: ', series_train.shape, '\nseries_test.shape: ', series_test.shape, '\nexog_train.shape: ', exog_train.shape, '\nexog_test.shape: ', exog_test.shape)

    model = SARIMAX(endog=series_train, exog=exog_train, order=SARIMAX_order, enforce_stationarity=False, enforce_invertibility=False)
    model_fitted = model.fit(disp=1)

    pred = model_fitted.predict(start=len(series_train), end=len(series) - 1, exog=exog_test)
    pred = pred.round().astype(int)
    print('pred.shape: ', pred.shape, '\n', pred, '\n\n\n\n', series_test.flatten())

    #dataset_predict.metrics.print_metrics(dataset_predict.metrics.get_metrics_full(test, predictions))
    print('test')

if __name__ == '__main__':
    main()
