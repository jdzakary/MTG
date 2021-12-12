class Parent1:
    def __init__(self, age):
        self.age = age

    def get_age(self):
        print(self.age)


class Parent2:
    def __init__(self, sex):
        self.sex = sex

    def get_sex(self):
        print(self.sex)

    def greeting(self):
        self.name = 'Davis'
        print('Hello!')


class ChildA(Parent1, Parent2):
    def __init__(self, age, sex):
        Parent1.__init__(self, age)
        Parent2.__init__(self, sex)

    def get_name(self):
        print(self.name)


child = ChildA(age=46, sex='Female')
child.get_age()
child.get_sex()
child.greeting()
child.get_name()
