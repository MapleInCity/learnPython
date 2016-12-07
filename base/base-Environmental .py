# -*- coding:utf-8 -*-
# 基本环境

# 虚拟机
# Python 是一种半编译半解释型运行环境。
# 首先，它会在模块 "载入" 时将源码编译成字节码 (Byte Code)。而后，这些字节码会被虚拟机在一个 "巨大" 的核心函数里解释执行。
# 这是导致 Python 性能较低的重要原因，好在现在有了内置 Just-in-time 二次编译器的 PyPy 可供选择。

# 当虚拟机开始运行时，它通过初始化函数完成整个运行环境设置：
#       创建解释器和主线程状态对象，这是整个进程的根对象。
#       初始化内置类型。数字、列表等类型都有专门的缓存策略需要处理。
#       创建 builtin 模块，该模块持有所有内置类型和函数。
#       创建 sys 模块，其中包含了 sys.path、modules 等重要的运行期信息。
#       初始化 import 机制。
#       初始化内置 Exception。
#       创建 main 模块，准备运行所需的名字空间。
#       通过 site.py 将 site-packages 中的第三方扩展库添加到搜索路径列表。
#       执行入口 py 文件。执行前会将 main.dict 作为名字空间传递进去。
#       程序执行结束。
#       执行清理操作，包括调用退出函数，GC 清理现场，释放所有模块等。
#       终止进程。

# Python 源码是个宝库，其中有大量的编程范式和技巧可供借鉴，尤其是对内存的管理分配。个人建议有 C 基础的兄弟，在闲暇时翻看一二。

# 类型和对象
# 先有类型 (Type)，而后才能生成实例 (Instance)。
# Python 中的一切都是对象，包括类型在内的每个对象都包含一个标准头，通过头部信息就可以明确知道其具体类型。

# 头信息由 "引用计数" 和 "类型指针" 组成，前者在对象被引用时增加，超出作用域或手工释放后减小，等于 0 时会被虚拟机回收
# (某些被缓存的对象计数器永远不会为 0)。

# 以 int 为例，对应 Python 结构定义是：

# #define PyObject_HEAD \
#     Py_ssize_t ob_refcnt; \
#     struct _typeobject *ob_type;

# typedef struct _object {
#     PyObject_HEAD
# } PyObject;

# typedef struct {
#     PyObject_HEAD  // 在 64 位版本中，头长度为 16 字节。
#     long ob_ival;  // long 是 8 字节。
# } PyIntObject;
# 可以用 sys 中的函数测试一下。

# >>> import sys

# >>> x = 0x1234  # 不要使用 [-5, 257) 之间的小数字，它们有专门的缓存机制。

# >>> sys.getsizeof(x) # 符合长度预期。
# 24

# >>> sys.getrefcount(x) # sys.getrefcount() 读取头部引用计数，注意形参也会增加一次引用。
# 2

# >>> y = x   # 引用计数增加。
# >>> sys.getrefcount(x)
# 3

# >>> del y   # 引用计数减小。
# >>> sys.getrefcount(x)
# 2

# 类型指针则指向具体的类型对象，其中包含了继承关系、静态成员等信息。
# 所有的内置类型对象都能从 types 模块中找到，至于 int、long、str 这些关键字可以看做是简短别名。

# >>> import types
# >>> x = 20
# >>> type(x) is types.IntType  # is 通过指针判断是否指向同一对象。
# True

# >>> x.__class__    # __class__ 通过类型指针来获取类型对象。
# <type 'int'>

# >>> x.__class__ is type(x) is int is types.IntType
# True

# >>> y = x

# >>> hex(id(x)), hex(id(y))  # id() 返回对象标识，其实就是内存地址。
# ('0x7fc5204103c0', '0x7fc5204103c0')
# >>> hex(id(int)), hex(id(types.IntType))
# ('0x1088cebd8', '0x1088cebd8')

# 除了 int 这样的固定长度类型外，还有 long、str 这类变长对象。其头部多出一个记录元素项数量的字段。
# 比如 str 的字节数量，list 列表的长度等等。

# #define PyObject_VAR_HEAD \
#     PyObject_HEAD \
#     Py_ssize_t ob_size;  /* Number of items in variable part */

