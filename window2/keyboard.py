class Keyboard:
    buffer: list = []

    @classmethod
    def __init__(self):
        self.buffer = []
        print("Keyboard initialized")

    @classmethod
    def add_key_to_buffer(self, key):
        self.buffer.append(key)

    @classmethod
    def clear_buffer(self):
        self.buffer.clear()

    @classmethod
    def view_next_key(self):
        if self.keypressed():
            return self.buffer[0]
        else:
            return None

    @classmethod
    def view_last_key(self):
        if self.keypressed():
            return self.buffer[-1]
        else:
            return None

    @classmethod
    def keypressed(self) -> bool:
        return len(self.buffer) > 0

    @classmethod
    def get_key(self):
        if self.keypressed():
            return self.buffer.pop(0)
        else:
            return None


if __name__ == "__main__":
    print("Compilation: OK")
