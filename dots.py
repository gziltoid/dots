#!/usr/bin/env python3
from graphics import *
from random import randrange, uniform


WIDTH, HEIGHT = 800, 600
CIRCLE_RADIUS = 7


def main():
    win = GraphWin("Dots", WIDTH, HEIGHT)
    win.setBackground("black")

    message = Text(Point(win.getWidth() / 2, 20), "Click anywhere to quit.")
    message.setTextColor("pink")
    message.setSize(18)
    message.draw(win)

    x0, y0 = randrange(WIDTH), randrange(HEIGHT)
    c = Circle(Point(x0, y0), CIRCLE_RADIUS)
    c.setFill("white")
    c.draw(win)

    dx, dy = uniform(-3.0, 3.0), uniform(-3.0, 3.0)

    while True:
        c.undraw()
        centerPoint = c.getCenter()
        curr_x, curr_y = centerPoint.x, centerPoint.y

        x = (curr_x + dx) % WIDTH
        y = (curr_y + dy) % HEIGHT

        c = Circle(Point(x, y), CIRCLE_RADIUS)
        c.setFill("white")
        c.draw(win)

        time.sleep(0.015)

        if win.checkMouse():
            win.close()
            break


if __name__ == "__main__":
    main()
