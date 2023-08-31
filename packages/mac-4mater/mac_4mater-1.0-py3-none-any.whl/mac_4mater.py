def mac_4mater(mac: str, delimiter: str = ':', chunk: int = 2, capital: bool = False) -> str:
    """
    Get mac address, correct and return in required format
    DOES NOT CHECK THE INPUT MAC ADDRESS FORMAT, just delete invalid characters and check len = 12
    :param mac: mac address
    :param delimiter: separator character
    :param chunk: the number of characters before the separator output, mast be in [1, 2, 3, 4, 6]. 0 or None for output without delimiter
    :param capital: lowercase or uppercase return output str. default lowercase
    :return: mac address in required format
    """

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield ''.join(lst[i:i + n])

    # str of valid characters
    valid_characters = '0123456789abcdef'
    # converting the string to lowercase
    mac = mac.lower()
    mac_lst = []
    # selecting valid characters from the received data
    for c in mac:
        if c in valid_characters:
            mac_lst.append(c.upper()) if capital else mac_lst.append(c)
    # checking that the mac address is 12 characters long
    if len(mac_lst) != 12:
        raise ValueError(f'Invalid mac address {mac}')
    if chunk in [0, None]:
        return ''.join(mac_lst)
    elif chunk in [1, 2, 3, 4, 6]:
        if type(delimiter) is str:
            return delimiter.join(chunks(mac_lst, chunk))
        else:
            raise ValueError('Delimiter must be str')
    else:
        raise ValueError('Invalid chunk size, must be 1, 2, 3, 4, 6 or 0 , None')


if __name__ == '__main__':

    print(mac_4mater('AB.bc.55.55.55.53', delimiter=':', chunk=2, capital=True))

