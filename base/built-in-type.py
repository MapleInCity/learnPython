# -*- coding:utf-8 -*-

# 按照用途不同，Python 内置类型可分为 "数据" 和 "程序" 两大类。
# 数据类型：
# 空值: None
# 数字: bool, int, long, float, complex
# 序列: str, unicode, list, tuple
# 字典: dict
# 集合: set, frozenset

# 数字
# bool

# None、0、空字符串、以及没有元素的容器对象都可视为 False，反之为 True。

# print map(bool, [None, 0, "", u"", list(), tuple(), dict(), set(), frozenset()])
# [False, False, False, False, False, False, False, False, False]
# 虽然有点古怪，但 True、False 的确可以当数字使用。

# print int(True)
# 1
# >>> int(False)
# 0
# >>> range(10)[True]
# 1

# >>> x = 5
# >>> range(10)[x > 3]
# 1
# int

# 在 64 位平台上，int 类型是 64 位整数 (sys.maxint)，这显然能应对绝大多数情况。整数是虚拟机特殊照顾对象：

# 从堆上按需申请名为 PyIntBlock 的缓存区域存储整数对象。
# 使用固定数组缓存 [-5, 257) 之间的小数字，只需计算下标就能获得指针。
# PyIntBlock 内存不会返还给操作系统，直至进程结束。
# 看看 "小数字" 和 "大数字" 的区别：

# >>> a = 15
# >>> b = 15

# >>> a is b
# True

# >>> sys.getrefcount(a)
# 47

# >>> a = 257
# >>> b = 257

# >>> a is b
# False

# >>> sys.getrefcount(a)
# 2
# 因 PyIntBlock 内存只复用不回收，同时持有大量整数对象将导致内存暴涨，且不会在这些对象被回收后释放内存，造成事实上的内存泄露。

# 用 range 创建一个巨大的数字列表，这就需要足够多的 PyIntBlock 为数字对象提供存储空间。
# 但换成 xrange 就不同了，每次迭代后，数字对象被回收，其占用内存空闲出来并被复用，内存也就不会暴涨了。

# 运行下面测试代码前，必须先安装 psutil 包，用来获取内存统计数据。

# $ sudo easy_install -U psutil
# $ cat test.py
# #/usr/bin/env python

# import gc, os, psutil

# def test():
#     x = 0
#     for i in range(10000000): # xrange
#         x += i

#     return x

# def main():
#     print test()
#     gc.collect()

#     p = psutil.Process(os.getpid())
#     print p.get_memory_info()

# if __name__ == "__main__":
#     main()
# 对比 range 和 xrange 所需的 RSS 值。

# range: meminfo(rss=93339648L, vms=2583552000L) # 89 MB
# xrange: meminfo(rss=8638464L, vms=2499342336L) # 8 MB
# 在实际开发中，很少会遇到这样的情形。就算是海量整数去重、排序，我们也可用位图等算法来节约内存使用。
# Python 3 已经用 xrange 替换掉了默认的 range，我们使用 2.x 时稍微注意一下即可。

# long

# 当超出 int 限制时， 会自动转换成 long。 作为变长对象，只要有内存足够，足以存储无法想象的天文数字。

# >>> a = sys.maxint
# >>> type(a)
# <type 'int'>

# >>> b = a + 1   # 超出，自动使用 long 类型。
# >>> type(b)
# <type 'long'>

# >>> 1 << 3000
# 12302319221611....890612250135171889174899079911291512399773872178519018229989376L

# >>> sys.getsizeof(1 << 0xFFFFFFFF)
# 572662332
# 使用 long 的机会不多，Python 也就没有必要专门为其设计优化策略。

# float

# 使用双精度浮点数 (float)，不能 "精确" 表示某些十进制的小数值。尤其是 "四舍五入 (round)" 的结果，可能和预想不同。

# >>> 3 / 2   # 除法默认返回整数，在 Python 3 中返回浮点数。
# 1

# >>> float(3) / 2
# 1.5

# >>> 3 * 0.1 == 0.3  # 这个容易导致莫名其妙的错误。
# False

# >>> round(2.675, 2) # 并没有想象中的四舍五入。
# 2.67
# 如果需要，可用 Decimal 代替，它能精确控制运算精度、有效数位和 round 的结果。

# >>> from decimal import Decimal, ROUND_UP, ROUND_DOWN

