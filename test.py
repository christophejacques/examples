import sys
import datetime
from datetime import datetime as dt

print('{:>30}'.format('right aligned'))
print('{:^30}'.format('centered'))
print('{:<30}'.format('left aligned'))
print('{:-^30}'.format(' centered '))

print("{:>30_}".format(1234567890))
print("{:>30.2%}".format(0.78563))

print("{:%Y/%m/%d %H:%M:%S.%f}".format(dt.now()))

print(datetime.date.today().strftime("%d/%m/%Y"))
print("{:%d/%m/%Y}".format(datetime.date.today()))
print(f"{datetime.date.today():%d/%m/%Y}")

print(sys.version)
for p in sys.path:
    print("-", p)
