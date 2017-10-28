import operator


class ColourFactory:
    @staticmethod
    def create(value):
        if type(value) is str:
            return Colour.get_colour_by_name(value)
        if type(value) is tuple:
            return Colour(value, None)
        if type(value) is Colour:
            return value
        return error


class Colour(tuple):
    _palete = {}

    def __new__(cls, value, name=None):
        return tuple.__new__(Colour, value)

    def __init__(self, value, name=None):
        super(Colour, self).__init__(value)
        self._name = name
        self.r = property(operator.itemgetter(0))
        self.g = property(operator.itemgetter(1))
        self.b = property(operator.itemgetter(2))

        if name is not None:
            Colour._palete[name] = self

    @staticmethod
    def get_colour_by_name(name):
        if name in Colour._palete:
            return Colour._palete[name]
        return None


lightred = Colour((255, 100, 100), "lightred")
red = Colour((255, 0, 0), "red")
darkred = Colour((100, 0, 0), "darkred")

lightgreen = Colour((100, 255, 100), "lightgreen")
green = Colour((0, 255, 0), "green")
darkgreen = Colour((0, 100, 0), "darkgreen")

lightblue = Colour((100, 100, 255), "lightblue")
blue = Colour((0, 0, 255), "blue")
darkblue = Colour((0, 0, 100), "darkblue")

white = Colour((255, 255, 255), "white")
lightgrey = Colour((200, 200, 200), "lightgrey")
grey = Colour((100, 100, 100), "grey")
darkgrey = Colour((50, 50, 50), "darkgrey")
black = Colour((0, 0, 0), "black")

lightorange = Colour((255, 200, 100), "lightorange")
orange = Colour((255, 165, 0), "orange")
darkorange = Colour((200, 120, 0), "darkorange")

error = Colour((100, 50, 200), "error")
