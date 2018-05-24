import numpy as np
import pandas as pd
import argparse
import time
import sys; sys.path.append('./dataset_transform/')
from trend import Trend, TrendList
from group_trend import GroupTrend, GroupTrendList
from group_stream import GroupStream
from rules_stream import RulesStream

parser = argparse.ArgumentParser(description='Sequence Transform Tool.')
parser.add_argument('-i','--input', help='Config input file name',required=True)
parser.add_argument('-s','--save', action="store_true", help='Save generated sequence?', default=False, required=False)
args = parser.parse_args()

df = pd.read_csv(args.input)

tl, gl, attr = [], [], []
j=0
for i in df.columns:
    attr.append(i)
    tl.append(TrendList(i, np.array(df[i]), merge_at_once=True, merge_threshold=2))
    gl.append(GroupTrendList(tl[j]))
    j+=1
#print(tl)
#print(gl)


gs = GroupStream(gl)
print(gs)


#rs = RulesStream(gs, attr)

if args.save:
    timestr = time.strftime("%Y_%m_%d-%H.%M.%S")
    filename='{0}[rules-gen:{1}].csv'.format(args.input[:-4], timestr)
    with open(filename, 'w') as f:
        f.write(str(rs))
else:
    #print(rs)
    pass