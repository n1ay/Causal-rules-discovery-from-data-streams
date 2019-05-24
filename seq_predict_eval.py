import argparse
import sys

sys.path.append('./dataset_transform/')
sys.path.append('./dataset_predict/')
from dataset_predict.metrics import *
from dataset_predict.classifier import Classifier
from config import test_data_percent
import time

parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
args = parser.parse_args()

# dataset
df = pd.read_csv(args.input)
df_train = df.iloc[0:int(len(df) * (100 - test_data_percent) / 100), :]
df_test = df.iloc[int(len(df) * (100 - test_data_percent) / 100):, :]
y_test = pd.DataFrame(df_test.iloc[:, -1])

print('Loaded data: ', args.input, '\ndf_train.shape: ', df_train.shape, '\ndf_test.shape: ', df_test.shape)

classifier = Classifier(lookup=1, merge_threshold=2, fade_threshold=2)

# prediction of single stream
start = time.time()
classifier.fit(df_train)
stop = time.time()
fit_time = stop - start
start = time.time()
prediction = classifier.predict(df_test.iloc[:, :-1])
stop = time.time()
predict_time = stop - start

present_results(y_test, prediction, 'QSP')
print('Time elapsed: fit: {0} s, predict: {1} s'.format(fit_time, predict_time))

