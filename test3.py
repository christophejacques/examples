import itertools

print(dir(itertools))
print(help(itertools.repeat))

n = 10
for x in itertools.repeat(1, n):
    n -= 2
    print(n, x)
