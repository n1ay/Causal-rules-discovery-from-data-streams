# The MIT License
# Copyright (c) 2018 Kamil Jurek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
sys.path.append('./detectors/')
sys.path.append('../../dataset_predict/')
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from scipy import signal
from online_simulator import OnlineSimulator
from rules_detector import RulesDetector
from utils import *
from zscore_detector import ZScoreDetector
from adwin_detector import AdwinDetector
from cusum_detector import CusumDetector
from page_hinkley_detector import PageHinkleyDetector
from ddm_detector import DDMDetector
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder
from metrics import present_results

def tlc(lst, classes):
    return [[1 if val == i else 0 for i in range(classes)] for val in lst]

def encode_values(df):
    le = LabelEncoder()
    values = list(set(df.values.reshape(1, -1)[0]))
    le.fit(values)
    classes = len(values)
    encoded_values = le.transform(df.values.reshape(1, -1)[0])
    encoded_values = np.asarray(encoded_values)
    return DataFrame(encoded_values.reshape(df.shape[0], df.shape[1])), le, classes

# df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
# df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
df = pd.read_csv('../../sequences/9600/sequence2_0_noise_9600.csv')
seq_names = ['a', 'b', 'c', 'd']
df, le, classes = encode_values(df)
df.columns = seq_names

#print(df)

predict_ratio=0.85
base_seqs =[]

for name in seq_names:
    base_seqs.append(np.array(df[name]))

sequences = [[] for i in range(len(base_seqs))]
for nr in range(1):
    for i, seq in enumerate(sequences):
        sequences[i] = np.concatenate((seq, base_seqs[i]))

# CHANGE DETECTION METHOD
METHOD_ZSCORE="zscore"
METHOD_CUSUM="cusum"
METHOD_PAGE_HINKLEY="page-hinkley"
METHOD_ADWIN="adwin"
METHOD_DDM="ddm"

use_method=METHOD_ADWIN

print('change detection method: ', use_method)
# ZScore
if use_method == METHOD_ZSCORE:
    zscore_win_size = 5
    zscore_threshold = 3
    detector1 = ZScoreDetector(window_size=zscore_win_size, threshold=zscore_threshold)
    detector2 = ZScoreDetector(window_size=zscore_win_size, threshold=zscore_threshold)
    detector3 = ZScoreDetector(window_size=zscore_win_size, threshold=zscore_threshold)

# CUSUM
if use_method == METHOD_CUSUM:
    cusum_delta = 0.005
    cusum_lambd = 1000
    detector1 = CusumDetector(delta=cusum_delta, lambd=cusum_lambd)
    detector2 = CusumDetector(delta=cusum_delta, lambd=cusum_lambd)
    detector3 = CusumDetector(delta=cusum_delta, lambd=cusum_lambd)

# Page Hinkley Test
if use_method == METHOD_PAGE_HINKLEY:
    page_hinkley_delta = 0.005
    page_hinkley_lambd = 50
    page_hinkley_alpha = 1 - 0.0001
    detector1 = PageHinkleyDetector(delta=page_hinkley_delta, lambd=page_hinkley_lambd, alpha=page_hinkley_alpha)
    detector2 = PageHinkleyDetector(delta=page_hinkley_delta, lambd=page_hinkley_lambd, alpha=page_hinkley_alpha)
    detector3 = PageHinkleyDetector(delta=page_hinkley_delta, lambd=page_hinkley_lambd, alpha=page_hinkley_alpha)

# ADWIN
if use_method == METHOD_ADWIN:
    adwin_delta1 = float(sys.argv[1])
    adwin_delta2 = float(sys.argv[2])
    adwin_delta3 = float(sys.argv[3])
    adwin_delta4 = float(sys.argv[4])
    #adwin_delta5 = float(sys.argv[5])
    print(adwin_delta1, adwin_delta2, adwin_delta3, adwin_delta4)
    detector1 = AdwinDetector(delta=adwin_delta1)
    detector2 = AdwinDetector(delta=adwin_delta2)
    detector3 = AdwinDetector(delta=adwin_delta3)
    detector4 = AdwinDetector(delta=adwin_delta4)
    #detector5 = AdwinDetector(delta=adwin_delta5)

# DDM
if use_method == METHOD_DDM:
    ddm_lambd = 5
    ddm_delta = 0.001
    detector1 = DDMDetector(lambd=ddm_lambd, delta=ddm_delta)
    detector2 = DDMDetector(lambd=ddm_lambd, delta=ddm_delta)
    detector3 = DDMDetector(lambd=ddm_lambd, delta=ddm_delta)

target_seq_index = len(seq_names) - 1
round_to = 10
rules_detector = RulesDetector(target_seq_index=target_seq_index,
                               window_size=10,
                               round_to=round_to,
                               type="all",
                               combined=False)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],#, detector5],
                            sequences,
                            seq_names,
                            round_to=round_to,
                            predict_ratio=predict_ratio)
#simulator.random_subsequences = False

start_time = time.time()

simulator.run(plot=False, detect_rules=True, predict_seq=False)

#print_detected_change_points(simulator.get_detected_changes())
#print_rules(simulator.get_rules_sets(), 0)

end_time = time.time()
predict_time = end_time - start_time
print('fit time: ', predict_time, 's')

start_time = time.time()
simulator.run(plot=True, detect_rules=True, predict_seq=True)

end_time = time.time()

print('predict time: ', end_time - start_time - predict_time, 's')


#print("Rules used for prediction:")
#for br in simulator.best_rules:
#    print(br)

prediction_start = int(len(sequences[target_seq_index])*predict_ratio)
#predicted = simulator.predictor.predicted[prediction_start:len(sequences[target_seq_index])]
#real = sp.signal.medfilt(sequences[target_seq_index][prediction_start:],21)
#rmse = np.sqrt(((predicted - real) ** 2).mean())
#print('Mean Squared Error: {}'.format(round(rmse, 5)))

#plot_sequences_on_one_figure(sequences, seq_names, simulator, target_seq_index)

#print("Time:", end_time - start_time)

predicted = simulator.predictor.predicted
index = 0
seq_len = len(sequences[target_seq_index])
for i in predicted:
    if i == -1:
        index += 1

predicted = pd.DataFrame(predicted[index:seq_len])
real = pd.DataFrame(sequences[target_seq_index][index:seq_len])

out_len = len(predicted) if len(predicted) < len(real) else len(real)
if len(predicted) != len(real):
    out_len = len(predicted) if len(predicted) < len(real) else len(real)
    predicted = predicted[0:out_len]
    real = real[0:out_len]

#print(len(predicted), predicted, len(real), real)
present_results(real, predicted, 'CRDiS')

#plt.show()
