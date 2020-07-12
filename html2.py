def type_balise(tbalise):
    def text_balise(text):
        return f"<{tbalise}>{text}</{tbalise}>"
        
    return text_balise

print(type_balise("h2")("test"))


class MonIterateur(object):
    def __init__(self, obj):
        self.obj = obj
        self.length = len(obj)
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.length:
            raise StopIteration

        else:
            result = self.obj[self.count]

        self.count += 1
        return result


try:
    for lettre in MonIterateur("hello_world"):
        print(lettre, end=",")
    print()
    
except StopIteration:
    print("fin d'iteration")
