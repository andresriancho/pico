from scipy import stats
from utils.read_samples import read_samples

x0 = read_samples('token-timing-224a%s.txt' % ('0' * 36,))
x1 = read_samples('token-timing-224c%s.txt' % ('0' * 36,))
x2 = read_samples('token-timing-224a93060c0dd4fb931d05083b4cb7b6a8c27df8.txt')

z_stat, p_val = stats.ranksums(x2, x0)

print('MWW RankSum P for input samples: %s' % p_val)
print('MWW RankSum Z for input samples: %s' % z_stat)
print('')
print('== 0.00  means totally different')
print('<= 0.05  highly confident that the distributions significantly differ')
