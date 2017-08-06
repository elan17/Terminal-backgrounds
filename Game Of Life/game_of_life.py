#! /usr/bin/env python

import curses
import shutil
import time
import random
import copy

"""
Under-development. Not pretty useful right now as it eats tons of cpu with the random option
"""


class Tile:  # Just tiles

    """
    Super-class that represents the basic information for an object of the grid
    """

    def __init__(self, color=0, character=" "):
        """
        Constructor for the tile object
        :param color: Color of the object
        :param character: Character which will represent the object
        """
        self.character = character
        self.color = color


class Grid:
    def __init__(self, alto, ancho, vacia):
        """
        Constructor class for the map
        :param alto: height
        :param ancho: width
        """
        self.alto = alto
        self.ancho = ancho
        self.grid = {}
        self.vacia = vacia

    def print_grid(self, stdscr):
        """
        Prints the map using the curses library
        :param stdscr: Stdscr object from curses library
        :return: VOID
        """
        stdscr.clear()
        for y_ind in range(0, self.alto-1):
            for x_ind in range(self.ancho):
                x = self.get_coords((x_ind, y_ind))
                stdscr.addstr(x.character, curses.color_pair(x.color))
            stdscr.addstr("\n")
        for x_ind in range(self.ancho):
            x = self.get_coords((x_ind, y_ind + 1))
            stdscr.addstr(x.character, curses.color_pair(x.color))
        stdscr.refresh()

    def remove(self, coords):
        del self.grid[(coords[0] % self.ancho, coords[1] % self.alto)]

    def get_coords(self, coords):
        """
        Return the object at given coords
        :param coords: Coordinates to search in
        :return: (x, y) or False if not a valid tile
        """
        converted = (coords[0] % self.ancho, coords[1] % self.alto)
        if converted in self.grid:
            return self.grid[converted]
        else:
            return self.vacia

    def set_coords(self, coords, objeto):
        """
        Changes the object at given coords
        :param coords: Coordinates to change
        :param objeto: Object to insert
        :return: False if not a valid position
        """
        self.grid[(coords[0] % self.ancho, coords[1] % self.alto)] = objeto


class Game(Grid):

    def __init__(self, size, color, character="#", patron=None):
        """
        Game object
        :param size: (width, height) of the terminal
        :param color: Color of the cells
        :param character: Character for the cells
        :param patron: Pattern to use. TODO
        """
        self.vacia = Tile()
        self.size = size
        super().__init__(size[1], size[0]-1, self.vacia)
        self.celula = Tile(color, character)
        self.born = []
        self.kill = []
        self.estados = []
        if patron is None:
            self.init_grid()
        else:
            self.load_pattern()

    def load_pattern(self):
        pass  # TODO

    def init_grid(self):
        """
        In case of no pattern provided, generates a random grid
        :return:
        """
        for x in range(self.ancho):
            for y in range(self.alto):
                if random.randint(0, 1) == 1:
                    self.set_coords((x, y), self.celula)

    def run(self, term):
        """
        Updates the game
        :param term: Terminal object to use to print
        """
        if list(shutil.get_terminal_size()) != self.size:
            raise Exception("Terminal changed size")
        if len(self.grid) == 0:
            exit()
        self.print_grid(term)
        self.update_coords()
        for x in self.kill:
            self.remove(x)
        for x in self.born:
            self.set_coords(x, self.celula)
        if self.grid in self.estados:
            raise Exception("Static state")
        self.estados.append(copy.copy(self.grid))
        if len(self.estados) > 10:
            self.estados.pop(0)
        self.born = []
        self.kill = []

    def count_neighbours(self, coords):
        """
        Count the number of neighbours a tile has
        :param coords: Coords to check
        :return: Number of neighbours
        """
        counter = 0
        for x_tmp in range(-1, 2):
            for y_tmp in range(-1, 2):
                if x_tmp == 0 and y_tmp == 0:
                    continue
                x = coords[0] + x_tmp
                y = coords[1] + y_tmp
                if self.get_coords((x, y)).character != " ":
                    counter += 1
        return counter

    def update_coords(self):
        """
        Update all coords of the game
        """
        for coords in self.grid.keys():
            if self.count_neighbours(coords) not in (2, 3):
                self.kill.append(coords)
            for x_tmp in range(-1, 2):
                for y_tmp in range(-1, 2):
                    x = x_tmp + coords[0]
                    y = y_tmp + coords[1]
                    if self.count_neighbours((x, y)) == 3:
                        self.born.append((x, y))


def main(stdscr):  # The root method, do not annoy him
    curses.curs_set(0)
    size = list(shutil.get_terminal_size())  # Gets terminal size so curses won't complain
    curses.start_color()
    curses.use_default_colors()
    colors = []
    for i in range(0, curses.COLORS):  # Curses shit
        curses.init_pair(i + 1, i, -1)
        colors.append(i)
    game = Game(size, random.choice(colors))
    while True:
        time.sleep(1/24)
        game.run(stdscr)

while True:
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        exit()
    except:
        pass
