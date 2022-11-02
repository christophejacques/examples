import sys
import datetime
from datetime import datetime as dt

if True:
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

    for p in sys.path:
        print("-", p)

print(sys.version)


class INIT:
    def __init__(self, arg, *args):
        print("INIT:", arg)
        ENTER.__init__(self, *args)


class ENTER:
    def __init__(self, arg1, *arg2):
        print("FUNC:", arg1)
        PARAMS.__init__(self, *arg2)


class PARAMS:
    def __init__(self, arg1, *args):
        print("PARAMS:", arg1, args)


class Test(INIT):
    pass


t = Test(1, 2, 3)
