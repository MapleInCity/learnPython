# -- coding:utf-8 --
animals = ['bear', 'python', 'peacock', 'kangaroo', 'whale', 'platypus']

def read_animal(animals, index):
    return "is at %d and is a %s" % (index, animals[index])

print("The animal at 1", read_animal(animals, 0))
print("The 3rd animal", read_animal(animals, 2))
print("The 1st animal", read_animal(animals, 0))
print("The animal at 3", read_animal(animals, 2))
print("The 5th animal", read_animal(animals, 4))
print("The animal at 2", read_animal(animals, 1))
print("The 6th animal", read_animal(animals, 5))
print("The animal at 4", read_animal(animals, 3))