# >>> float('0.1') * 3 == float('0.3')     # float 转型精度不同
# False

# >>> Decimal('0.1') * 3 == Decimal('0.3')    # decimal 没有问题
# True

# >>> Decimal('2.675').quantize(Decimal('.01'), ROUND_UP)  # 精确控制 round
# Decimal('2.68')

# >>> Decimal('2.675').quantize(Decimal('.01'), ROUND_DOWN)
# Decimal('2.67')
# 在内存管理上，float 也采用 PyFloatBlock 模式，但没有特殊的 "小浮点数"。

# 字符串
# 与字符串相关的问题总是很多，比如池化 (intern)、编码 (encode) 等。字符串是不可变类型，保存字符序列或二进制数据。

# 短字符串存储在 arena 区域， str、unicode 单字符会被永久缓存。
# str 没有缓存机制，unicode 则保留 1024 个宽字符长度小于 9 的复用对象。
# 内部包含 hash 值，str 另有标记用来判断是否被池化。
# 字符串常量定义简单自由，可以是单引号、双引号或三引号。但我个人建议用双引号表示字符串，用单引号表示字符，和其他语言习惯保持一致。

# >>> "It's a book."    # 双引号里面可以用单引号。
# "It's a book."

# >>> 'It\'s a book.'   # 转义
# "It's a book."

# >>> '{"name":"Tom"}'   # 单引号里面正常使用双引号。
# '{"name":"Tom"}'

# >>> """     # 多行
# ... line 1
# ... line 2
# ... """

# >>> r"abc\x"    # r 前缀定义非转义的 raw-string。
# 'abc\\x'

# >>> "a" "b" "c"    # 自动合并多个相邻字符串。
# 'abc'

# >>> "中国人"     # UTF-8 字符串 (Linux 系统默认)。
# '\xe4\xb8\xad\xe5\x9b\xbd\xe4\xba\xba'

# >>> type(s), len(s)
# <type 'str'>, 9

# >>> u"中国人"    # 使用 u 前缀定义 UNICODE 字符串。
# u'\u4e2d\u56fd\u4eba'

# >>> type(u), len(u)
# <type 'unicode'>, 3
# 基本操作：

# >>> "a" + "b"
# 'ab'

# >>> "a" * 3
# 'aaa'

# >>> ",".join(["a", "b", "c"])     # 合并多个字符串。
# 'a,b,c'

# >>> "a,b,c".split(",")      # 按指定字符分割。
# ['a', 'b', 'c']

# >>> "a\nb\r\nc".splitlines()     # 按行分割。
# ['a', 'b', 'c']

# >>> "a\nb\r\nc".splitlines(True)    # 分割后，保留换行符。
# ['a\n', 'b\r\n', 'c']

# >>> "abc".startswith("ab"), "abc".endswith("bc")  # 判断是否以特定子串开始或结束。
# True, True

# >>> "abc".upper(), "Abc".lower()    # 大小写转换。
# 'ABC', 'abc'

# >>> "abcabc".find("bc"), "abcabc".find("bc", 2)  # 可指定查找起始结束位置。
# 1, 4

# >>> " abc".lstrip(), "abc ".rstrip(), " abc ".strip() # 剔除前后空格。
# 'abc', 'abc', 'abc'

# >>> "abc".strip("ac")      # 可删除指定的前后缀字符。
# 'b'

# >>> "abcabc".replace("bc", "BC")    # 可指定替换次数。
# 'aBCaBC'

# >>> "a\tbc".expandtabs(4)     # 将 tab 替换成空格。
# 'a bc'

# >>> "123".ljust(5, '0'), "456".rjust(5, '0'), "abc".center(10, '*') # 填充
# '12300', '00456', '***abc****'

# >>> "123".zfill(6), "123456".zfill(4)      # 数字填充
# '000123', '123456'
# 编码

# Python 2.x 默认采用 ASCII 编码。为了完成编码转换，必须和操作系统字符编码统一起来。

# >>> import sys, locale

# >>> sys.getdefaultencoding()  # Python 默认编码。
# 'ascii'

# >>> c = locale.getdefaultlocale(); c # 获取当前系统编码。
# ('zh_CN', 'UTF-8')

# >>> reload(sys)    # setdefaultencoding 在被初始化时被 site.py 删掉了。
# <module 'sys' (built-in)>

