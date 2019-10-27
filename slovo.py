import time
import functools


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        call = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        print(f'[{elapsed:0.8f}s] {func.__name__}')
        return result

    return clocked


height = 0


class Node:
    def __init__(self, symbol, is_end=False):
        self.leafs = {}
        self.symbol = symbol
        self.word = ''
        self.is_end = is_end

    def __str__(self):
        return f'Node {self.symbol}, is_end {self.is_end}'

    def __repr__(self):
        return f'Node({self.symbol, self.is_end})'


def insert(node, word, pre=''):
    for i, char in enumerate(word):
        if char not in node.leafs:
            node.leafs[char] = Node(char)
        node = node.leafs[char]
    node.is_end = True
    node.word = pre + word


class Trie:
    @clock
    def __init__(self, words):
        self.leafs = {}
        for word in words:
            self.insert_word(word)

    def insert_word(self, word):
        char = word[0]
        if char not in self.leafs:
            self.leafs[char] = Node(char)
        node = self.leafs[char]
        insert(node, word[1:], word[0])


def transform_into_matrix(table):
    table = [c for c in table if c in alphabet]
    if len(table) != 5 * 5:
        raise ValueError('Invalid field')
    result = [table[start * 5:(start + 1) * 5] for start in range(5)]
    return result


@clock
def findall(table, dictionary):
    n = len(table[0])
    result = set()

    def find_all_ways(i, j):
        ways = []
        n = len(table[0]) - 1
        if i != 0 and j != 0:
            ways.append((-1, -1))
        if i < n and j < n:
            ways.append((1, 1))
        if i != 0 and j < n:
            ways.append((-1, 1))
        if i < n and j != 0:
            ways.append((1, -1))
        if i != 0:
            ways.append((-1, 0))
        if i < n:
            ways.append((1, 0))
        if j != 0:
            ways.append((0, -1))
        if j < n:
            ways.append((0, 1))
        return ways

    def dfs(i, j, ways, node, path):
        if node.is_end:
            result.add(node.word)
        next_chars = dict()
        for di, dj in ways:
            next_chars[(di, dj)] = table[i + di][j + dj]
        for dcoor, next_char in next_chars.items():
            if next_char in node.leafs:
                fi, fj = dcoor
                if (i + fi, j + fj) in path:
                    continue
                ways = find_all_ways(i + fi, j + fj)
                ways.remove((-fi, -fj))
                dfs(i + fi, j + fj, ways, node.leafs[next_char], path + ((i + fi, j + fj),))

    for i in range(n):
        for j in range(n):
            begin_char = table[i][j]
            ways = find_all_ways(i, j)
            if begin_char in dictionary.leafs:
                dfs(i, j, ways, dictionary.leafs[begin_char], ((i, j),))
    return result


alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


@clock
def read_words(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        result = []
        for line in file.readlines():
            word = line.rstrip().replace('ё', 'е')
            result.append(word)
        return result


# table='пги1т4ениофо2олт3силуоглтисро'
# крдкакюоаярдвжмревтиеснкс
words = sorted(list(set(read_words('words_erudit.txt') +
                        read_words('word_rus.txt') +
                        read_words('zdf.txt'))))

dictionary = Trie(words)
# table = input("Ваше поле: ")
table = 'е4хрлил3оилтлбзфии1ресшопов2т'
table = transform_into_matrix(table)
for row in table:
    print(*row, sep=' ')
result = findall(table, dictionary)
result = list(result)
result.sort(key=len, reverse=False)
print("Слов найдено:", len(result))
import random

# random.shuffle(result)
print(*result, sep='\n')
