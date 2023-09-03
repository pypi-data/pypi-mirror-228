from typing import Callable
from random import choice
from .lib import split

class Generator:

    def __init__(self, length: int = 25, nums: list = None):
        """
        This function takes in two arguments, length and nums, and sets the length and nums attributes of the object to the
        values of the arguments

        :param length: The length of the items, defaults to 25
        :type length: int (optional)
        :param nums: The list of numbers that will be used to generate the items
        :type nums: list
        """
        self.length = length
        self.nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] if nums is None else nums

    def lorem(self, length: int = -1):
        """
        `lorem` is a function that takes in a length and returns a string of lorem ipsum text

        :param length: The length of the text to be generated
        :type length: int
        """
        text = ""
        for i in range(0, self.length if length == -1 else length):
            word = choice(loremWordList)
            text = f"{text} {word}"

    def Str(self, length: int = -1, capitalized: bool = False, special: bool = False):
        """
        It generates a random string of characters

        :param length: The length of the string
        :type length: int
        :param capitalized: If True, the string will be capitalized, defaults to False
        :type capitalized: bool (optional)
        :param special: If True, the string will contain special characters, defaults to False
        :type special: bool (optional)
        :return: A string of random characters.
        """
        chars = "qwertyuiopasdfghjklzxcvbnm"
        if capitalized:
            chars = chars.upper()
        if special:
            chars = chars + "`~!@#$%^&*()_-+={[}]|:;'<,>.?/'" + '"'
        chars = split(chars)
        text = ""
        for i in range(0, self.length if length == -1 else length):
            char = choice(chars)
            text = f"{text}{char}"
        return text

    def Int(self, length: int = -1):
        """
        It returns a random integer of a specified length

        :param length: The length of the number you want to generate
        :type length: int
        :return: A random number of length self.length
        """
        nums = self.nums
        number = ""
        for i in range(0, self.length if length == -1 else length):
            num = choice(nums)
            number = f"{number}{num}"
        return int(number)

    def Dict(self, length: int = -1, internalValueParameters: tuple = (), internalValueFunction: object = Str):
        """
        It creates a dictionary with the length of the parameter length. If length is not specified, it will use the length
        of the object.

        :param length: The length of the list
        :type length: int
        :param internalValueParameters: This is a tuple of parameters that will be passed to the internalValueFunction
        :type internalValueParameters: tuple
        :param internalValueFunction: The function that will be used to generate the values of the dictionary
        :type internalValueFunction: object
        :return: A dictionary with the keys being the index of the item in the dictionary and the values being the result of
        the internalValueFunction.
        """
        Dict = {}
        for i in range(0, self.length if length == -1 else length):
            item = internalValueFunction(*internalValueParameters)
            Dict[i] = item
        return Dict

    def List(self, length: int = -1, internalItemParameters: list = [], internalDataFunction: Callable = "Default"):
        """
        It creates a list of a specified length, and fills it with a specified type of data

        :param length: The length of the list
        :type length: int
        :param internalItemParameters: list = []
        :type internalItemParameters: list
        :param internalDataFunction: This is the function that will be called to generate the data for each item in the
        list, defaults to Default
        :type internalDataFunction: Callable (optional)
        :return: A list of strings.
        """
        List = []
        if internalDataFunction == "Default":
            for i in range(0, self.length if length == -1 else length):
                item = self.Str(*internalItemParameters)
                List.append(item)
        else:
            for i in range(0, self.length if length == -1 else length):
                item = internalDataFunction(*internalItemParameters)
                List.append(item)
        return List

    def Bool(self):
        """
        It returns a random boolean value.
        :return: A random choice of either False or True.
        """
        return choice([False, True])

    def Type(self, special: bool = False):
        """
        It returns a random type from a list of types

        :param special: If True, then the function will return a type that is not a basic type, defaults to False
        :type special: bool (optional)
        :return: A random type from the list of types.
        """
        if not special:
            types = [str, int, float, list, dict, any]
        else:
            types = [str, int, float, list, dict, any, bool, tuple]
        return choice(types)

    def Tuple(self, length: int = -1, internalItemParameters: tuple = (), internalDataFunction: Callable = Str):
        """
        `Tuple` is a function that returns a tuple of `List`s of `Str`s

        :param length: The length of the tuple. If -1, then the length is infinite
        :type length: int
        :param internalItemParameters: This is a tuple of parameters that will be passed to the internalDataFunction
        :type internalItemParameters: tuple
        :param internalDataFunction: This is the function that will be used to generate the data for each item in the list
        :type internalDataFunction: Callable
        :return: A list of tuples.
        """
        return tuple(self.List(length=length, internalItemParameters=internalItemParameters,
                               internalDataFunction=internalDataFunction))

    def Float(self, length: int = -1):
        """
        It takes a length, and returns a float with that length

        :param length: The length of the number
        :type length: int
        :return: A float value
        """
        nums = self.nums
        if length == -1:
            length = self.length
        frontDecimal = round(length * .20)
        valFrontDecimal = ""
        for i in range(0, frontDecimal):
            valFrontDecimal = valFrontDecimal + str(choice(nums))
        valBackDecimal = ""
        for x in range(0, length - frontDecimal):
            valBackDecimal = valBackDecimal + str(choice(nums))
        num = f"{valFrontDecimal}.{valBackDecimal}"
        return float(num)

    def Random(self):
        """
        It chooses a random function from a list of functions and returns the result of that function
        :return: A function is being returned.
        """
        function = choice([self.Int, self.Str, self.Dict, self.List, self.Bool, self.Type, self.Tuple, self.Float])
        return function()

    def __int__(self, length: int = -1):
        """
        This function returns an integer value of the specified length

        :param length: The length of the string to be generated
        :type length: int
        :return: The class Int is being returned.
        """
        return self.Int(length=length)

    def __str__(self, length: int = -1):
        """
        The function takes in a length parameter, and if the length is -1, it returns the entire string. Otherwise, it
        returns the first length characters of the string

        :param length: The length of the string to return. If -1, returns the entire string
        :type length: int
        :return: The string representation of the object.
        """
        return self.Str(length=length)

    def __float__(self, length: int = -1):
        """
        This function returns a float value from the current position in the buffer

        :param length: The length of the string to be returned
        :type length: int
        :return: A float object
        """
        return self.Float(length=length)

    def __bool__(self):
        """
        If the object is not None, then it is True
        :return: The value of the boolean expression.
        """
        return self.Bool()