# typedef struct {
#     PyObject_VAR_HEAD
# } PyVarObject;
# 有关类型和对象更多的信息，将在后续章节中详述。

# 名字空间
# 名字空间是 Python 最核心的内容。

# >>> x
# NameError: name 'x' is not defined
# 我们习惯于将 x 称为变量，但在这里，更准确的词语是 "名字"。
# 和 C 变量名是内存地址别名不同，Python 的名字实际上是一个字符串对象，它和所指向的目标对象一起在名字空间中构成一项 {name: object} 关联。

# Python 有多种名字空间，比如称为 globals 的模块名字空间，称为 locals 的函数堆栈帧名字空间，还有 class、instance 名字空间。
# 不同的名字空间决定了对象的作用域和生存周期。

# >>> x = 123

# >>> globals()   # 获取 module 名字空间。
# {'x': 123, ......}
# 可以看出，名字空间就是一个字典 (dict)。我们完全可以直接在名字空间添加项来创建名字。

# >>> globals()["y"] = "Hello, World"

# >>> y
# 'Hello, World'
# 在 Python 源码中，有这样一句话：Names have no type, but objects do.

# 名字的作用仅仅是在某个时刻与名字空间中的某个对象进行关联。其本身不包含目标对象的任何信息，只有通过对象头部的类型指针才能获知其具体类型，
# 进而查找其相关成员数据。正因为名字的弱类型特征，我们可以在运行期随时将其关联到任何类型对象。

# >>> y
# 'Hello, World'

# >>> type(y)
# <type 'str'>

# >>> y = __import__("string") # 将原本与字符串关联的名字指向模块对象。

# >>> type(y)
# <type 'module'>

# >>> y.digits   # 查看模块对象的成员。
# '0123456789'
# 在函数外部，locals() 和 globals() 作用完全相同。
# 而当在函数内部调用时，locals() 则是获取当前函数堆栈帧的名字空间，其中存储的是函数参数、局部变量等信息。

# >>> import sys

# >>> globals() is locals()
# True

# >>> locals()
# {
#     '__builtins__': <module '__builtin__' (built-in)>,
#     '__name__': '__main__',
#     'sys': <module 'sys' (built-in)>,
# }

# >>> def test(x):     # 请对比下面的输出内容。
# ... y = x + 100
# ... print locals()    # 可以看到 locals 名字空间中包含当前局部变量。
# ... print globals() is locals()  # 此时 locals 和 globals 指向不同名字空间。

# ... frame = sys._getframe(0)   # _getframe(0) 获取当前堆栈帧。
# ... print locals() is frame.f_locals # locals 名字空间实际就是当前堆栈帧的名字空间。
# ... print globals() is frame.f_globals # 通过 frame 我们也可以函数定义模块的名字空间。

# >>> test(123)
# {'y': 223, 'x': 123}
# False
# True
# True
# 在函数中调用 globals() 时，总是获取包含该函数定义的模块名字空间，而非调用处。

# >>> pycat test.py

# a = 1
# def test():
#     print {k:v for k, v in globals().items() if k = "__builtins__"}

# >>> import test

# >>> test.test()
# {
#     '__file__': 'test.pyc',
#     '__name__': 'test',
#     'a': 1,
#      'test': <function test at 0x10bd85e60>,
# }
# 可通过 .dict 访问其他模块的名字空间。

# >>> test.__dict__      # test 模块的名字空间
# {
#     '__file__': 'test.pyc',
#     '__name__': 'test',
#     'a': 1,
#     'test': <function test at 0x10bd85e60>,
# }

# >>> import sys

# >>> sys.modules[__name__].__dict__ is globals() # 当前模块名字空间和 globals 相同。
# True
# 与名字空间有关的内容很多，比如作用域、LEGB 查找规则、成员查找规则等等。所有这些，都将在相关章节中给出详细说明。

# 使用名字空间管理上下文对象，带来无与伦比的灵活性，但也牺牲了执行性能。毕竟从字典中查找对象远比指针低效很多，各有得失。

# 内存管理
# 为提升执行性能，Python 在内存管理上做了大量工作。最直接的做法就是用内存池来减少操作系统内存分配和回收操作，那些小于等于 256 字节对象，将直接从内存池中获取存储空间。

