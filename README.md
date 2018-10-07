# Qualitative stream prediction using causal rules discovery

## Using predictor ##
If you want to test predictor accuracy with K-folding dataset use:

`python3.5 seq_predict_test.py -i sequences/sequence1_0_noise_clean.csv`

- `-i` input file

Or, if you want to use it for prediction use:

`python3.5 seq_predict.py -if sequences/sequence1_0_noise_clean_f.csv -ip sequences/sequence1_0_noise_clean_p.csv`

- `-if` input file to fit classifier
- `-ip` input file to predict last column


## Using sequence generator
Example:
`python seqgen.py -i configs/config_file -s`

- `-i` input file
- `-s` save generated sequence in sequences/ directory
- `-h` help

## Plotting sequences
`python plot_sequence.py -i sequences/sequence.csv -s 0`

- `-s` start X axis from 0

## Adding rules to the stream
`./add_attr.sh -i configs/new_test -r configs/rules`
- `-i` input file
- `-r` rules file
- `-h` help

For a file new_test as below:
```
attr='a';value=1;domain=[1,2,3,4]; from=-300;to=-280;probability=0.8
attr='a';value=2;domain=[1,2,3,4]; from=-280;to=-250;probability=0.8
attr='a';value=1;domain=[1,2,3,4]; from=-200;to=-150;probability=0.8
attr='a';value=2;domain=[1,2,3,4]; from=-150;to=0;probability=0.8
attr='b';value=2;domain=[1,2,3,4]; from=-200;to=-150;probability=0.8
attr='b';value=3;domain=[1,2,3,4]; from=-150;to=0;probability=0.8
```
and rules:
```
attr='c';value=(a=1->2,b=2->3,1->3);domain=([1,2,3,4]->[2,3,4]);probability=(0.8->0.9);parts=(1,2);after=0
```
Executing script for these two files produces an output:
```
attr='c';value=1;domain=[1,2,3,4];from=-200;to=-150;probability=0.8
attr='c';value=3;domain=[2,3,4];from=-150;to=0;probability=0.9
```
About rules file:
  * `attr='c';` add an attribute named `c`
  * `value=(a=1->2,b=2->3,1->3);` when `a` changes value from 1 to 2 and `b` changes value from 2 to 3 then `c` attribute changes value from 1 to 3
  * `domain=([1,2,3,4]->[2,3,4]);` and its domain change from `[1,2,3,4]` to `[2,3,4]`
  * `probability=(0.8->0.9);` and probability of set value changes from `0.8` to `0.9`
  * `parts=(1,2);` add both parts of the rule. Look up there are two parts in the output, if you want only one of them just use `parts=(1);` or `parts=(2);`
  * `after=0` add this rule shifted by `0` in comparision with `a` and `b` attributes. If you want to shift rule backward just use negative value.

## Shifting the stream ##
`./shift.sh configs/new_test -600`
`-600` is how much you want to shift the stream, `-600` means 600 units backward.

Produced output for new_test file:
```
attr='a';value=1;domain=[1,2,3,4];from=-900;to=-880;probability=0.8
attr='a';value=2;domain=[1,2,3,4];from=-880;to=-850;probability=0.8
attr='a';value=1;domain=[1,2,3,4];from=-800;to=-750;probability=0.8
attr='a';value=2;domain=[1,2,3,4];from=-750;to=-600;probability=0.8
attr='b';value=2;domain=[1,2,3,4];from=-800;to=-750;probability=0.8
attr='b';value=3;domain=[1,2,3,4];from=-750;to=-600;probability=0.8
```

## Mining rules ##
`python3.5 seq_transform.py -i sequences/sequence.csv -s`

- `-i` input
- `-s` save rules in sequence directory
