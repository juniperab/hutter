from hutter.huffman.huffman import Huff


def read_data(length=100):
    """
    Read some information from data files
    :param length:  the quantity of data to read from each file
    :return:        a tuple of data objects
    """
    with open('data/pi-billion.txt', 'r') as f:
        p = f.read(length + 2)
    with open('data/enwik9', 'r') as f:
        w = f.read(length)
    return p[2:], w
