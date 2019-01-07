import unittest
import pandas as pd

from dataset_predict.kfold_data import *
from dataset_predict.metrics import *
from dataset_predict.classifier import Classifier


class SeqPredictTest(unittest.TestCase):

    def test_accuracy1(self):
        df = pd.read_csv("sequences/test_seq1.csv")

        # number of folds
        K = 10
        X_train, X_test, = kfold_data(df, K)
        y_test = [X_test[i][df.columns[-1]] for i in range(len(X_test))]

        classifier = Classifier(lookup=1, merge_threshold=2, fade_threshold=2)
        classifier.fit_kfolded(X_train, X_test)

        # full prediction of kfolded data set
        prediction_kfolded = classifier.predict_kfolded()
        metrics = get_metrics_full(y_test, prediction_kfolded, mean=True)

        expected = [0.772, 0.83580519, 0.772, 0.78547064]
        for i in range(4):
            self.assertAlmostEqual(metrics[i], expected[i], delta=0.0001)


if __name__ == '__main__':
    unittest.main()
