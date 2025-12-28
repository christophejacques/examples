class Keyboard:
    buffer: list = []

    @classmethod
    def __init__(cls):
        cls.buffer = []
        print("Keyboard initialized")

    @classmethod
    def add_key_to_buffer(cls, key):
        cls.buffer.append(key)

    @classmethod
    def clear_buffer(cls):
        cls.buffer.clear()

    @classmethod
    def view_next_key(cls):
        if cls.keypressed():
            return cls.buffer[0]
        else:
            return None

    @classmethod
    def view_last_key(cls):
        if cls.keypressed():
            return cls.buffer[-1]
        else:
            return None

    @classmethod
    def keypressed(cls) -> bool:
        return len(cls.buffer) > 0

    @classmethod
    def get_key(cls):
        if cls.keypressed():
            return cls.buffer.pop(0)
        else:
            return None


if __name__ == "__main__":
    print("Compilation: OK")
