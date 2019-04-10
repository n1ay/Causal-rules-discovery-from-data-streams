import argparse
import sys

sys.path.append('./dataset_transform/')
sys.path.append('./dataset_predict/')
from dataset_predict.metrics import *
from dataset_predict.classifier import Classifier
from config import test_data_percent

parser = argparse.ArgumentParser(description='Sequence Predict-Test Tool.')
parser.add_argument('-i', '--input', help='Input file name with csv sequence', required=True)
args = parser.parse_args()

# dataset
df = pd.read_csv(args.input)
df_train = df.iloc[0:int(len(df) * (100 - test_data_percent) / 100), :]
df_test = df.iloc[int(len(df) * (100 - test_data_percent) / 100):, :]
y_test = pd.DataFrame(df_test.iloc[:, -1])

classifier = Classifier(lookup=1, merge_threshold=2, fade_threshold=2)

# prediction of single stream
classifier.fit(df_train)
prediction = classifier.predict(df_test.iloc[:, :-1])

present_results(y_test, prediction, 'QSP')