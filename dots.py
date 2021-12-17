#!/usr/bin/env python3
from math import cos, pi, sin
from graphics import *
from random import randrange, uniform
import argparse
from PIL import Image
import subprocess


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CIRCLE_RADIUS = 6
CIRCLES_NUMBER = 80
CIRCLE_SPEED = 0.5
DISTANCE_LIMIT = 80


def main():
    win = GraphWin('Dots', SCREEN_WIDTH, SCREEN_HEIGHT, autoflush=False)

    rectangle = Rectangle(
        Point(0, 0),
        Point(SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1))
    rectangle.setFill('black')
    rectangle.draw(win)

    message = Text(Point(win.getWidth() / 2, 20), 'Click anywhere to quit')
    message.setTextColor('pink')
    message.setFace('courier')
    message.setSize(16)
    message.draw(win)

    circles = []
    lines = []

    for _ in range(CIRCLES_NUMBER):
        x0, y0 = randrange(SCREEN_WIDTH), randrange(SCREEN_HEIGHT)
        c = Circle(Point(x0, y0), CIRCLE_RADIUS)
        angle = uniform(0, 2 * pi)
        dx = CIRCLE_SPEED * cos(angle)
        dy = CIRCLE_SPEED * sin(angle)
        c.setFill('white')
        c.draw(win)
        circles.append((c, dx, dy))

    while not win.checkMouse():
        for line in lines:
            line.undraw()

        for i, (c, dx, dy) in enumerate(circles):
            c.undraw()
            centerPoint = c.getCenter()
            curr_x, curr_y = centerPoint.x, centerPoint.y

            x = (curr_x + dx) % SCREEN_WIDTH
            y = (curr_y + dy) % SCREEN_HEIGHT

            c = Circle(Point(x, y), CIRCLE_RADIUS)
            circles[i] = (c, dx, dy)

        for i, (c1, _, _) in enumerate(circles):
            centerPoint = c1.getCenter()
            x1, y1 = centerPoint.x, centerPoint.y
            for c2, _, _ in circles[i + 1:]:
                centerPoint2 = c2.getCenter()
                x2, y2 = centerPoint2.x, centerPoint2.y
                d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                if d < DISTANCE_LIMIT:
                    line = Line(Point(x1, y1), Point(x2, y2))
                    lines.append(line)
                    line.setFill('green')
                    line.draw(win)

        for c, _, _ in circles:
            c.setFill('white')
            c.draw(win)

        update(30)

        yield win


def save_as_gif(n):
    '''Convert from eps to gif format using PIL'''
    images = []
    for i in range(n):
        im = Image.open(f'{i}.eps')
        im.save(f'{i}.png')
        images.append(im)
    images[0].save('dots.gif', save_all=True,
                   append_images=images[1:], loop=0)
    subprocess.call(' '.join(['rm', './*.eps', ' ./*.png']), shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Cicles and lines visualization.')
    parser.add_argument('--gif', action='store_true', help='save as gif')
    args = parser.parse_args()
    print(args)
    if not args.gif:
        for _ in main():
            pass
    else:
        n = 0
        for win in main():
            # save the current TKinter object to postscript format
            win.postscript(file=f"{n}.eps", colormode='color')
            n += 1
        save_as_gif(n)
