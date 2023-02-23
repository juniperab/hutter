from collections import Counter, deque, namedtuple
from itertools import islice

HuffData = namedtuple('HuffData', ['symb_tree', 'rev_symb_tree', 'longest_code', 'sz'])


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


class Huff:
    def __init__(self, seq, sz=1):
        self.__proc(seq, sz)

    def __proc(self, seq, sz):
        if type(seq) == str:
            seq = seq.encode('utf8')
        if type(seq) != bytes:
            raise ValueError('can only process bytes or str')

        self.__sz = sz
        self.__symb_counter = Counter((bytes(c) for c in chunk(seq, sz)))
        symb_tree, rev_symb_tree = self.__symb_tree()
        # N.B., data values should be immutable
        self.__data = HuffData(
            symb_tree=symb_tree,
            rev_symb_tree=rev_symb_tree,
            longest_code=sorted(rev_symb_tree.values(), reverse=True, key=lambda el: len(el))[0],
            sz=sz,
        )

    def __repr__(self):
        return f"Huff(symbs: {len(self.__data.rev_symb_tree)})"

    def __str__(self):
        return repr(self)

    def __symb_tree(self):
        tree = deque((c, (None, s)) for s, c in self.__symb_counter.items())
        while len(tree) > 1:
            a = tree.popleft()
            b = tree.popleft()
            ab = (a[0] + b[0], (a[1], b[1]))
            insert_at = len(tree)
            for i in range(len(tree)):
                if tree[i][0] >= ab[0]:
                    insert_at = i
                    break
            tree.insert(insert_at, ab)
        tree = tree[0][1]

        rev_tree = {}

        def populate_rev_tree(tree, rev_tree, path):
            if tree[0] is None:
                rev_tree[tree[1]] = path
                return
            populate_rev_tree(tree[0], rev_tree, path + '0')
            populate_rev_tree(tree[1], rev_tree, path + '1')

        populate_rev_tree(tree, rev_tree, '')
        return tree, rev_tree

    def data(self):
        return self.__data

    def __encode_bin(self, seq, b=8):
        acc = deque()
        block = deque()
        for symb in seq:
            acc.extend(self.__data.rev_symb_tree[symb])
            if len(acc) >= b:
                for i in range(b):
                    block.append(acc.pop())
                yield ''.join(block)
                block.clear()
        if len(acc) > 0:
            acc.extend(self.__data.longest_code[:-1])
            if len(acc) < b:
                raise ValueError("cannot terminate encoded sequence")
            for i in range(b):
                block.append(acc.pop())
            yield ''.join(block)
            block.clear()

    def __encode_hex(self, seq, b=2):
        for bblock in self.__encode_bin(seq, b=b * 4):
            n = int(bblock, 2)
            hblock = ('{:0%dx}' % b).format(n)
            yield from hblock

    def encode(self, seq):
        if type(seq) == str:
            seq = seq.encode('utf8')
        if type(seq) != bytes:
            raise ValueError('can only encode bytes or str')
        chunks = (bytes(c) for c in chunk(seq, self.__sz))
        return bytes((int(ch, 2) for ch in self.__encode_bin(chunks, b=8)))