# >>> sys.setdefaultencoding(c[1]) # 重新设置默认编码。
# str、unicode 都提供了 encode 和 decode 编码转换方法。

# encode: 将默认编码转换为其他编码。
# decode: 将默认或者指定编码字符串转换为 unicode。
# >>> s = "中国人"; s
# '\xe4\xb8\xad\xe5\x9b\xbd\xe4\xba\xba'

# >>> u = s.decode(); u   # UTF-8 -> UNICODE
# u'\u4e2d\u56fd\u4eba'

# >>> gb = s.encode("gb2312"); gb  # UTF-8 -> GB2312
# '\xd6\xd0\xb9\xfa\xc8\xcb'

# >>> gb.encode("utf-8")   # encode 会把 gb 当做默认 UTF-8 编码，所以出错。
# UnicodeDecodeError: 'utf8' codec can't decode byte 0xd6 in position 0: invalid
# continuation byte

# >>> gb.decode("gb2312")   # 可以将其转换成 UNICODE。
# u'\u4e2d\u56fd\u4eba'

# >>> gb.decode("gb2312").encode() # 然后再转换成 UTF-8
# '\xe4\xb8\xad\xe5\x9b\xbd\xe4\xba\xba'

# >>> unicode(gb, "gb2312")  # GB2312 -> UNICODE
# u'\u4e2d\u56fd\u4eba'
# >>> u.encode()    # UNICODE -> UTF-8
# '\xe4\xb8\xad\xe5\x9b\xbd\xe4\xba\xba'

# >>> u.encode("gb2312")   # UNICODE -> GB2312
# '\xd6\xd0\xb9\xfa\xc8\xcb'
# 标准库另有 codecs 模块用来处理更复杂的编码转换，比如大小端和 BOM。

# >>> from codecs import BOM_UTF32_LE

# >>> s = "中国人"
# >>> s
# '\xe4\xb8\xad\xe5\x9b\xbd\xe4\xba\xba'

# >>> s.encode("utf-32")
# '\xff\xfe\x00\x00-N\x00\x00\xfdV\x00\x00\xbaN\x00\x00'

# >>> BOM_UTF32_LE
# '\xff\xfe\x00\x00'

# >>> s.encode("utf-32").decode("utf-32")
# u'\u4e2d\u56fd\u4eba'
# 格式化

# Python 提供了两种字符串格式化方法，除了熟悉的 C 样式外，还有更强大的 format。

# %[(key)][flags][width][.precision]typecode
# 标记：- 左对齐，+ 数字符号，# 进制前缀，或者用空格、0 填充。

# >>> "%(key)s=%(value)d" % dict(key = "a", value = 10)  # key
# 'a=10'

# >>> "[%-10s]" % "a"      # 左对齐
# '[a ]'

# >>> "%+d, %+d" % (-10, 10)     # 数字符号
# '-10, +10'

# >>> "%010d" % 3       # 填充
# '0000000003'

# >>> "%.2f" % 0.1234      # 小数位
# '0.12'

# >>> "%#x, %#X" % (100, 200)     # 十六进制、前缀、大小写。
# '0x64, 0XC8'

# >>> "%s, %r" % (m, m)      # s: str(); r: repr()
# 'test..., <__main__.M object at 0x103c4aa10>'
# format 方法支持更多的数据类型，包括列表、字典、对象成员等。

# {fieldconvertflag:formatspec}
# 格式化规范：

# formatspec: [[fill]align][sign][#][0][width][.precision][typecode]
# 示例：

# >>> "{key}={value}".format(key="a", value=10) # 使用命名参数。
# 'a=10'

# >>> "{0},{1},{0}".format(1, 2)    # field 可多次使用。
# '1,2,1'

# >>> "{0:,}".format(1234567)    # 千分位符号
# '1,234,567'

# >>> "{0:,.2f}".format(12345.6789)   # 千分位，带小数位。
# '12,345.68'

# >>> "[{0:<10}], [{0:^10}], [{0:*>10}]".format("a") # 左中右对齐，可指定填充字符。
# '[a ], [ a ], [*********a]'

# >>> import sys

# >>> "{0.platform}".format(sys)    # 成员
# 'darwin'

# >>> "{0[a]}".format(dict(a=10, b=20))   # 字典
# '10'

# >>> "{0[5]}".format(range(10))    # 列表
# '5'
# 另有 string.Template 模板可供使用。该模块还定义了各种常见的字符序列。

