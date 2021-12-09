#!/usr/bin/env python3
from graphics import *
from random import randint
from math import sin, cos

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

    x0, y0 = randint(6, WIDTH - 1 - CIRCLE_RADIUS), randint(6,
                                                            HEIGHT - 1 - CIRCLE_RADIUS)
    c = Circle(Point(x0, y0), CIRCLE_RADIUS)
    c.setFill("white")
    c.draw(win)

    x, y = randint(-3, 3), randint(-3, 3)

    while not win.checkKey():
        c.move(x, y)
        time.sleep(.03)

    win.close()


main()