# 根据需要，虚拟机每次从操作系统申请一块 256KB，取名为 arena 的大块内存。并按系统页大小，划分成多个 pool。每个 pool 继续分割成 n 个大小相同的 block，这是内存池最小存储单位。

# block 大小是 8 的倍数，也就是说存储 13 字节大小的对象，需要找 block 大小为 16 的 pool 获取空闲块。所有这些都用头信息和链表管理起来，以便快速查找空闲区域进行分配。

# 大于 256 字节的对象，直接用 malloc 在堆上分配内存。程序运行中的绝大多数对象都小于这个阈值，因此内存池策略可有效提升性能。

# 当所有 arena 的总容量超出限制 (64MB) 时，就不再请求新的 arena 内存。而是如同 "大对象" 一样，直接在堆上为对象分配内存。另外，完全空闲的 arena 会被释放，其内存交还给操作系统。

# 引用传递

# 对象总是按引用传递，简单点说就是通过复制指针来实现多个名字指向同一对象。因为 arena 也是在堆上分配的，所以无论何种类型何种大小的对象，都存储在堆上。Python 没有值类型和引用类型一说，就算是最简单的整数也是拥有标准头的完整对象。

# >>> a = object()

# >>> b = a
# >>> a is b
# True

# >>> hex(id(a)), hex(id(b))  # 地址相同，意味着对象是同一个。
# ('0x10b1f5640', '0x10b1f5640')

# >>> def test(x):   
# ... print hex(id(x))  

# >>> test(a)
# 0x10b1f5640     # 地址依旧相同。
# 如果不希望对象被修改，就需使用不可变类型，或对象复制品。

# 不可变类型：int, long, str, tuple, frozenset
# 除了某些类型自带的 copy 方法外，还可以：

# 使用标准库的 copy 模块进行深度复制。
# 序列化对象，如 pickle、cPickle、marshal。
# 下面的测试建议不要用数字等不可变对象，因为其内部的缓存和复用机制可能会造成干扰。

# >>> import copy

# >>> x = object()
# >>> l = [x]    # 创建一个列表。

# >>> l2 = copy.copy(l)  # 浅复制，仅复制对象自身，而不会递归复制其成员。
# >>> l2 is l    # 可以看到复制列表的元素依然是原对象。
# False
# >>> l2[0] is x
# True

# >>> l3 = copy.deepcopy(l) # 深度复制，会递归复制所有深度成员。
# >>> l3 is l    # 列表元素也被复制了。
# False
# >>> l3[0] is x
# False
# 循环引用会影响 deepcopy 函数的运作，建议查阅官方标准库文档。

# 引用计数

# Python 默认采用引用计数来管理对象的内存回收。当引用计数为 0 时，将立即回收该对象内存，要么将对应的 block 块标记为空闲，要么返还给操作系统。

# 为观察回收行为，我们用 del 监控对象释放。

# >>> class User(object):
# ...     def __del__(self):
# ...         print "Will be dead"

# >>> a = User()
# >>> b = a

# >>> import sys
# >>> sys.getrefcount(a)
# 3

# >>> del a    # 删除引用，计数减小。
# >>> sys.getrefcount(b)
# 2

# >>> del b    # 删除最后一个引用，计数器为 0，对象被回收。
# Will be dead
# 某些内置类型，比如小整数，因为缓存的缘故，计数永远不会为 0，直到进程结束才由虚拟机清理函数释放。

# 除了直接引用外，Python 还支持弱引用。允许在不增加引用计数，不妨碍对象回收的情况下间接引用对象。但不是所有类型都支持弱引用，比如 list、dict ，弱引用会引发异常。

# 改用弱引用回调监控对象回收。

# >>> import sys, weakref

# >>> class User(object): pass

# >>> def callback(r):   # 回调函数会在原对象被回收时调用。
# ...      print "weakref object:", r
# ...      print "target object dead"

# >>> a = User()

# >>> r = weakref.ref(a, callback) # 创建弱引用对象。

# >>> sys.getrefcount(a)   # 可以看到弱引用没有导致目标对象引用计数增加。
# 2      # 计数 2 是因为 getrefcount 形参造成的。

# >>> r() is a    # 透过弱引用可以访问原对象。
# True

# >>> del a     # 原对象回收，callback 被调用。
# weakref object: <weakref at 0x10f99a368; dead>
# target object dead

