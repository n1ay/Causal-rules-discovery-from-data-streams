# https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# https://machinelearningmastery.com/make-predictions-time-series-forecasting-python/
# https://colab.research.google.com/drive/134oEzWiJ6s8v41MpUVLFD82XKCr1g9DZ#scrollTo=x1aY5EBRYAoD

import pandas as pd
import argparse
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import KFold
import dataset_predict.metrics

epochs = 10
batch_size = 1
K = 10


def encode_values(df):
    le = LabelEncoder()
    values = list(set(df.values.reshape(1, -1)[0]))
    le.fit(values)
    encoded_values = le.transform(df.values.reshape(1, -1)[0])
    return encoded_values.reshape(df.shape)


def main():
    parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
    parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
    args = parser.parse_args()

    # dataset
    df = pd.read_csv(args.input)
    encoded_df = encode_values(df)
    X = encoded_df[:, 0:(encoded_df.shape[1] - 1)]
    y = encoded_df[:, (encoded_df.shape[1] - 1):]

    X_train, X_test, y_train, y_test = [], [], [], []
    kf = KFold(n_splits=K, shuffle=False)
    for train_index, test_index in kf.split(X):
        X_train.append((X[train_index]))
        y_train.append((y[train_index]))
        X_test.append((X[test_index]))
        y_test.append((y[test_index]))

    X_train = [x.reshape(x.shape[0], 1, x.shape[1]) for x in X_train]
    X_test = [x.reshape(x.shape[0], 1, x.shape[1]) for x in X_test]

    model = Sequential()
    model.add(LSTM(50, input_shape=(X_train[0].shape[1], X_train[0].shape[2])))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')

    y_predict = []
    for i in range(len(X_train)):
        history = model.fit(X_train[i], y_train[i], initial_epoch=i * epochs, epochs=(i + 1) * epochs,
                            batch_size=batch_size, validation_data=(X_test[i], y_test[i]),
                            verbose=1, shuffle=False)
        y_predict.append(model.predict(X_test[i]))

    for i in range(len(y_predict)):
        y_predict[i] = [round(j[0]) for j in y_predict[i]]

    y_test2 = []
    for i in range(len(y_test)):
        y_test2.append([j[0] for j in y_test[i]])

    print(dataset_predict.metrics.print_metrics(dataset_predict.metrics.get_metrics_full(y_test2, y_predict)))

if __name__ == '__main__':
    main()
