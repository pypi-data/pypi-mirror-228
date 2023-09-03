import sys
import time
from datetime import datetime

from .colors import color, colored


def progressbar(it, colors: color = color(color=(0, 0, 0)), prefix: str = "", size: int = 60, out=sys.stdout):  # Python3.3+
    """
    It takes an iterable, and prints a progress bar to the console, with a percentage, and an estimate of how long it will
    take to complete

    :param it: the iterable object
    :param colors: the color of the bar
    :type colors: easylib.colors.color
    :param prefix: The text to be displayed before the progress bar
    :type prefix: str
    :param size: The length of the progress bar in characters, defaults to 60
    :type size: int (optional)
    :param out: The output stream to write to. Defaults to sys.stdout
    """
    itemsList = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    count = len(it)
    startTime = datetime.now()
    barSize = 0
    def show(j, barSize):
        """
        It prints a progress bar.

        :param j: the current iteration
        :param barSize: The size of the bar
        """
        x = int(size * j / count)
        if barSize < x:
            print(
                "\r{}[{}{}] {}% {:.01f}s".format(prefix, colored(colors, "█" * x), " " * (size - x),
                                                 int((j / count) * 100),
                                                 (datetime.now() - startTime).total_seconds() * 10 ** 3 / 1000),
                file=out, flush=True, end='')
        else:
            print(
                "\r{}[{}{}] {}% {:.01f}s".format(prefix, colored(colors, "█" * x), " " * (size - x), int((j / count) * 100),
                                                 (datetime.now() - startTime).total_seconds() * 10 ** 3 / 1000),
                file=out, flush=True, end='')
        return barSize

    barSize = show(0, barSize)
    for i, item in enumerate(it):
        yield item
        barSize = show(i + 1, barSize)
    print("\n", flush=True, file=out)