# >>> hex(id(r))    # 通过对比，可以看到 callback 参数是弱引用对象。
# '0x10f99a368'    # 因为原对象已经死亡。

# >>> r() is None    # 此时弱引用只能返回 None。也可以此判断原对象死亡。
# True
# 引用计数是一种简单直接，并且十分高效的内存回收方式。大多数时候它都能很好地工作，除了循环引用造成计数故障。简单明显的循环引用，可以用弱引用打破循环关系。但在实际开发中，循环引用的形成往往很复杂，可能由 n 个对象间接形成一个大的循环体，此时只有靠 GC 去回收了。

# 垃圾回收

# 事实上，Python 拥有两套垃圾回收机制。除了引用计数，还有个专门处理循环引用的 GC。通常我们提到垃圾回收时，都是指这个 "Reference Cycle Garbage Collection"。

# 能引发循环引用问题的，都是那种容器类对象，比如 list、set、object 等。对于这类对象，虚拟机在为其分配内存时，会额外添加用于追踪的 PyGC_Head。这些对象被添加到特殊链表里，以便 GC 进行管理。

# typedef union _gc_head {
#     struct {
#         union _gc_head *gc_next;
#         union _gc_head *gc_prev;
#         Py_ssize_t gc_refs;
#     } gc;
#     long double dummy;
# } PyGC_Head;
# 当然，这并不表示此类对象非得 GC 才能回收。如果不存在循环引用，自然是积极性更高的引用计数机制抢先给处理掉。也就是说，只要不存在循环引用，理论上可以禁用 GC。当执行某些密集运算时，临时关掉 GC 有助于提升性能。

# >>> import gc

# >>> class User(object):
# ...     def __del__(self):
# ...         print hex(id(self)), "will be dead"

# >>> gc.disable()    # 关掉 GC

# >>> a = User()  
# >>> del a     # 对象正常回收，引用计数不会依赖 GC。
# 0x10fddf590 will be dead
# 同 .NET、JAVA 一样，Python GC 同样将要回收的对象分成 3 级代龄。GEN0 管理新近加入的年轻对象，GEN1 则是在上次回收后依然存活的对象，剩下 GEN2 存储的都是生命周期极长的家伙。每级代龄都有一个最大容量阈值，每次 GEN0 对象数量超出阈值时，都将引发垃圾回收操作。

# #define NUM_GENERATIONS 3

# /* linked lists of container objects */
# static struct gc_generation generations[NUM_GENERATIONS] = {
#     /* PyGC_Head, threshold, count */
#     {{{GEN_HEAD(0), GEN_HEAD(0), 0}}, 700, 0},
#     {{{GEN_HEAD(1), GEN_HEAD(1), 0}}, 10, 0},
#     {{{GEN_HEAD(2), GEN_HEAD(2), 0}}, 10, 0},
# };
# GC 首先检查 GEN2，如阈值被突破，那么合并 GEN2、GEN1、GEN0 几个追踪链表。如果没有超出，则检查 GEN1。GC 将存活的对象提升代龄，而那些可回收对象则被打破循环引用，放到专门的列表等待回收。

# >>> gc.get_threshold()  # 获取各级代龄阈值
# (700, 10, 10)

# >>> gc.get_count()   # 各级代龄链表跟踪的对象数量
# (203, 0, 5)
# 包含 del 方法的循环引用对象，永远不会被 GC 回收，直至进程终止。

# 这回不能偷懒用 del 监控对象回收了，改用 weakref。因 IPython 对 GC 存在干扰，下面的测试代码建议在原生 shell 中进行。

# >>> import gc, weakref

# >>> class User(object): pass
# >>> def callback(r): print r, "dead"

# >>> gc.disable()     # 停掉 GC，看看引用计数的能力。

# >>> a = User(); wa = weakref.ref(a, callback)
# >>> b = User(); wb = weakref.ref(b, callback)

# >>> a.b = b; b.a = a    # 形成循环引用关系。

# >>> del a; del b     # 删除名字引用。
# >>> wa(), wb()     # 显然，计数机制对循环引用无效。
# (<__main__.User object at 0x1045f4f50>, <__main__.User object at 0x1045f4f90>)

# >>> gc.enable()     # 开启 GC。
# >>> gc.isenabled()     # 可以用 isenabled 确认。
# True

