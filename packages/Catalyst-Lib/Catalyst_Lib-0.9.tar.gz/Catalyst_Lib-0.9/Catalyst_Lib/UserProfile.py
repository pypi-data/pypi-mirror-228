import datetime
import calendar
import json


def Birthdate(year: int, month: int, day: int):
    return tuple([year, month, day])


class Age:

    def __init__(self, birthdate: tuple):
        now = datetime.datetime.now()
        self.birthdate = birthdate
        self.monthdays = {1: 31,
                          2: 29 if calendar.isleap(now.year) else 28,
                          3: 31,
                          4: 30,
                          5: 31,
                          6: 30,
                          7: 31,
                          8: 31,
                          9: 30,
                          10: 31,
                          11: 30,
                          12: 31}

    def ageFinder(self):
        now = datetime.datetime.now()
        yeardif = now.year - self.birthdate[0]
        if now.month < self.birthdate[1]:
            if now.day < self.birthdate[2]:
                yeardif = yeardif - 1
        return yeardif

    def timeLeft(self):
        now = datetime.datetime.now()
        if now.month > self.birthdate[1]:
            months = (12 - now.month) + self.birthdate[1]
        else:
            months = abs(now.month - self.birthdate[1])
        if now.day > self.birthdate[2]:
            days = ((self.monthdays[now.month]) - now.day) + self.birthdate[2]
        else:
            days = abs(now.day - self.birthdate[2])
        return {
            "months": months,
            "days": days
        }

    def __export__(self):
        return json.dumps({"birthdate": self.birthdate})


class Name:

    def __init__(self, name: str):
        names = name.split(" ")
        for x in range(names.count("")):
            names.remove("")
        self.name = names
        self.nameOriginal = name

    def __str__(self):
        newname = ""
        for name in self.name:
            if len(self.name) - 1 == self.name.index(name):
                newname = newname + name
            else:
                newname = newname + name + " "
        return newname

    def capitalize(self):
        for x in self.name:
            self.name[self.name.index(x)] = x.capitalize()

    def __export__(self):
        return json.dumps({"name": self.nameOriginal})


class user:

    def __init__(self, name: str, age: int):
        if name is not None:
            self.name = name
        else:
            self.name = None
        if age is not None:
            self.age = age
        else:
            self.age = None
