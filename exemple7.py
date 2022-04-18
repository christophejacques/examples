class ClassName:
    """docstring for ClassName"""

    def __init__(self, arg):
        self.arg = arg
        
    def ma_fonction(self, p):
        pass


def main():
    try:
        c = ClassName(1)
        print(c.__doc__)
    
    except Exception as error:
        print(error)
    
    else:
        print("pas d'erreur")


try:
    if __name__ == '__main__':
        main()

except Exception as e:
    print("Error:", e)
