# https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# https://machinelearningmastery.com/make-predictions-time-series-forecasting-python/
# https://colab.research.google.com/drive/134oEzWiJ6s8v41MpUVLFD82XKCr1g9DZ#scrollTo=x1aY5EBRYAoD
# http://colah.github.io/posts/2015-08-Understanding-LSTMs/
# http://karpathy.github.io/2015/05/21/rnn-effectiveness/

import argparse

import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense
from keras.models import Sequential
from sklearn.preprocessing import LabelEncoder

from config import test_data_percent
from dataset_predict.metrics import present_results
from utils.utils import transform_list_into_categorical_vector_list as tlc, \
    reshape_data_to_lstm

epochs = 15
batch_size = 10

LSTM_nodes = 64
backward_time_step = 3
forward_time_step = 3
dropout = 0.2


def encode_values(df):
    le = LabelEncoder()
    values = list(set(df.values.reshape(1, -1)[0]))
    le.fit(values)
    classes = len(values)
    encoded_values = le.transform(df.values.reshape(1, -1)[0])
    encoded_values = np.asarray(tlc(encoded_values, classes)).reshape(1, -1)[0]
    encoded_values = np.asarray(encoded_values)
    return encoded_values.reshape(df.shape[0], df.shape[1] * classes), le, classes


def main():
    # CLI parser
    parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
    parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
    args = parser.parse_args()

    # load dataset
    df = pd.read_csv(args.input)
    encoded_df, le, classes = encode_values(df)
    X = encoded_df[:, 0:(encoded_df.shape[1] - classes)]
    y = encoded_df[:, (encoded_df.shape[1] - classes):]

    X_train = (X[0:int(len(X) * (100 - test_data_percent) / 100)])
    y_train = (y[0:int(len(X) * (100 - test_data_percent) / 100)])
    X_test = (X[int(len(X) * (100 - test_data_percent) / 100):])
    y_test = (y[int(len(X) * (100 - test_data_percent) / 100):])
    y_raw_test = pd.DataFrame(df.iloc[int(len(X) * (100 - test_data_percent) / 100):, len(df.columns) - 1])

    X_train = reshape_data_to_lstm(X_train, backward_time_step, forward_time_step)
    X_test = reshape_data_to_lstm(X_test, backward_time_step, forward_time_step)

    # create LSTM NN
    model = Sequential()
    model.add(LSTM(LSTM_nodes, recurrent_dropout=dropout))
    model.add(Dense(classes * classes, activation='relu'))
    model.add(Dense(classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    history = model.fit(X_train, y_train, initial_epoch=0, epochs=epochs,
                        batch_size=batch_size, validation_data=(X_test, y_test),
                        verbose=1, shuffle=False)
    y_predict_categorical = model.predict(X_test)
    y_predict_encoded = [np.argmax(y_predict_categorical[i, :]) for i in range(y_predict_categorical.shape[0])]
    y_predict = le.inverse_transform(y_predict_encoded)
    y_predict = pd.DataFrame(y_predict)

    present_results(y_raw_test, y_predict, 'LSTM')


if __name__ == '__main__':
    main()
