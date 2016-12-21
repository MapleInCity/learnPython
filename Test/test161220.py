# !usr/bin/env Python
# coding:utf-8

class Foo:
    # 共有
    name = ''
    # 私有
    __age = ''

    def __init__(self, name, age=0):
        self.name = name
        self.__age = age

    def hi(self):
        print "name : " + str(self.name)
        print "age : " + str(self.__age)

if __name__ == "__main__":
    foo01 = Foo('letian')
    foo01.hi()
    print type(Foo)
    print type(foo01)
    print id(foo01)
    print id(Foo)
