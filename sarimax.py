import pandas as pd
import numpy as np
import argparse
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from dataset_predict.metrics import present_results
import statsmodels.api as sm
from config import test_data_percent
import time
import matplotlib.pyplot as plt

# https://www.kaggle.com/poiupoiu/how-to-use-sarimax
# https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html
# https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/

# order = (p, d, q)
SARIMAX_order = (1, 1, 13)
SARIMAX_maxiter = 250
SARIMAX_method = 'lbfgs'


def encode_values(df):
    le = LabelEncoder()
    values = list(set(df.values.reshape(1, -1)[0]))
    le.fit(values)
    classes = len(values)
    encoded_values = le.transform(df.values.reshape(1, -1)[0])
    return encoded_values.reshape(df.shape), le, classes

def find_delta_indices(data):
    lst = data.tolist()
    delta_indices = [(i, lst[i]) for i in range(len(lst))]
    i = 0
    while i < len(delta_indices) - 1:
        if delta_indices[i][1] == delta_indices[i + 1][1]:
            del delta_indices[i + 1]
        else:
            i += 1
    return [v[0] for v in delta_indices]

def find_next_delta_index(index, delta_indices):
    for i in range(len(delta_indices) - 1):
        if index >= delta_indices[i] and index < delta_indices[i + 1]:
            return delta_indices[i + 1]

    return -1

def single_transform(data, index, delta_indices):
    val = data[index]
    next_delta = find_next_delta_index(index, delta_indices)
    if next_delta < 0:
        return val
    return val + (data[next_delta] - val) / (next_delta - index)

def apply_transform(data):
    delta_indices = find_delta_indices(data)
    return [single_transform(data, i, delta_indices) for i in range(len(data))]

def main():
    # CLI parser
    parser = argparse.ArgumentParser(description='SARIMAX-Test Tool.')
    parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
    args = parser.parse_args()

    # load dataset
    df = pd.read_csv(args.input)
    encoded_df, le, classes = encode_values(df)
    encoded_df = np.array(encoded_df, dtype=float)
    #for c in range(encoded_df.shape[1]):
    #    encoded_df[:, c] = apply_transform(encoded_df[:, c])

    series = encoded_df[:, (encoded_df.shape[1] - 1):]
    exog = encoded_df[:, 0:(encoded_df.shape[1] - 1)]

    series_train = series[0:int(len(series) * (100 - test_data_percent) / 100)]
    series_test = series[len(series_train):]
    series_test_raw = df.iloc[len(series_train):, df.shape[1] - 1]

    exog_train = exog[0:int(len(exog) * (100 - test_data_percent) / 100), :]
    exog_test = exog[len(exog_train):, :]

    print('Loaded data: ', args.input, '\nseries_train.shape: ', series_train.shape, '\nseries_test.shape: ',
          series_test.shape, '\nexog_train.shape: ', exog_train.shape, '\nexog_test.shape: ', exog_test.shape)

    # draw ACF, PACF
    fig, ax = plt.subplots(2, 1, figsize=(20, 10))
    sm.graphics.tsa.plot_acf(pd.DataFrame(series_train).diff(), lags=25, ax=ax[0])
    sm.graphics.tsa.plot_pacf(pd.DataFrame(series_train).diff(), lags=25, ax=ax[1])
    plt.show()

    # resDiff = sm.tsa.arma_order_select_ic(series_train, max_ar=20, max_ma=20, ic='aic', trend='nc')
    # print('ARMA(p,q) =', resDiff['aic_min_order'], 'is the best.')

    start = time.time()
    model = SARIMAX(endog=series_train, exog=exog_train, order=SARIMAX_order, enforce_stationarity=False,
                    enforce_invertibility=False)
    model_fitted = model.fit(disp=1, maxiter=SARIMAX_maxiter, method=SARIMAX_method)

    pred = model_fitted.predict(start=len(series_train), end=len(series) - 1, exog=exog_test)
    stop = time.time()
    print('pred.shape: ', pred.shape, ' predictions:\n', pred, '\n\n\n\ntest:\n', series_test.flatten())
    mse = mean_squared_error(series_test, pred)
    print('mse: ', mse)

    pred = le.inverse_transform(pred.round().astype(int))
    series_test_raw = pd.DataFrame(series_test_raw)
    pred = pd.DataFrame(pred)

    present_results(series_test_raw, pred, 'SARIMAX')
    print('Time elapsed: {0} s'.format(stop - start))


if __name__ == '__main__':
    main()
