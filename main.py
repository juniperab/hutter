#!/usr/bin/env python3

from hutter import *
import pprint

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    p, w = read_data(1000)
    h = Huff(w, 1)
    we = h.encode(w)

    pp = pprint.PrettyPrinter()
    pp.pprint('Symbol Tree:')
    pp.pprint(h.data().symb_tree)
    pp.pprint('\nReverse Symbol Tree:')
    pp.pprint(h.data().rev_symb_tree)
    pp.pprint(f"\nEncoded Data ({len(we)} bytes):")
    pp.pprint(we)
