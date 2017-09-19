import curses
import shutil
import time
import random
from math import sqrt


class Tile:  # Just tiles

    """
    Super-class that represents the basic information for an object of the grid
    """

    def __init__(self, coords, color=curses.COLOR_WHITE, character="█", transitable=False):
        """
        Constructor for the tile object
        :param coords: Initial coords of the object (x, y)
        :param color: Color of the object
        :param character: Character which will represent the object
        :param transitable: Self-explanatory
        """
        self.coords = coords
        self.character = character
        self.color = color
        self.transitable = transitable
        self.nextone = coords


class Mapa:
    def __init__(self, alto, ancho):
        """
        Constructor class for the map
        :param alto: height
        :param ancho: width
        """
        self.alto = alto
        self.ancho = ancho-1
        self.grid = self.gen_grid()

    def gen_grid(self):
        """
        Generates the grid matrix, filing it with empty tiles
        :return: Matrix map
        """
        returneo = []
        for y in range(0, self.alto):
            returneo.append([])
            for x in range(0, self.ancho):
                returneo[y].append(Tile((x, y)))
        return returneo

    def print_grid(self, stdscr):
        """
        Prints the map using the curses library
        :param stdscr: Stdscr object from curses library
        :return: VOID
        """
        stdscr.clear()
        for y in range(0, len(self.grid)-1):
            y = self.grid[y]
            for x in y:
                stdscr.addstr(x.character, curses.color_pair(x.color))
            stdscr.addstr("\n")
        for x in self.grid[-1]:
            stdscr.addstr(x.character, curses.color_pair(x.color))
        stdscr.refresh()

    def coords_in(self, coords):
        if coords[0] in range(0, self.ancho) and coords[1] in range(0, self.alto):
            return True
        return False

    def get_coords(self, coords):
        """
        Return the object at given coords
        :param coords: Coordinates to search in
        :return: (x, y) or False if not a valid tile
        """
        if not self.coords_in(coords):
            raise Exception
        return self.grid[coords[1]][coords[0]]

    def set_coords(self, coords, objeto):
        """
        Changes the object at given coords
        :param coords: Coordinates to change
        :param objeto: Object to insert
        :return: False if not a valid position
        """
        if not self.coords_in(coords):
            raise Exception
        self.grid[coords[1]][coords[0]] = objeto


class Generator:

    def __init__(self, mapa, entrada=(0, 0.5), salida=(1, 0.5)):
        self.variacion = ((0, -1), (1, 0), (0, 1), (-1, 0))
        self.mapa = mapa
        self.pointer = (int(entrada[0]*(self.mapa.ancho-1)), int(entrada[1]*(self.mapa.alto-1)))
        self.exit = (int(salida[0]*(self.mapa.ancho-1)), int(salida[1]*(self.mapa.alto-1)))
        self.mapa.set_coords(self.exit, Tile(self.exit, character="#"))
        self.stack = []

    def run(self, tiempo=None):
        while self.pointer is not None:
            self.mapa.set_coords(self.pointer, Tile(self.pointer, character=" ", color=curses.COLOR_CYAN))
            self.pointer = self.choose_next()
            if tiempo is not None:
                self.mapa.print_grid(tiempo[1])
                time.sleep(tiempo[0])
        self.mapa.set_coords(self.exit, Tile(self.pointer, character=" ", color=curses.COLOR_CYAN))

    def choose_next(self):
        possibilities = []
        for x in self.variacion:
            coords = (self.pointer[0] + x[0], self.pointer[1] + x[1])
            if self.possible(coords):
                possibilities.append(coords)
        if len(possibilities) == 0:
            if len(self.stack) == 0:
                return None
            return self.stack.pop()
        eleccion = None
        for x in possibilities:
            for y in self.variacion:
                coords = (x[0] + y[0], x[1] + y[1])
                if self.mapa.get_coords(coords).character == "#":
                    eleccion = x
        if eleccion is None:
            eleccion = random.choice(possibilities)
        self.stack.append(eleccion)
        return eleccion

    def possible(self, coords):
        if self.adyacent(coords) or self.coord_in_frame(coords):
            return False
        return True

    def adyacent(self, coords):
        counter = 0
        for x in self.variacion:
            coordinates = (coords[0] + x[0], coords[1] + x[1])
            try:
                coordinates = self.mapa.get_coords(coordinates)
            except:
                continue
            if coordinates.character == " ":
                counter += 1
        if counter > 1:
            return True
        return False

    def coord_in_frame(self, coord):
        if coord[0] in range(1, self.mapa.ancho-1) and coord[1] in range(1, self.mapa.alto-1):
            return False
        return True


class Solver:

    def __init__(self, mapa):
        self.mapa = mapa
        self.pointer = self.get_entry()
        self.entry = self.pointer
        self.variacion = ((0, -1), (1, 0), (0, 1), (-1, 0))
        self.stack = []

    def get_entry(self):
        for x in range(1, self.mapa.ancho-2):
            for y in (0, self.mapa.alto-1):
                if self.mapa.get_coords((x, y)).character == " ":
                    return x, y
        for x in (0, self.mapa.ancho-1):
            for y in range(1, self.mapa.alto-2):
                if self.mapa.get_coords((x, y)).character == " ":
                    return x, y

    def run(self, tiempo=None):
        while self.pointer is not None:
            self.pointer = self.choose_next()
            if tiempo is not None:
                time.sleep(tiempo[0])
                self.mapa.print_grid(tiempo[1])

    def choose_next(self):
        possibilities = []
        for x in self.variacion:
            coords = (self.pointer[0] + x[0], self.pointer[1] + x[1])
            if self.coord_in_frame(coords) and coords != self.entry and self.pointer != self.entry \
                    and self.mapa.get_coords(coords).character == " ":
                self.mapa.set_coords(self.pointer, Tile(self.pointer, color=curses.COLOR_GREEN))
                self.mapa.set_coords(coords, Tile(coords, color=curses.COLOR_GREEN))
                return None
            if self.possible(coords):
                possibilities.append(coords)
        if len(possibilities) == 0:
            self.mapa.set_coords(self.pointer, Tile(self.pointer, color=curses.COLOR_RED))
            return self.stack.pop()
        self.mapa.set_coords(self.pointer, Tile(self.pointer, color=curses.COLOR_GREEN))
        eleccion = random.choice(possibilities)
        self.stack.append(self.pointer)
        return eleccion

    def possible(self, coords):
        if self.coord_in_frame(coords) or self.mapa.get_coords(coords).character != " ":
            return False
        return True

    def coord_in_frame(self, coord):
        if coord[0] in range(1, self.mapa.ancho-1) and coord[1] in range(1, self.mapa.alto-1):
            return False
        return True


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    colors = []
    for i in range(0, curses.COLORS):  # Curses shit
        curses.init_pair(i, i, -1)
        colors.append(i)
    size = list(shutil.get_terminal_size())
    while True:
        try:
            mapa = Mapa(size[1], size[0])
            gen = Generator(mapa)
            gen.run()
            mapa.print_grid(stdscr)
            solv = Solver(mapa)
            solv.run()
            mapa.print_grid(stdscr)
            time.sleep(1)
        except IndexError:
            pass
        except KeyboardInterrupt:
            exit()
curses.wrapper(main)
