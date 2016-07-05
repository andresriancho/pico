import sys
import requests
requests.packages.urllib3.disable_warnings()

import plotly

from plotly.graph_objs import Histogram, Layout, Figure
from utils.read_samples import read_timing_samples

TEST_NAME = sys.argv[1]

# Should be different (success and fail)
x0 = read_timing_samples('token-timing.db', TEST_NAME, '224a93060c0dd4fb931d05083b4cb7b6a8000000', 'x_runtime_0')
x1 = read_timing_samples('token-timing.db', TEST_NAME, '224a93060c0dd4fb931d05083b4cb7b6a1000000', 'x_runtime_1')

# Should be equal (two fails)
x2 = read_timing_samples('token-timing.db', TEST_NAME, '224a93060c0dd4fb931d05083b4cb7b6a7000000', 'x_runtime_0')
x3 = read_timing_samples('token-timing.db', TEST_NAME, '224a93060c0dd4fb931d05083b4cb7b6a0000000', 'x_runtime_1')

assert x0
assert x1
assert x2
assert x3

sample_ok = Histogram(
    x=x0,
    name='Success (takes longer)',
    histnorm='count',
    opacity=0.4
)

sample_fail = Histogram(
    x=x1,
    name='Fail #1',
    histnorm='count',
    opacity=0.4
)

sample_fail_2 = Histogram(
    x=x1,
    name='Fail #2',
    histnorm='count',
    opacity=0.4
)

sample_fail_3 = Histogram(
    x=x1,
    name='Fail #3',
    histnorm='count',
    opacity=0.4
)

data = [sample_ok, sample_fail, sample_fail_2, sample_fail_3]
layout = Layout(
    barmode='overlay',
    xaxis=dict(
        title='Response time (ms)'
    ),
    yaxis=dict(
        title='Count'
    ),
    bargap=0.0,
    bargroupgap=0.0
)

fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig)
