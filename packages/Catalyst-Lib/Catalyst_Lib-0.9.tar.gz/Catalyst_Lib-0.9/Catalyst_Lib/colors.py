from random import randint


def printFormatTable():
    """
    It prints a table of all the possible combinations of foreground and background colors, and styles
    """
    for style in range(2):
        for fg in range(30, 38):
            s1 = ''
            for bg in range(40, 48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 = s1 + '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')


class printStyle:

    def __init__(self):
        """
        It creates a dictionary of all the possible styles and background styles that can be used in the terminal
        """
        self.stylesList = ["black", "red", "green", "brown", "blue", "purple", "cyan", "light_gray", "dark_gray",
                           "light_red",
                           "light_green", "yellow", "light_blue", "light_purple", "light_cyan", "light_white", "bold",
                           "faint",
                           "italic", "underline", "blink", "negative", "crossed"]
        self.bgstylelist = ["black", "red", "green", "orange", "blue", "purple", "cyan", "light_gray"]
        self.styles = {}
        self.bgstyles = {}
        item = 29
        round = 1
        bgitem = 40
        for style in self.bgstylelist:
            self.bgstyles[style] = f"\033[{bgitem}m"
            bgitem = bgitem + 1

        for style in self.stylesList:
            if round == 1 or round == 2:
                item = item + 1
                if item == 38:
                    round = round + 1
                    item = 30
                    if round == 3:
                        item = 1
                self.styles[style] = f"\033[{round - 1};{item}m"
            else:
                if (item == 5) or (item == 7):
                    item = item + 2
                else:
                    item = item + 1
                self.styles[style] = f"\033[{item}m"

        if not __import__("sys").stdout.isatty():
            for _ in dir():
                if isinstance(_, str) and _[0] != "_":
                    locals()[_] = ""

        else:
            if __import__("platform").system() == "Windows":
                kernel32 = __import__("ctypes").wind11.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                del kernel32

    def getStyle(self, color: str):
        """
        It returns the style of the color.

        :param color: The color of the text
        :type color: str
        :return: The style of the color.
        """
        return self.styles[color]

    def getbgStyle(self, color: str):
        """
        It takes a color as a string and returns the corresponding background style

        :param color: The color of the background
        :type color: str
        :return: The background style of the color.
        """
        return self.bgstyles[color]

    def getbgStyleList(self):
        """
        It returns a list of the background styles that are available in the current theme
        :return: The list of background styles.
        """
        return self.bgstylelist

    def getStyleList(self):
        """
        It returns a list of all the styles in the document
        :return: The list of styles.
        """
        return self.stylesList

    def bgstyle(self, color: str, message: str):
        """
        It returns a string with the background color and the message.

        :param color: The color you want to use
        :type color: str
        :param message: The message you want to send
        :type message: str
        :return: the message with the background color.
        """
        return f"{self.getbgStyle(color)}{message}"

    def style(self, color: str, message: str):
        """
        This function takes in a color and a message and returns the message with the color

        :param color: The color you want to use
        :type color: str
        :param message: The message you want to send
        :type message: str
        :return: the message with the color style.
        """
        return f"{self.getStyle(color)}{message}\033[0m"


class color:

    def __init__(self, color: tuple or str):
        """
        If the color is a string, convert it to a tuple. If the color is a tuple, set it to the color. If the color is
        neither, raise an error

        :param color: The color of the text. Can be a hex code or a tuple of RGB values
        :type color: tuple or str
        """
        if type(color) == str:
            self.color = hex_to_rgb(color)
        elif type(color) == tuple:
            self.color = color
        else:
            raise ValueError("The color given is in an incorrect format")

    def hex(self):
        """
        It takes the RGB values of the color attribute of the object and converts them to a hexadecimal value
        :return: The hex value of the color.
        """
        return rgb_to_hex(r=self.color[0], g=self.color[1], b=self.color[2])

    def rgb(self):
        """
        It returns the color of the object.
        :return: The color of the object.
        """
        return self.color

    def __str__(self):
        """
        It returns a string that contains the ANSI escape code for the color of the object
        :return: The color of the text.
        """
        return '\033[{};2;{};{};{}m'.format(38, self.color[0], self.color[1], self.color[2])

    def background(self):
        """
        It takes the color of the background and returns the color in the format of the ANSI escape code
        :return: The background color of the text.
        """
        return '\033[{};2;{};{};{}m'.format(48, self.color[0], self.color[1], self.color[2])


def rgb_to_hex(r, g, b):
    """
    It takes three integers between 0 and 255, and returns a string of six characters, where the first two characters are
    the hexadecimal representation of the first integer, the second two characters are the hexadecimal representation of the
    second integer, and the last two characters are the hexadecimal representation of the third integer

    :param r: red
    :param g: The green value of the color
    :param b: The number of bits per pixel
    :return: The hexadecimal representation of the RGB values.
    """
    return '{:x}{:x}{:x}'.format(r, g, b)


def hex_to_rgb(hex):
    """
    It takes a hexadecimal string and returns a tuple of three integers

    :param hex: The hexadecimal color code
    :return: A tuple of the RGB values of the hex color code.
    """
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)
    return tuple(rgb)


def randColor():
    """
    `randColor()` returns a random color
    :return: A random color.
    """
    randcolor = (randint(0, 255), randint(0, 255), randint(0, 255))
    return color(color=randcolor)


def colored(Color: color, message: str, background: bool = False):
    """
    It takes a color, a message, and a boolean, and returns the message in the color specified

    :param Color: color - The color you want to use
    :type Color: color
    :param message: The message you want to print
    :type message: str
    :param background: bool = False, defaults to False
    :type background: bool (optional)
    :return: a string with the color and message.
    """
    return f"{str(Color.background()) if background else str(Color)}{message}\033[0m"