# >>> gc.collect()     # 因为没有达到阈值，我们手工启动回收。
# <weakref at 0x1045a8cb0; dead> dead  # GC 的确有对付基友的能力。 
# <weakref at 0x1045a8db8; dead> dead  # 这个地址是弱引用对象的，别犯糊涂。
# 一旦有了 del，GC 就拿循环引用没办法了。

# >>> import gc, weakref

# >>> class User(object):
# ... def __del__(self): pass    # 难道连空的 __del__ 也不行？

# >>> def callback(r): print r, "dead"

# >>> gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK) # 输出更详细的回收状态信息。
# >>> gc.isenabled()      # 确保 GC 在工作。
# True

# >>> a = User(); wa = weakref.ref(a, callback)
# >>> b = User(); wb = weakref.ref(b, callback)
# >>> a.b = b; b.a = a

# >>> del a; del b
# >>> gc.collect()      # 从输出信息看，回收失败。
# gc: collecting generation 2...
# gc: objects in each generation: 520 3190 0
# gc: uncollectable <User 0x10fd51fd0>   # a
# gc: uncollectable <User 0x10fd57050>   # b
# gc: uncollectable <dict 0x7f990ac88280>  # a.__dict__
# gc: uncollectable <dict 0x7f990ac88940>  # b.__dict__
# gc: done, 4 unreachable, 4 uncollectable, 0.0014s elapsed.
# 4

# >>> xa = wa()
# >>> xa, hex(id(xa.__dict__))
# <__main__.User object at 0x10fd51fd0>, '0x7f990ac88280',

# >>> xb = wb()
# >>> xb, hex(id(xb.__dict__))
# <__main__.User object at 0x10fd57050>, '0x7f990ac88940'
# 关于用不用 del 的争论很多。大多数人的结论是坚决抵制，诸多 "牛人" 也是这样教导新手的。可毕竟 del 承担了析构函数的角色，某些时候还是有其特定的作用的。用弱引用回调会造成逻辑分离，不便于维护。对于一些简单的脚本，我们还是能保证避免循环引用的，那不妨试试。就像前面例子中用来监测对象回收，就很方便。

# 编译
# Python 实现了栈式虚拟机 (Stack-Based VM) 架构，通过与机器无关的字节码来实现跨平台执行能力。这种字节码指令集没有寄存器，完全以栈 (抽象层面) 进行指令运算。尽管很简单，但对普通开发人员而言，是无需关心的细节。

# 要运行 Python 语言编写的程序，必须将源码编译成字节码。通常情况下，编译器会将源码转换成字节码后保存在 pyc 文件中。还可用 -O 参数生成 pyo 格式，这是简单优化后的 pyc 文件。

# 编译发生在模块载入那一刻。具体来看，又分为 pyc 和 py 两种情况。

# 载入 pyc 流程：

# 核对文件 Magic 标记。
# 检查时间戳和源码文件修改时间是否相同，以确定是否需要重新编译。
# 载入模块。
# 如果没有 pyc，那么就需要先完成编译：

# 对源码进行 AST 分析。
# 将分析结果编译成 PyCodeObject。
# 将 Magic、源码文件修改时间、PyCodeObject 保存到 pyc 文件中。
# 载入模块。
# Magic 是一个特殊的数字，由 Python 版本号计算得来，作为 pyc 文件和 Python 版本检查标记。PyCodeObject 则包含了代码对象的完整信息。

# typedef struct {
#     PyObject_HEAD
#     int co_argcount;  // 参数个数，不包括 *args, **kwargs。
#     int co_nlocals;  // 局部变量数量。
#     int co_stacksize;  // 执行所需的栈空间。
#     int co_flags;   // 编译标志，在创建 Frame 时用得着。
#     PyObject *co_code;  // 字节码指令。
#     PyObject *co_consts;  // 常量列表。
#     PyObject *co_names;  // 符号列表。
#     PyObject *co_varnames; // 局部变量名列表。
#     PyObject *co_freevars; // 闭包: 引用外部函数名字列表。
#     PyObject *co_cellvars; // 闭包: 被内部函数引用的名字列表。
#     PyObject *co_filename; // 源码文件名。
#     PyObject *co_name;  // PyCodeObject 的名字，函数名、类名什么的。
#     int co_firstlineno;  // 这个 PyCodeObject 在源码文件中的起始位置，也就是行号。
#     PyObject *co_lnotab;  // 字节码指令偏移量和源码行号的对应关系，反汇编时用得着。
#     void *co_zombieframe;  // 为优化准备的特殊 Frame 对象。
#     PyObject *co_weakreflist; // 为弱引用准备的...
# } PyCodeObject;
# 无论是模块还是其内部的函数，都被编译成 PyCodeObject 对象。内部成员都嵌套到 co_consts 列表中。

