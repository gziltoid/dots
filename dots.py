#!/usr/bin/env python3
from graphics import *
from random import randint

WIDTH, HEIGHT = 800, 600
CIRCLE_RADIUS = 7
SPEED = 10


def main():
    win = GraphWin("Dots", WIDTH, HEIGHT)
    win.setBackground("black")

    message = Text(Point(win.getWidth() / 2, 20), "Press any key to quit.")
    message.setTextColor("pink")
    message.setSize(18)
    message.draw(win)

    x, y = randint(6, WIDTH - 1 - CIRCLE_RADIUS), randint(6, HEIGHT - 1 - CIRCLE_RADIUS)
    c = Circle(Point(x, y), CIRCLE_RADIUS)
    c.setFill("white")
    c.draw(win)

    while not win.checkKey():
        c.move(SPEED, 0)
        time.sleep(.2)

    win.close()


main()
