# --coding:utf-8--
class TheThing(object):

    def __init__(self):
        self.number = 0;

    def some_function(self):
        print("I got called.")

    def add_me_up(self, more):
        self.number += more
        return self.number


# two different things
a = TheThing()
a.some_function()
print(a.add_me_up(20))
print(a.add_me_up(20))
print(a.number)

b = TheThing()
b.some_function()
print(b.add_me_up(30))
print(b.add_me_up(30))
print(b.number)