# >>> pycat test.py
# """
#     Hello, World
# """

# def add(a, b):
#     return a + b

# c = add(10, 20)

# >>> code = compile(open("test.py").read(), "test.py", "exec")

# >>> code.co_filename, code.co_name, code.co_names
# ('test.py', '<module>', ('__doc__', 'add', 'c'))

# >>> code.co_consts
# ('\n Hello, World\n', <code object add at 0x105b76e30, file "test.py", line 5>, 10,
# 20, None)

# >>> add = code.co_consts[1]
# >>> add.co_varnames
# ('a', 'b')
# 除了内置 compile 函数，标准库里还有 py_compile、compileall 可供选择。

# >>> import py_compile, compileall

# >>> py_compile.compile("test.py", "test.pyo")
# >>> ls
# main.py* test.py  test.pyo

# >>> compileall.compile_dir(".", 0)
# Listing . ...
# Compiling ./main.py ...
# Compiling ./test.py ...
# 如果对 pyc 文件格式有兴趣，但又不想看 C 代码，可以到 /usr/lib/python2.7/compiler 目录里寻宝。又或者你对反汇编、代码混淆、代码注入等话题更有兴趣，不妨看看标准库里的 dis。

# 执行
# 相比 .NET、JAVA 的 CodeDOM 和 Emit，Python 天生拥有无与伦比的动态执行优势。

# 最简单的就是用 eval() 执行表达式。

# >>> eval("(1 + 2) * 3")  # 假装看不懂这是啥……
# 9

# >>> eval("{'a': 1, 'b': 2}") # 将字符串转换为 dict。
# {'a': 1, 'b': 2}
# eval 默认会使用当前环境的名字空间，当然我们也可以带入自定义字典。

# >>> x = 100
# >>> eval("x + 200")  # 使用当前上下文的名字空间。
# 300

# >>> ns = dict(x = 10, y = 20)
# >>> eval("x + y", ns)  # 使用自定义名字空间。
# 30

# >>> ns.keys()   # 名字空间里多了 __builtins__。
# ['y', 'x', '__builtins__']
# 要执行代码片段，或者 PyCodeObject 对象，那么就需要动用 exec 。同样可以带入自定义名字空间，以避免对当前环境造成污染。

# >>> py = """
# ... class User(object):
# ...     def __init__(self, name):
# ...         self.name = name
# ...     def __repr__(self):
# ...         return "<User: {0:x}; name={1}>".format(id(self), self.name)
# ... """

# >>> ns = dict()
# >>> exec py in ns   # 执行代码片段，使用自定义的名字空间。

# >>> ns.keys()   # 可以看到名字空间包含了新的类型：User。
# ['__builtins__', 'User']

# >>> ns["User"]("Tom")  # 完全可用。貌似用来开发 ORM 会很简单。
# <User: 10547f290; name=Tom>
# 继续看 exec 执行 PyCodeObject 的演示。

# >>> py = """
# ... def incr(x):
# ...     global z
# ...     z += x
# ... """

# >>> code = compile(py, "test", "exec")   # 编译成 PyCodeObject。

# >>> ns = dict(z = 100)     # 自定义名字空间。
# >>> exec code in ns     # exec 执行以后，名字空间多了 incr。

# >>> ns.keys()      # def 的意思是创建一个函数对象。
# ['__builtins__', 'incr', 'z']

# >>> exec "incr(x); print z" in ns, dict(x = 50) # 试着调用这个 incr，不过这次我们提供一个
# 150        # local 名字空间，以免污染 global。
# >>> ns.keys()      # 污染没有发生。
# ['__builtins__', 'incr', 'z']
# 动态执行一个 py 文件，可以考虑用 execfile()，或者 runpy 模块。