# >>> from string import letters, digits, Template

# >>> letters         # 字母表
# 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# >>> digits         # 数字表
# '0123456789'

# >>> Template("$name, $age").substitute(name = "User1", age = 20) # 模板替换。
# 'User1, 20'

# >>> Template("${name}, $age").safe_substitute(name = "User1")  # 没找到值，不会抛出异常。
# 'User1, $age'
# 池化

# 在 Python 进程中，无数的对象拥有一堆类似 "name"、"doc" 这样的名字，池化有助于减少对象数量和内存消耗， 提升性能。

# 用 intern() 函数可以把运行期动态生成的字符串池化。

# >>> s = "".join(["a", "b", "c"])

# >>> s is "abc"   # 显然动态生成的字符串 s 没有被池化。
# False

# >>> intern(s) is "abc"  # intern 会检查内部标记。
# True

# >>> intern(s) is intern(s) # 以后用 intern 从池中获取字符串对象，就可以复用了。
# True
# 当池化的字符串不再有引用时，将被回收。

# 列表
# 从功能上看，列表 (list) 类似 Vector，而非数组或链表。

# 列表对象和存储元素指针的数组是分开的两块内存，后者在堆上分配。
# 虚拟机会保留 80 个列表复用对象，但其元素指针数组会被释放。
# 列表会动态调整指针数组大小，预分配内存多于实际元素数量。
# 创建列表：

# >>> []       # 空列表。
# []

# >>> ['a', 'b'] * 3      # 这个少见吧。
# ['a', 'b', 'a', 'b', 'a', 'b']

# >>> ['a', 'b'] + ['c', 'd']    # 连接多个列表。
# ['a', 'b', 'c', 'd']

# >>> list("abcd")      # 将序列类型或迭代器转换为列表。
# ['a', 'b', 'c', 'd']

# >>> [x for x in range(3)]    # 生成器表达式。
# [0, 1, 2]
# 常见操作：

# >>> l = list("abc")
# >>> l[1] = 2      # 按序号读写。
# >>> l
# ['a', 2, 'c']

# >>> l = list(xrange(10))
# >>> l[2:-2]       # 切片。
# [2, 3, 4, 5, 6, 7]

# >>> l = list("abcabc")
# >>> l.count("b")      # 统计元素项。
# 2

# >>> l = list("abcabc")
# >>> l.index("a", 2)     # 从指定位置查找项，返回序号。
# 3

# >>> l = list("abc")
# >>> l.append("d")
# >>> l        # 追加元素。
# ['a', 'b', 'c', 'd']

# >>> l = list("abc")
# >>> l.insert(1, 100)     # 在指定位置插入元素。
# >>> l
# ['a', 100, 'b', 'c']

# >>> l = list("abc")
# >>> l.extend(range(3))     # 合并列表。
# >>> l
# ['a', 'b', 'c', 0, 1, 2]

# >>> l = list("abcabc")
# >>> l.remove("b")      # 移除第一个指定元素。
# >>> l
# ['a', 'c', 'a', 'b', 'c']

# >>> l = list("abc")
# >>> l.pop(1)      # 弹出指定位置的元素 (默认最后项)。
# 'b'
# >>> l
# ['a', 'c']
# 可用 bisect 向有序列表中插入元素。

# >>> import bisect

# >>> l = ["a", "d", "c", "e"]
# >>> l.sort()
# >>> l
# ['a', 'c', 'd', 'e']

# >>> bisect.insort(l, "b")
# >>> l
# ['a', 'b', 'c', 'd', 'e']

# >>> bisect.insort(l, "d")
# >>> l
# ['a', 'b', 'c', 'd', 'd', 'e']
# 性能

# 列表用 realloc() 调整指针数组内存大小，可能需要复制数据。插入和删除操作，还会循环移动后续元素。这些都是潜在的性能隐患。对于频繁增删元素的大型列表，应该考虑用链表等数据结构代替。

# 下面的例子测试了两种创建列表对象方式的性能差异。为获得更好测试结果，我们关掉 GC，元素使用同一个小整数对象，减少其他干扰因素。

# >>> import itertools, gc

# >>> gc.disable()

# >>> def test(n):
# ...     return len([0 for i in xrange(n)])  # 先创建列表，然后 append。

# >>> def test2(n):
# ...     return len(list(itertools.repeat(0, n))) # 按照迭代器创建列表对象，一次分配内存。

