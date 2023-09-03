"─│┌┐└┘├┤┬┼┴═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬"
from .lists import contains_duplicates

"""
print("┌────────────────────────────────────┐")
print("│                                    │")
print("└────────────────────────────────────┘")
print("")
print("╔════════════════════════════════════╗")
print("╠════════════════════════════════════╣")
print("╚════════════════════════════════════╝")
"""


class Table:

    def __init__(self, items: list):
        for item in items:
            if type(item) != dict:
                raise ValueError(f"Items in list must be dict\n{item}")
        self.items = items

    def append(self, item: dict):
        self.items.append(item)

    def display(self):
        vitems = self.items
        items = self.items[0]
        top = "╔"
        bottom = "╚"
        lengths = {}
        middle = "╠"
        for x in items:
            length = 0
            for y in self.items:
                length = len(self.items[self.items.index(y)][x]) if len(
                    self.items[self.items.index(y)][x]) > length else length
                length = len(x) if len(x) > length else length
            lengths[x] = length
            top = top + ("═" * (length + 2)) + ("╦" if list(items.keys()).index(x) < (len(items) - 1) else "")
            bottom = bottom + ("═" * (length + 2)) + ("╩" if list(items.keys()).index(x) < (len(items) - 1) else "")
            middle = middle + ("═" * (length + 2)) + ("╬" if list(items.keys()).index(x) < (len(items) - 1) else "")
        top = top + "╗"
        bottom = bottom + "╝"
        middle = middle + "╣"
        runs = 0
        mainstring = ""
        contains_dups = contains_duplicates(self.items)
        header = "║ "
        for item in items.keys():
            length = lengths[item]
            vitem = item
            difference = int(length - len(vitem))
            if difference == 0:
                if list(items.keys()).index(item) < (len(items) - 1):
                    header = header + vitem + " ║ "
                else:
                    header = header + vitem + " ║"
            elif difference % 2 == 0:
                vitem = f"{' ' * int(difference / 2)}{vitem}{' ' * int(difference / 2)}"
                if list(items.keys()).index(item) < (len(items) - 1):
                    header = header + vitem + " ║ "
                else:
                    header = header + vitem + " ║"
            elif difference % 2 != 0:
                difference = difference + 1
                vitem = f"{' ' * int(difference / 2)}{vitem}{' ' * (int(difference / 2) - 1)}"
                if list(items.keys()).index(item) < (len(items) - 1):
                    header = header + vitem + " ║ "
                else:
                    header = header + vitem + " ║"
        header = header + "\n" + middle
        for items in self.items:
            string = "║ "
            for item in items:
                length = lengths[item]
                vitem = items[item]
                difference = int(length - len(vitem))
                if difference == 0:
                    if list(items.keys()).index(item) < (len(items) - 1):
                        string = string + vitem + " ║ "
                    else:
                        string = string + vitem + " ║"
                elif difference % 2 == 0:
                    vitem = f"{' ' * int(difference / 2)}{vitem}{' ' * int(difference / 2)}"
                    if list(items.keys()).index(item) < (len(items) - 1):
                        string = string + vitem + " ║ "
                    else:
                        string = string + vitem + " ║"
                elif difference % 2 != 0:
                    difference = difference + 1
                    vitem = f"{' ' * int(difference / 2)}{vitem}{' ' * (int(difference / 2) - 1)}"
                    if list(items.keys()).index(item) < (len(items) - 1):
                        string = string + vitem + " ║ "
                    else:
                        string = string + vitem + " ║"
            if contains_dups:
                mainstring = (mainstring + string + (
                    "\n" if (vitems.index(items) + runs) < (len(self.items) - 1) else "")) if (vitems.index(
                    items) + runs) < (len(self.items)) else mainstring
                mainstring = (mainstring + middle + (
                    "\n" if (vitems.index(items) + runs) < (len(self.items)) else "")) if (vitems.index(
                    items) + runs) < (len(self.items) - 1) else mainstring
                runs = runs + 1
            else:
                mainstring = (mainstring + string + (
                    "\n" if self.items.index(items) < (len(self.items) - 1) else "")) if self.items.index(
                    items) < (len(self.items)) else mainstring
                mainstring = (mainstring + middle + (
                    "\n" if self.items.index(items) < (len(self.items)) else "")) if self.items.index(
                    items) < (len(self.items) - 1) else mainstring
        print(
            f"""{top}
{header}
{mainstring}
{bottom}"""
        )
