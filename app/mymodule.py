

class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def sum(self):
        return self.a + self.b

    def mul(self):
        return self.a * self.b

    def __repr__(self):
        return f'MyClass ({self.a}, {self.b})'


class MyClass2:
    def __init__(self):
        print("constructor")

    def __call__(self, *args, **kwargs):
        print("called")