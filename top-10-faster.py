import sys
import pprint
from utils.read_samples import read_samples

TEST_NAME = sys.argv[1]

runtimes_0 = []
runtimes_1 = []
samples = read_samples('token-timing.db', TEST_NAME)

for sample in samples:
    runtimes_0.append(float(sample['x_runtime_0']))
    runtimes_1.append(float(sample['x_runtime_1']))

token_0 = sample['token_0']
token_1 = sample['token_1']

averages = []

for i, runtime in enumerate((runtimes_0, runtimes_1)):
    runtime.sort()
    runtime = runtime[:10]

    print('Top10 fastest responses for sample %s:' % i)
    pprint.pprint(runtime)

    averages.append(sum(runtime) / len(runtime))

# Are all responses from sample 0 faster than the ones from sample 1?
for avg in averages:
    print('Average slowest response time: %s' % avg)

avg_0 = averages[0]
avg_1 = averages[1]

perc = avg_0 / avg_1

print('Sample #0 is %.2f%% greater than sample #1' % perc)