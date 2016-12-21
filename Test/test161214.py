# !usr/bin/env python
# coding:utf-8
import pickle
try:
    with open("./test3.txt", 'wb') as mySaveData:
        pickle.dump(["鹅鹅鹅，曲项向天歌。", "白毛浮绿水，红掌拨青波。"], mySaveData)

    with open("./test3.txt", "rb") as myReadData:
        data = pickle.load(myReadData)
        for each_Item in data:
            print each_Item
except IOError as err:
    print "IOError: " + err
except pickle.PickleError as perr:
    print "Pickle Error: " + str(perr)
finally:
    pass
