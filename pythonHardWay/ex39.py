# -- coding:utf-8 --
ten_thing = "Apples Oranges Crows Telephone Light Sugar"
print("Wait there's not 10 thing in that list, let's fix that.")

stuff = ten_thing.split(' ')
more_stuff = ["Day", "Night", "Song", "Feisbee", "Corn", "Banana", "Girl", "Boy"]

while len(stuff) != 10:
	next_one = more_stuff.pop()
	print("Adding:  ", next_one)
	stuff.append(next_one)
	print("There's %d items now." % len(stuff))
	
print("There we go: ", stuff)

print("let's do some things with stuff")

print(stuff[1])
print(stuff[-1]) # whoa! fancy
print(stuff.pop())
print(' '.join(stuff))
print('#'.join(stuff[3:5]))	

# 自己的练习

# 1、将每一个被调用的函数以上述的方式翻译成 Python 实际执行的动作。例如： ' '.join(things) 其实是 join(' ', things)
# print(''.join(stuff))
# print(''.join('#', stuff[3:5]))

# 2、将这两种方式翻译为自然语言。例如， ' '.join(things) 可以翻译成“用 ‘ ‘ 连接(join) things”，
# 	而 join(' ', things) 的意思是“为 ‘ ‘ 和 things 调用 join 函数”。这其实是同一件事情。
 
# 3、上网阅读一些关于“面向对象编程(Object Oriented Programming)”的资料。晕了吧？嗯，我以前也是。别担心。
# 	你将从这本书学到足够用的关于面向对象编程的基础知识，而以后你还可以慢慢学到更多。
 
# 4、查一下 Python中的 “class” 是什么东西。不要阅读关于其他语言的 “class” 的用法，这会让你更糊涂。
 
# 5、dir(something) 和 something 的 class 有什么关系？
 
# 6、如果你不知道我讲的是些什么东西，别担心。程序员为了显得自己聪明，于是就发明了 Opject Oriented Programming，简称为 OOP，
# 	然后他们就开始滥用这个东西了。如果你觉得这东西太难，你可以开始学一下 “函数编程(functional programming)”。