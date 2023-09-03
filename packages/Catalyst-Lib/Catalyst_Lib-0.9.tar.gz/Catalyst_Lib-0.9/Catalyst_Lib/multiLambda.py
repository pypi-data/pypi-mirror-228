class multiLambda:
    function_list = []
    example_list_items = [abs, (1, 2)]
    variables = {}
    is_empty = True

    def setvar(self, name: any, value: any):
        """
        It sets the value of a variable.

        :param name: The name of the variable
        :type name: any
        :param value: The value to set the variable to
        :type value: any
        """
        self.variables[name] = value

    def getvar(self, name: any):
        """
        It returns the value of the variable with the name 'name' from the dictionary 'variables'

        :param name: The name of the variable
        :type name: any
        :return: The value of the variable.
        """
        return self.variables[name]

    def printvar(self, name: any, printtype: any = print):
        """
        `printvar` is a function that takes in two arguments, `self` and `name`, and prints the value of the variable `name`
        in the `self` object

        :param name: The name of the variable you want to print
        :type name: any
        :param printtype: The function to use to print the variable
        :type printtype: any
        """
        printtype(self.variables[name])

    def execute(self):
        """
        It takes a list of functions and their arguments, and executes them in order
        """
        responces = []
        for i in self.function_list:
            responces.append(i[0](*i[1]))

    def getvars(self):
        """
        It returns the variables of the class
        :return: The variables are being returned.
        """
        return self.variables

    def __init__(self, functions: list):
        """
        It takes a list of functions and their parameters, and then it adds them to the function list

        :param functions: list
        :type functions: list
        """
        if not isinstance(functions, list):
            raise ValueError("Parameter for creations of a function must be a list")
        for x in range(len(functions)):
            if type(functions[x][0]) not in [type(lambda: print()), type(print)]:
                raise ValueError(
                    f"All elements of parameter list must be a function or built in function. Found {type(x)}")
            else:
                if not isinstance(functions[x][1], tuple):
                    raise ValueError(str(type(functions[x][1])))
                newtuple = list(functions[x][1])
                for y in range(len(newtuple)):
                    if newtuple[y] == "$self":
                        newtuple[y] = self
                newtuple = tuple(newtuple)
                self.function_list.append([functions[x][0], newtuple])
                self.is_empty = False

    def get_keys(self):
        """
        It returns the list of keys in the dictionary.
        :return: The function_list is being returned.
        """
        return self.function_list

    def add_key(self, function: list):
        """
        It adds a function to the function list

        :param function: list
        :type function: list
        :return: A list of lists.
        """
        try:
            if function[1][0] == "$self":
                function[1][0] = self
            self.function_list.append([function[0], function[1]])
            return True
        except Exception as e:
            print(e.with_traceback())
            return False

    def remove_key(self, function: list):
        """
        It removes a function from the function list

        :param function: list
        :type function: list
        :return: The function is being returned.
        """
        try:
            if function in self.function_list:
                item = self.function_list.remove(function)
                if len(self.function_list) == 0:
                    self.is_empty = True
                return item
            return False
        except Exception as e:
            print(e.with_traceback())
            return False

    def remove_all_keys(self, function: list):
        """
        It removes all the keys in the list that are equal to the function

        :param function: list
        :type function: list
        :return: True
        """
        while function in self.function_list:
            if function in self.function_list:
                self.function_list.remove(function)
        return True

    def clear_keys(self):
        """
        This function clears the list of functions and sets the is_empty flag to True
        :return: True
        """
        self.function_list = []
        self.is_empty = True
        return True

    def vars(self, var):
        """
        It returns the value of the variable 'var' in the dictionary 'variables'

        :param var: The variable to be returned
        :return: The value of the variable.
        """
        return self.variables[var]


def builder(*functions) -> multiLambda:
    """
    It takes a list of functions and returns a multiLambda object with those functions as keys
    :return: A multiLambda object with the functions added to it.
    """
    instance = multiLambda([])
    for x in functions:
        instance.add_key(x)
    return instance


def Parameter(*args) -> list:
    """
    It takes in any number of arguments and returns a list of those arguments
    :return: A list of the parameters
    """
    return [param for param in args]


def Function(function, params: list = None) -> list:
    """
    "Function takes a function and a list of parameters and returns a list of the function and the parameters."

    The first line of the function is a docstring. It's a string that describes what the function does. It's not necessary,
    but it's good practice to include one

    :param function: The function to be called
    :param params: list = None
    :type params: list
    :return: A list with the function and the parameters.
    """
    if params is None:
        params = []
    return [function, params]

