from time import sleep


def retry(retries=3):
    left = {'retries': retries}

    def decorator(f):
        def inner(*args, **kwargs):
            while left['retries']:
                try:
                    return f(*args, **kwargs)

                except Exception as ex:
                    left['retries'] -= 1
                    print(ex)
                    sleep(1)

            msg = f"Retried {retries} times unsuccessfully."
            print(msg)

        return inner
    return decorator


@retry()
def func(p1, p2):
    print(p1, p2, end=": ")
    a = 1 / 0
    print(a)
    

func(1, 2)
