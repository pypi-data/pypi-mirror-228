def dict_to_list(items: dict = None, split: bool = True):
    """
    It takes a dictionary and returns a list of the keys and values

    :param items: The dictionary to be converted
    :type items: dict
    :param split: If True, the function will return a list of two lists, the first being the keys, the second being the
    values, defaults to True
    :type split: bool (optional)
    :return: A list of the keys and a list of the values.
    """
    if items is None:
        return None
    else:
        if split:
            keys_list = []
            items_list = []
            for i in items:
                keys_list.append(i)
                items_list.append(items[i])
            return [keys_list, items_list]
        elif not split:
            items_r = []
            for i in items:
                items_r.append(i)
                items_r.append(items[i])
            return items_r


class Import(dict):

    def to_list(self, split: bool = True):
        """
        It takes a dictionary and returns a list of the dictionary's keys and values

        :param split: If True, the list will be split into two lists, one for the keys and one for the values, defaults to
        True
        :type split: bool (optional)
        :return: A list of the keys and values of the dictionary.
        """
        return dict_to_list(items=self, split=split)
