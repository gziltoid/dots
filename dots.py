#!/usr/bin/env python3
from math import cos, pi, sin
from graphics import *
from random import randrange, uniform


WIDTH, HEIGHT = 800, 600
CIRCLE_RADIUS = 6
CIRCLE_NUMBERS = 80
SPEED = 0.6


def main():
    win = GraphWin("Dots", WIDTH, HEIGHT, autoflush=False)
    win.setBackground("black")

    message = Text(Point(win.getWidth() / 2, 20), "Click anywhere to quit.")
    message.setTextColor("pink")
    message.setSize(18)
    message.draw(win)

    circles = []
    for _ in range(CIRCLE_NUMBERS):
        x0, y0 = randrange(WIDTH), randrange(HEIGHT)
        c = Circle(Point(x0, y0), CIRCLE_RADIUS)
        angle = uniform(0, 2 * pi)
        dx = SPEED * cos(angle)
        dy = SPEED * sin(angle)
        c.setFill("white")
        c.draw(win)
        circles.append((c, dx, dy))

    while not win.checkMouse():
        for i, (c, dx, dy) in enumerate(circles):
            c.undraw()
            centerPoint = c.getCenter()
            curr_x, curr_y = centerPoint.x, centerPoint.y

            x = (curr_x + dx) % WIDTH
            y = (curr_y + dy) % HEIGHT

            c = Circle(Point(x, y), CIRCLE_RADIUS)
            c.setFill("white")
            c.draw(win)
            circles[i] = (c, dx, dy)

        update(30)


if __name__ == "__main__":
    main()
