import sys
import plotly

from plotly.graph_objs import Scatter
from utils.read_samples import read_samples

TEST_NAME = sys.argv[1]

diffs = []
samples = read_samples('token-timing.db', TEST_NAME)

for sample in samples:
    diff = float(sample['x_runtime_0']) - float(sample['x_runtime_1'])
    diffs.append(diff)

# Create a trace
trace = Scatter(
    x=range(len(diffs)),
    y=diffs,
    mode='markers'
)

data = [trace]

# Plot!
plotly.offline.plot(data)
