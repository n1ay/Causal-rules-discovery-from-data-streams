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

import sys;
sys.path.append('./detectors/')
sys.path.insert(0, './rules_mining/')
import numpy as np
import pandas as pd
import encoders as en

from utils import *
from online_simulator import OnlineSimulator
from adwin_detector import AdwinDetector
from rules_detector import RulesDetector


#Numerical data
#df = pd.read_csv('sequences/sequence_2017_11_24-20.16.00.csv')
df = pd.read_csv('sequences/sequence_2018_04_15-22.22.16.csv')
seq_1 = np.array(df['attr_1'])
seq_2 = np.array(df['attr_4'])

detector_1 = AdwinDetector(delta = 0.01)
detector_2 = AdwinDetector(delta = 0.01)

rules_detector = RulesDetector(target_seq_index=1)

simulator = OnlineSimulator(rules_detector,
                            [detector_1, detector_2],
                            [seq_1, seq_2],
                            ['attr_1', 'attr_2'])

simulator.run(plot=True, detect_rules=True)

print_rules(simulator.get_rules_sets(), 1)
