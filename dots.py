#!/usr/bin/env python3
import argparse
import subprocess
from collections import namedtuple
from math import cos, pi, sin
from random import randrange, uniform

from PIL import Image
from graphics import Point, Circle, GraphWin, Rectangle, Text, Line, update

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = '#34344a'
FONT_SIZE = 16
FONT_FAMILY = 'courier'
FONT_COLOR = '#f4978e'
DOT_RADIUS = 6
DOT_COLOR = '#7c90db'
DOTS_NUMBER = 80
DOT_SPEED = 0.5
LINE_COLOR = '#eac4d5'
DISTANCE_LIMIT = 80
FPS_LIMIT = 30

MovingDot = namedtuple('MovingDot', 'dot dx dy')


def create_window():
    win = GraphWin('Dots', SCREEN_WIDTH, SCREEN_HEIGHT, autoflush=False)

    rectangle = Rectangle(
        Point(0, 0),
        Point(SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1))
    rectangle.setFill(BG_COLOR)
    rectangle.draw(win)

    message = Text(Point(win.getWidth() / 2, SCREEN_HEIGHT - 20),
                   'Click anywhere to quit')
    message.setTextColor(FONT_COLOR)
    message.setFace(FONT_FAMILY)
    message.setSize(FONT_SIZE)
    message.draw(win)

    return win


def initialize(win):
    dots = []
    for _ in range(DOTS_NUMBER):
        x0, y0 = randrange(SCREEN_WIDTH), randrange(SCREEN_HEIGHT)
        dot = Circle(Point(x0, y0), DOT_RADIUS)
        dot.setFill(DOT_COLOR)
        dot.draw(win)
        angle = uniform(0, 2 * pi)
        dx = DOT_SPEED * cos(angle)
        dy = DOT_SPEED * sin(angle)
        dots.append(MovingDot(dot=dot, dx=dx, dy=dy))
    return dots


def undraw(dots, lines):
    for d in dots:
        d.dot.undraw()

    for line in lines:
        line.undraw()


def move(dots):
    for i, (dot, dx, dy) in enumerate(dots):
        p = dot.getCenter()
        x = (p.x + dx) % SCREEN_WIDTH
        y = (p.y + dy) % SCREEN_HEIGHT
        d = Circle(Point(x, y), DOT_RADIUS)
        dots[i] = MovingDot(dot=d, dx=dx, dy=dy)


def get_distance(p1, p2):
    return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5


def draw(win, dots, lines):
    # connect dots within a given distance from each other
    for i, d1 in enumerate(dots):
        p1 = d1.dot.getCenter()
        for d2 in dots[i + 1:]:
            p2 = d2.dot.getCenter()
            dist = get_distance(p1, p2)
            if dist < DISTANCE_LIMIT:
                line = Line(Point(p1.x, p1.y), Point(p2.x, p2.y))
                lines.append(line)
                line.setFill(LINE_COLOR)
                line.draw(win)

    for d in dots:
        d.dot.setFill(DOT_COLOR)
        d.dot.draw(win)


def main():
    win = create_window()
    dots = initialize(win)
    lines = []

    while not win.checkMouse():
        undraw(dots, lines)
        move(dots)
        draw(win, dots, lines)

        update(FPS_LIMIT)

        yield win


def save_as_gif(n):
    """
    Convert from EPS via PNG to GIF format using PIL
    :param n: frames number
    """
    images = []
    for i in range(n):
        img = Image.open(f'{i}.eps')
        img.save(f'{i}.png')
        images.append(img)
    
    images[0].save('dots.gif', save_all=True,
                   append_images=images[1:], loop=0)
    subprocess.call(' '.join(['rm', './*.eps', ' ./*.png']), shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Connecting dots and lines visualization.')
    parser.add_argument('--gif', action='store_true', help='save as gif')
    args = parser.parse_args()

    if not args.gif:
        for _ in main():
            pass
    else:
        n = 0
        for win in main():
            win.postscript(file=f"{n}.eps", colormode='color')
            n += 1
        
        save_as_gif(n)
