# https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# https://machinelearningmastery.com/make-predictions-time-series-forecasting-python/
# https://colab.research.google.com/drive/134oEzWiJ6s8v41MpUVLFD82XKCr1g9DZ#scrollTo=x1aY5EBRYAoD
# http://colah.github.io/posts/2015-08-Understanding-LSTMs/
# http://karpathy.github.io/2015/05/21/rnn-effectiveness/

import numpy as np
import pandas as pd
import argparse
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import KFold
import dataset_predict.metrics
from utils.utils import transform_list_into_categorical_vector_list as tlc,\
    transform_categorical_vector_list_into_list as tcv, reshape_data_to_lstm

epochs = 10
batch_size = 10
K = 10

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
    return encoded_values.reshape(df.shape[0], df.shape[1] * classes), classes


def main():
    #CLI parser
    parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
    parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
    args = parser.parse_args()

    #load dataset
    df = pd.read_csv(args.input)
    encoded_df, classes = encode_values(df)
    X = encoded_df[:, 0:(encoded_df.shape[1] - 1)]
    y = encoded_df[:, (encoded_df.shape[1] - 1):]
    y_categorical = tlc(y, classes)
    y_categorical = np.asarray(y_categorical)
    y_categorical.reshape(df.shape[0], 1, classes)

    X_train, X_test, y_train, y_test, y_raw_test = [], [], [], [], []
    kf = KFold(n_splits=K, shuffle=False)
    for train_index, test_index in kf.split(X):
        X_train.append((X[train_index]))
        y_train.append((y_categorical[train_index]))
        X_test.append((X[test_index]))
        y_test.append((y_categorical[test_index]))
        y_raw_test.append((y[test_index]).flatten().tolist())

    X_train = [reshape_data_to_lstm(x, backward_time_step, forward_time_step) for x in X_train]
    X_test = [reshape_data_to_lstm(x, backward_time_step, forward_time_step) for x in X_test]

    #create LSTM NN
    model = Sequential()
    model.add(LSTM(LSTM_nodes, recurrent_dropout=dropout))
    model.add(Dense(classes * classes, activation='relu'))
    model.add(Dense(classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    weights = model.get_weights()

    y_predict_categorical = []
    for i in range(len(X_train)):
        model.set_weights(weights)
        history = model.fit(X_train[i], y_train[i], initial_epoch=i * epochs, epochs=(i + 1) * epochs,
                            batch_size=batch_size, validation_data=(X_test[i], y_test[i]),
                            verbose=1, shuffle=False)
        y_predict_categorical.append(model.predict(X_test[i]))

    y_predict = [tcv(sublist.tolist()) for sublist in y_predict_categorical]

    dataset_predict.metrics.print_metrics(dataset_predict.metrics.get_metrics_full(y_raw_test, y_predict))

if __name__ == '__main__':
    main()
