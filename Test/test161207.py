# !/usr/bin/env python
# coding:utf-8

a = 19 + 2 * 4 - 8 / 2
print a
print "free" + 'a'
print "free" + str(a)
# 这里 repr()是一个函数，其实就是反引号的替代品，它能够把结果字符串转化为合法的 python 表达式。
print "free" + repr(a)
name = raw_input("What is your name?")
age = raw_input("How old are you?")
print "Your name is:", name
print "You are " + age + " years old."
after_ten = int(age) + 10
print "You will be " + str(after_ten) + " years old after ten years."