# >>> timeit test(10000)
# 1000 loops, best of 3: 810 us per loop

# >>> timeit test2(10000)
# 10000 loops, best of 3: 89.5 us per loop
# 从测试结果来看，性能差异非常大。

# 某些时候，可以考虑用数组代替列表。 和列表存储对象指针不同，数组直接内嵌数据，既省了创建对象的内存开销，又提升了读写效率。

# >>> import array

# >>> a = array.array("l", range(10))  # 用其他序列类型初始化数组。
# >>> a
# array('l', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# >>> a.tolist()     # 转换为列表。
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# >>> a = array.array("c")    # 创建特定类型数组。

# >>> a.fromstring("abc")    # 从字符串添加元素。
# >>> a
# array('c', 'abc')

# >>> a.fromlist(list("def"))   # 从列表添加元素。
# >>> a
# array('c', 'abcdef')

# >>> a.extend(array.array("c", "xyz"))  # 合并列表或数组。
# >>> a
# array('c', 'abcdefxyz')
# 元组
# 元组 (tuple) 看上去像列表的只读版本，但在底层实现上有很多不同之处。

# 只读对象，元组和元素指针数组内存是一次性连续分配的。
# 虚拟机缓存 n 个元素数量小于 20 的元组复用对象。
# 在编码中，应该尽可能用元组代替列表。除内存复用更高效外，其只读特征更利于并行开发。

# 基本操作：

# >>> a = (4)     # 少了逗号，就成了普通的括号运算符了。
# >>> type(a)
# <type 'int'>

# >>> a = (4,)    # 这才是元组。
# >>> type(a)
# <type 'tuple'>

# >>> s = tuple("abcadef")   # 将其他序列类型转换成元组。
# >>> s
# ('a', 'b', 'c', 'a', 'd', 'e', 'f')

# >>> s.count("a")    # 元素统计。
# 2

# >>> s.index("d")    # 查找元素，返回序号。
# 4
# 标准库另提供了特别的 namedtuple，可用名字访问元素项。

# >>> from collections import namedtuple

# >>> User = namedtuple("User", "name age") # 空格分隔字段名，或使用迭代器。

# >>> u = User("user1", 10)
# >>> u.name, u.age
# ('user1', 10)
# 其实 namedtuple 并不是元组，而是利用模板动态创建的自定义类型。

# 字典
# 字典 (dict) 采用开放地址法的哈希表实现。

# 自带元素容量为 8 的 smalltable，只有 "超出" 时才到堆上额外分配元素表内存。
# 虚拟机缓存 80 个字典复用对象，但在堆上分配的元素表内存会被释放。
# 按需动态调整容量。扩容或收缩操作都将重新分配内存，重新哈希。
# 删除元素操作不会立即收缩内存。
# 创建字典：

# >>> {}      # 空字典
# {}

# >>> {"a":1, "b":2}     # 普通构造方式
# {'a': 1, 'b': 2}

# >>> dict(a = 1, b = 2)    # 构造
# {'a': 1, 'b': 2}

# >>> dict((["a", 1], ["b", 2]))   # 用两个序列类型构造字典。
# {'a': 1, 'b': 2}

# >>> dict(zip("ab", range(2)))   # 同上
# {'a': 0, 'b': 1}

# >>> dict(map(None, "abc", range(2)))  # 同上
# {'a': 0, 'c': None, 'b': 1}

# >>> dict.fromkeys("abc", 1)   # 用序列做 key，并提供默认 value。
# {'a': 1, 'c': 1, 'b': 1}

# >>> {k:v for k, v in zip("abc", range(3))} # 使用生成表达式构造字典。
# {'a': 0, 'c': 2, 'b': 1}
# 基本操作：

# >>> d = {"a":1, "b":2}
# >>> "b" in d     # 判断是否包含 key。
# True

# >>> d = {"a":1, "b":2}
# >>> del d["b"]     # 删除 k/v。
# >>> d
# {'a': 1}

# >>> d = {"a":1}
# >>> d.update({"c": 3})    # 合并 dict。
# >>> d
# {'a': 1, 'c': 3}

# >>> d = {"a":1, "b":2}
# >>> d.pop("b")     # 弹出 value。
# >>> d
# (2, {'a': 1})

# >>> d = {"a":1, "b":2}
# >>> d.popitem()     # 弹出 (key, value)。
# ('a', 1)
# 默认返回值：

