from enum import Enum, auto


class InstanceOnly: ...


class MonEnum(Enum):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isInstanceOnly = isinstance(args[0], InstanceOnly)


class Variable(MonEnum):
    UN = auto()
    DEUX = InstanceOnly()
    TROIS = InstanceOnly()


print(Variable.UN, Variable.UN.isInstanceOnly)
print(Variable.DEUX, Variable.DEUX.isInstanceOnly)
print(Variable.TROIS, Variable.TROIS.isInstanceOnly)

print(Variable.DEUX, id(Variable.DEUX))
print(Variable.TROIS, id(Variable.TROIS))
