import sys
from utils.read_samples import read_samples

TEST_NAME = sys.argv[1]

diffs = []
samples = read_samples('token-timing.db', TEST_NAME)

for sample in samples:
    diff = float(sample['x_runtime_0']) - float(sample['x_runtime_1'])
    diffs.append(diff)

print('Summarized diff without filters: %s' % sum(diffs))

filter_perc = 2.0
diffs.sort()
max_index = int(len(diffs) / 100.0 * (100.0 - filter_perc))
filtered_diffs = diffs[:max_index]
print('Summarized diff removing top %s%% diffs: %s' % (filter_perc, sum(filtered_diffs)))