# >>> d = {"a":1, "b":2}

# >>> d.get("c")     # 如果没有对应 key，返回 None。
# None

# >>> d.get("d", 123)    # 如果没有对应 key，返回缺省值。
# 123

# >>> d.setdefault("a", 100)   # key 存在，直接返回 value。
# 1

# >>> d.setdefault("c", 200)    # key 不存在，先设置，后返回。
# 200

# >>> d
# {'a': 1, 'c': 200, 'b': 2}
# 迭代器操作：

# >>> d = {"a":1, "b":2}

# >>> d.keys()
# ['a', 'b']

# >>> d.values()
# [1, 2]

# >>> d.items()
# [('a', 1), ('b', 2)]

# >>> for k in d: print k, d[k]
# a 1
# b 2

# >>> for k, v in d.items(): print k, v
# a 1
# b 2
# 对于大字典，调用 keys()、values()、items() 会构造同样巨大的列表。建议用迭代器替代，以减少内存开销。

# >>> d = {"a":1, "b":2}

# >>> d.iterkeys()
# <dictionary-keyiterator object at 0x10de82cb0>

# >>> d.itervalues()
# <dictionary-valueiterator object at 0x10de82d08>

# >>> d.iteritems()
# <dictionary-itemiterator object at 0x10de82d60>

# >>> for k, v in d.iteritems():
# ... print k, v
# a 1
# b 2
# 视图

# 要判断两个字典间的差异，使用视图是最简便的做法。

# >>> d1 = dict(a = 1, b = 2)
# >>> d2 = dict(b = 2, c = 3)

# >>> d1 & d2     # 字典不支持该操作。
# TypeError: unsupported operand type(s) for &: 'dict' and 'dict'

# >>> v1 = d1.viewitems()
# >>> v2 = d2.viewitems()

# >>> v1 & v2     # 交集
# set([('b', 2)])

# >>> v1 | v2     # 并集
# set([('a', 1), ('b', 2), ('c', 3)])

# >>> v1 - v2     # 差集 (仅 v1 有，v2 没有的)
# set([('a', 1)])

# >>> v1 ^ v2     # 对称差集 (不会同时出现在 v1 和 v2 中)
# set([('a', 1), ('c', 3)])

# >>> ('a', 1) in v1    # 判断
# True
# 视图让某些操作变得更加简便，比如在不引入新数据项的情况下更新字典内容。

# >>> a = dict(x=1)
# >>> b = dict(x=10, y=20)
# >>> a.update({k:b[k] for k in a.viewkeys() & b.viewkeys()})
# >>> a
# {'x': 10}
# 视图会和字典同步变更。

# >>> d = {"a": 1}
# >>> v = d.viewitems()
# >>> v
# dict_items([('a', 1)])

# >>> d["b"] = 2
# >>> v
# dict_items([('a', 1), ('b', 2)])

# >>> del d["a"]
# >>> v
# dict_items([('b', 2)])
# 扩展

# 当访问的 key 不存在时， defaultdict 自动调用 factory 对象创建所需键值对。factory 可以是任何无参数函数或 callable 对象。

# >>> from collections import defaultdict

# >>> d = defaultdict(list)

# >>> d["a"].append(1) # key "a" 不存在，直接用 list() 函数创建一个空列表作为 value。
# >>> d["a"].append(2)
# >>> d["a"]
# [1, 2]
# 字典是哈希表，默认迭代是无序的。如果希望按照元素添加顺序输出结果，可以用 OrderedDict。

# >>> from collections import OrderedDict

# >>> d = dict()
# >>> d["a"] = 1
# >>> d["b"] = 2
# >>> d["c"] = 3

# >>> for k, v in d.items(): print k, v  # 并非按添加顺序输出。
# a 1
# c 3
# b 2

# >>> od = OrderedDict()
# >>> od["a"] = 1
# >>> od["b"] = 2
# >>> od["c"] = 3

# >>> for k, v in od.items(): print k, v  # 按添加顺序输出。
# a 1
# b 2
# c 3

# >>> od.popitem()     # 按 LIFO 顺序弹出。
# ('c', 3)
# >>> od.popitem()
# ('b', 2)
# >>> od.popitem()
# ('a', 1)
# 集合
# 集合 (set) 用来存储无序不重复对象。所谓不重复对象，除了不是同一对象外，还包括 "值" 不能相同。集合只能存储可哈希对象，一样有只读版本 frozenset。

