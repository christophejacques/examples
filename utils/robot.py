# from utils.operation import *

def fibonnacci(n):
    if n < 3: return 1
    return fibonnacci(n-2) + fibonnacci(n-1)

def fib(n):
    if n < 3: return 1
    s = 0
    s1 = 1
    s2 = 1
    for _ in range(n-2):
        s = s1 + s2
        s1, s2 = s, s1
    return s

print("Suite de fibonnacci(x)")
for x in range(1000, 1004):
    print(fib(x))
print("\n")

def factoriel(x):
    p = 1
    for i in range(2, x+1):
        p *= i
    return p

class Robot:

    def __init__(self, name, build_year, lk=0.5, lp=0.5):
        self.name = name
        self.build_year = build_year
        self.__potential_physical = lk
        self.__potential_psychic = lp

    @property
    def condition(self):
        s = self.__potential_physical + self.__potential_psychic
        if s <= -1:
            return "I feel miserable!"
        elif s <= 0:
            return "I feel bad!"
        elif s <= 0.5:
            return "Could be worse!"
        elif s <= 1:
            return "Seems to be okay!"
        else:
            return "Great!"


def exemple1():
    x = Robot("Marvin", 1979, 0.2, 0.4)
    y = Robot("Caliban", 1993, -0.4, 0.3)
    print(x.condition)
    print(y.condition)


fct = {
    "+": lambda *x: x[0] + x[1],
    "-": lambda *x: x[0] - x[1],
    "*": lambda *x: x[0] * x[1],
    "!": lambda x: factoriel(x)
      }

if True:
    reverseParams = lambda *v: [x for x in reversed(v)]
    reverseListe  = lambda l: l[::-1]


    print(fct["+"](5, 9))
    print(fct["-"](5, 9))
    print(fct["*"](5, 9))
    print(fct["!"](5))
    print()

    print(reverseParams(5, 9, 3, 7))
    print(reverseListe([1, 2, 3, 4]))
    print(reverseListe((5, 6, 7, 8)))

    print([1,2]+[3,4])
    print((5,6)+(7,8))
    print(sorted([5, 2, 8, 1, 9]))
    print("{0}".format([1,2,3]))

from msvcrt import getch
# getch()