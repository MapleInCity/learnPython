# !usr/bin/env python
# coding:utf-8

import pickle

try:
    allText = []
    with open("E:/gitHub/learnPython/Test/test.txt") as test:
        for each_item in test:
            print each_item
            allText.append(each_item)

    with open("E:/gitHub/learnPython/Test/test2.txt", 'wb') as mysavedata:
        pickle.dump(allText, mysavedata)

    with open("E:/gitHub/learnPython/Test/test2.txt", 'rb') as myloaddata:
        mylist = pickle.load(myloaddata)
        for each_item in mylist:
            print each_item

    with open("E:/gitHub/learnPython/Test/test3.txt", 'wb') as mysavedata2:
        for each_item in allText:
            mysavedata2.write(each_item)

    with open("E:/gitHub/learnPython/Test/test3.txt", 'rb') as myloaddata2:
        for each_item in myloaddata2:
            print each_item

except IOError as err:
    print "File error: " + str(err)

except pickle.PickleError as perr:
    print "Pickle Error: " + str(perr)

finally:
    pass