# 判重公式：(a is b) or (hash(a) == hash(b) and eq(a, b))
# 在内部实现上，集合和字典非常相似，除了 Entry 没有 value 字段。集合不是序列类型，不能像列表那样按序号访问，也不能做切片操作。

# >>> s = set("abc")     # 通过序列类型初始化。
# >>> s
# set(['a', 'c', 'b'])

# >>> {v for v in "abc"}    # 通过构造表达式创建。
# set(['a', 'c', 'b'])

# >>> "b" in s     # 判断元素是否在集合中。
# True

# >>> s.add("d")     # 添加元素
# >>> s
# set(['a', 'c', 'b', 'd'])

# >>> s.remove("b")     # 移除元素
# >>> s
# set(['a', 'c', 'd'])

# >>> s.discard("a")     # 如果存在，就移除。
# >>> s
# set(['c', 'd'])

# >>> s.update(set("abcd"))   # 合并集合
# >>> s
# set(['a', 'c', 'b', 'd'])

# >>> s.pop()      # 弹出元素
# 'a'
# >>> s
# set(['c', 'b', 'd'])
# 集合和字典、列表最大的不同除了元素不重复外，还支持集合运算。

# >>> "c" in set("abcd")    # 判断集合中是否有特定元素。
# True

# >>> set("abc") is set("abc")
# False

# >>> set("abc") == set("abc")   # 相等判断
# True

# >>> set("abc") = set("abc")   # 不等判断
# False

# >>> set("abcd") >= set("ab")   # 超集判断 (issuperset)
# True

# >>> set("bc") < set("abcd")   # 子集判断 (issubset)
# True

# >>> set("abcd") | set("cdef")   # 并集 (union)
# set(['a', 'c', 'b', 'e', 'd', 'f'])

# >>> set("abcd") & set("abx")   # 交集 (intersection)
# set(['a', 'b'])

# >>> set("abcd") - set("ab")   # 差集 (difference)， 仅左边有，右边没有的。
# set(['c', 'd'])

# >>> set("abx") ^ set("aby")   # 对称差集 (symmetric_difference)
# set(['y', 'x'])     # 不会同时出现在两个集合当中的元素。

# >>> set("abcd").isdisjoint("ab")  # 判断是否没有交集
# False
# 更新操作：

# >>> s = set("abcd")
# >>> s |= set("cdef")    # 并集 (update)
# >>> s
# set(['a', 'c', 'b', 'e', 'd', 'f'])

# >>> s = set("abcd")
# >>> s &= set("cdef")    # 交集 (intersection_update)
# >>> s
# set(['c', 'd'])

# >>> s = set("abx")
# >>> s -= set("abcdy")    # 差集 (difference_update)
# >>> s
# set(['x'])

# >>> s = set("abx")
# >>> s ^= set("aby")    # 对称差集 (symmetric_difference_update)
# >>> s
# set(['y', 'x'])
# 集合和字典主键都必须是可哈希类型对象，但常用的 list、dict、set、defaultdict、OrderedDict 都是不可哈希的，仅有 tuple、frozenset 可用。

# >>> hash([])
# TypeError: unhashable type: 'list'

# >>> hash({})
# TypeError: unhashable type: 'dict'

# >>> hash(set())
# TypeError: unhashable type: 'set'

# >>> hash(tuple()), hash(frozenset())
# (3527539, 133156838395276)
# 如果想把自定义类型放入集合，需要保证 hash 和 equal 的结果都相同才能去重。

# >>> class User(object):
# ...     def __init__(self, name):
# ...         self.name = name

# >>> hash(User("tom")) # 每次的哈希结果都不同
# 279218517

# >>> hash(User("tom"))
# 279218521

# >>> class User(object):
# ...     def __init__(self, name):
# ...         self.name = name
# ...
# ...     def __hash__(self):
# ...         return hash(self.name)
# ...
# ...     def __eq__(self, o):
# ...         if not o or not isinstance(o, User): return False
# ...         return self.name == o.name

# >>> s = set()

# >>> s.add(User("tom"))
# >>> s.add(User("tom"))

# >>> s
# set([<__main__.User object at 0x10a48d150>])
# 数据结构很重要，这几个内置类型并不足以完成全部工作。像 C、数据结构、常用算法这类基础是每个程序开发人员都应该掌握的。
