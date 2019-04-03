import pandas as pd
import numpy as np
import argparse
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import dataset_predict.metrics
import matplotlib.pyplot as plt
import statsmodels.api as sm

# https://www.kaggle.com/poiupoiu/how-to-use-sarimax
# https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html
# https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/

test_data_percent = 10

#order = (p, d, q)
SARIMAX_order = (7, 0, 16)
SARIMAX_maxiter = 250
SARIMAX_method = 'lbfgs'

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
    df = df[::10]
    encoded_df, classes = encode_values(df)
    series = encoded_df[:, (encoded_df.shape[1] - 1):]
    exog = encoded_df[:, 0:(encoded_df.shape[1] - 1)]

    series_train = series[0:int(len(series)*(100 - test_data_percent)/100)]
    series_test = series[len(series_train):]

    exog_train = exog[0:int(len(exog)*(100 - test_data_percent)/100), :]
    exog_test = exog[len(exog_train):, :]

    print('Loaded data: ', args.input, '\nseries_train.shape: ', series_train.shape, '\nseries_test.shape: ', series_test.shape, '\nexog_train.shape: ', exog_train.shape, '\nexog_test.shape: ', exog_test.shape)

    #fig, ax = plt.subplots(2, 1, figsize=(20, 10))
    #fig = sm.graphics.tsa.plot_acf(pd.DataFrame(series_train).diff(), lags=25, ax=ax[0])
    #fig = sm.graphics.tsa.plot_pacf(pd.DataFrame(series_train).diff(), lags=25, ax=ax[1])
    #plt.show()

    #resDiff = sm.tsa.arma_order_select_ic(series_train, max_ar=20, max_ma=20, ic='aic', trend='nc')
    #print('ARMA(p,q) =', resDiff['aic_min_order'], 'is the best.')

    model = SARIMAX(endog=series_train, exog=exog_train, order=SARIMAX_order, enforce_stationarity=False, enforce_invertibility=False)
    model_fitted = model.fit(disp=1, maxiter=SARIMAX_maxiter, method=SARIMAX_method)

    pred = model_fitted.predict(start=len(series_train), end=len(series) - 1, exog=exog_test)
    pred = pred.round().astype(int)
    print('pred.shape: ', pred.shape, ' predictions:\n', pred, '\n\n\n\ntest:\n', series_test.flatten())
    mse = mean_squared_error(series_test, pred)
    print('mse: ', mse)

    plt.plot(series_test, label='test values')
    plt.plot(pred, label='predicted values')
    plt.xlabel('sample')
    plt.ylabel('value')
    plt.title('SARIMAX predictions of {0}'.format(args.input))
    plt.legend()
    plt.show()

    #dataset_predict.metrics.print_metrics(dataset_predict.metrics.get_metrics_full(test, predictions))
    print('END')

if __name__ == '__main__':
    main()
