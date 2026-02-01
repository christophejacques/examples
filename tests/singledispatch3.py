from functools import singledispatch

@singledispatch
def surcharger(a, b):
    raise NotImplementedError("Type du premier argument non supporté")

# --- Cas où le PREMIER argument est un INT ---
@surcharger.register(int)
def _(a, b):
    @singledispatch
    def interne(arg_b):
        return f"Défaut: int et {type(arg_b).__name__}"
    
    @interne.register(int)
    def _(arg_b):
        return f"Résultat: {a} (int) + {arg_b} (int) = {a + arg_b}"
    
    @interne.register(str)
    def _(arg_b):
        return f"Résultat: {arg_b} répété {a} fois"

    @interne.register(float)
    def _(arg_b):
        return f"Résultat: Division {a} / {arg_b} = {a / arg_b}"

    return interne(b)

# --- Cas où le PREMIER argument est un STR ---
@surcharger.register(str)
def _(a, b):
    @singledispatch
    def interne(arg_b):
        return f"Défaut: str et {type(arg_b).__name__}"
    
    @interne.register(int)
    def _(arg_b):
        return f"Résultat: {a} concaténé avec {arg_b}"
    
    @interne.register(str)
    def _(arg_b):
        return f"Résultat: Deux chaînes -> {a} & {arg_b}"

    return interne(b)

# --- Cas où le PREMIER argument est un FLOAT ---
@surcharger.register(float)
def _(a, b):
    @singledispatch
    def interne(arg_b):
        return f"Défaut: float et {type(arg_b).__name__}"
    
    @interne.register(int)
    def _(arg_b):
        return f"Résultat: Multiplication float*int = {a * arg_b}"
    
    @interne.register(float)
    def _(arg_b):
        return f"Résultat: Puissance float**float = {a ** arg_b}"

    return interne(b)

# --- Tests ---
print(surcharger(5, 10))        # int, int
print(surcharger(3, "Lo"))      # int, str
print(surcharger("Item", 1))    # str, int
print(surcharger("A", "B"))     # str, str
print(surcharger(2.5, 4))       # float, int
print(surcharger(10, 2.5))      # int, float
print(surcharger(2.0, 3.0))     # float, float

exit()
from multipledispatch import dispatch


# 1. Type int et int
@dispatch(int, int)
def calculer(a, b):
    return f"Addition d'entiers : {a + b}"

# 2. Type int et str
@dispatch(int, str)
def calculer(a, b):
    return f"Répétition : {b * a}"

# 3. Type str et int
@dispatch(str, int)
def calculer(a, b):
    return f"Concaténation forcée : {a}{b}"

# 4. Type str et str
@dispatch(str, str)
def calculer(a, b):
    return f"Fusion de chaînes : {a} - {b}"

# 5. Type float et int
@dispatch(float, int)
def calculer(a, b):
    return f"Produit mixte (float/int) : {a * b}"

# 6. Type int et float
@dispatch(int, float)
def calculer(a, b):
    return f"Division mixte (int/float) : {a / b}"

# 7. Type float et float
@dispatch(float, float)
def calculer(a, b):
    return f"Puissance de flottants : {a ** b}"

# --- Tests ---
print(calculer(10, 5))       # int, int
print(calculer(3, "Lo"))     # int, str
print(calculer("Code", 1))   # str, int
print(calculer("A", "B"))    # str, str
print(calculer(2.5, 4))      # float, int
print(calculer(10, 2.0))     # int, float
print(calculer(2.0, 3.0))    # float, float
