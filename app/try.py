class Parent:
    def __init__(self, name):
        self.name = name
        return


class Child(Parent):
    def child_method(self):
        print('child')

c = Child("my name")
c.child_method()
p = Parent("I am parent")
p.child_method(d)
