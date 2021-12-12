class Parent:
    def __init__(self):
        self.config = {'Item1': 86, 'Item2': 97}

    def get_config(self):
        print(self.config)


class Child:
    def __init__(self, source: Parent):
        self.source = source
        self.config = source.config

    def get_config(self):
        print(self.config)

    def change_config(self, key, value):
        self.config[key] = value


parent_1 = Parent()
child_1 = Child(parent_1)
parent_1.get_config()

child_1.change_config('Item1', 34)
child_1.get_config()
parent_1.get_config()
