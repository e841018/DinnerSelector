# calculate MAP
# s = 'xxooxoooxxoxxoxxoooxooxxxoxoxx'# MVNLab
s = 'xoooxoxoxoooxoxxxoxxoxxxxxxoox'# huzixiao
a = 0
n = 0
Sum = 0
for i in s:
    n += 1
    if i == 'o':
        a += 1
        Sum += a/n
print(Sum/len(s))