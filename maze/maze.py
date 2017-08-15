import curses


class Tile:  # Just tiles

    """
    Super-class that represents the basic information for an object of the grid
    """

    def __init__(self, coords, color=0, character=" ", transitable=True):
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
        self.ancho = ancho
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

    def get_coords(self, coords):
        """
        Return the object at given coords
        :param coords: Coordinates to search in
        :return: (x, y) or False if not a valid tile
        """
        return self.grid[coords[1] % len(self.grid)][coords[0] % len(self.grid[0])]

    def set_coords(self, coords, objeto):
        """
        Changes the object at given coords
        :param coords: Coordinates to change
        :param objeto: Object to insert
        :return: False if not a valid position
        """
        try:
            self.grid[coords[1] % len(self.grid)][coords[0] % len(self.grid[0])] = objeto
        except IndexError:
            return False

