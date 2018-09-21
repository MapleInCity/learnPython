# -- coding:utf-8 --
from sys import exit


def start():
    print("You are in a dark room.")
    print("There is a door to your right and left.")
    print("Which one do you take?")

    next = input("> ")
    if next == "left":
        bear_room()
    elif next == "right":
        cthulhu_room()
    else:
        dead("You stumble around the room until you starve.")


def dead(why):
    print(why, "Good job!")
    exit(0)


def gold_room():
    print("This room is full of gold. How much do you take?")

    # s为字符串
    # s.isalnum() 所有字符都是数字或者字母
    # s.isalpha() 所有字符都是字母
    # s.isdigit() 所有字符都是数字
    # s.islower() 所有字符都是小写
    # s.isupper() 所有字符都是大写
    # s.istitle() 所有单词都是首字母大写，像标题
    # s.isspace() 所有字符都是空白字符、\t、\n、\r
    next = input("> ")
    if next.isdigit():
        how_much = int(next)
    else:
        dead("Man, learn to type a number.")
    
    if how_much < 50:
        print("Nice, you're not greedy, you win!")
        exit(0)
    else:
        dead("You greed bastard!")


def bear_room():
    print("There is a bear here.")
    print("The bear has a bunch of honey.")
    print("The fat bear is in front of anther door.")
    print("How are you going to move the dear?")
    bear_moved = False

    while True:
        next = input("> ")
        if next == "take honey":
            dead("The bear looks at you then slaps your face off.")
        elif next == "taunt bear" and not bear_moved:
            print("The bear has moved from the door. You can go through it now.")
            bear_moved = True
        elif next == "taunt bear" and bear_moved:
            dead("The bear gets pissed off and chews your leg off.")
        elif next == "open door" and bear_moved:
            gold_room()
        else:
            print("I got no idea what that means.")


def cthulhu_room():
    print("Here you see the great evil Cthulhu.")
    print("He, it, whatever stares at you and you go insane.")
    print("Do you flee for you life or eat your head?")

    next = input("> ")

    if "flee" in next:
        start()
    elif "head" in next:
        dead("Well that was tasty!")
    else:
        cthulhu_room()


start()
