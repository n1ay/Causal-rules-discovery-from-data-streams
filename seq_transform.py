import numpy as np
import pandas as pd
import argparse
import time
import sys; sys.path.append('./dataset_transform/')
from trend import Trend, TrendList
from group_stream import GroupStream
from rules_stream import RulesStream

parser = argparse.ArgumentParser(description='Sequence Transform Tool.')
parser.add_argument('-i','--input', help='Config input file name',required=True)
parser.add_argument('-s','--save', action="store_true", help='Save generated sequence?', default=False, required=False)
args = parser.parse_args()

df = pd.read_csv(args.input)

window_size=25
prob_threshold=0.65

tl = []
attr = []
for i in df.columns:
    attr.append(i)
    tl.append(TrendList(i, np.array(df[i]), prob_threshold, window_size, merge_at_once=True))

gs = GroupStream(tl)
#print(gs)

rs = RulesStream(gs, attr)


if args.save:
    timestr = time.strftime("%Y_%m_%d-%H.%M.%S")
    filename='{0}[rules-gen:{1}].csv'.format(args.input[:-4], timestr)
    with open(filename, 'w') as f:
        f.write(str(rs))
else:
    print(rs)