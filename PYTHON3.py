#Создание бинарной кучи с использованием heapq
import heapq
someNumbers = [8, 3, 5, 1, 6, 2, 4, 7]
heapq.heapify(someNumbers)

#Создание бинарной/биноминальной кучи в виде собственного класса
class BinaryHeap:
    def __init__(self):
        self.heap = []

    def insert(self, key):
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def delete_min(self):
        self.heap.pop()
        self._heapify_down(0)

    def get_min(self):
        if self.is_empty():
            return None
        return self.heap

    def is_empty(self):
        return len(self.heap) == 0

#Создание кучи для печати ряда Фибоначчи до заданного количества элементов
def fibonacci_for_loop(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=' ')
        a, b = b, a + b

#Алгорит для рекурсивного вычисления n-го числа ряда Фибоначчи
def fibonacci(n):
    if n in (1, 2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

#Хеш-таблицы как класс
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return ord(key[0]) % self.size

    def set(self, key, value):
        hash_index = self._hash(key)
        self.table[hash_index] = (key, value)

    def get(self, key):
        hash_index = self._hash(key)
        if self.table[hash_index] is not None:
            return self.table[hash_index][1]
        raise KeyError(f'Key {key} not found')

    def remove(self, key):
        hash_index = self._hash(key)
        if self.table[hash_index] is not None:
            self.table[hash_index] = None
        else:
            raise KeyError(f'Key {key} not found')
        
#Хеш-таблица с собственной реализацией
def hash_function(key):
    hash_code = 0
    for char in key:
        hash_code += ord(char)
    return hash_code % array_size

class HashTable:

    def __init__(self, size):
        self.array_size = size
        self.array = [None] * size

    def put(self, key, value):
        # Insert key-value pair

    def get(self, key):
        # Retrieve value by key

    def remove(self, key):
        # Remove key-value pair

    def hash_function(self, key):
        # Generate hash code

def put(self, key, value):
    index = self.hash_function(key)
    if self.array[index] is None:
        self.array[index] = HashTableEntry(key, value)
    else:
        entry = self.array[index]
        entry.value = value
        entry.key = key

class HashTableEntry:

    def __init__(self, key, value):
        self.key = key
        self.value = value

def get(self, key):
    index = self.hash_function(key)
    if self.array[index] is None:
        raise KeyError()
    entry = self.array[index]
    if entry.key == key:
        return entry.value
    raise KeyError()

def remove(self, key):
    index = self.hash_function(key)
    if self.array[index] is None:
        raise KeyError()
    entry = self.array[index]
    if entry.key == key:
        self.array[index] = None
    else:
        raise KeyError()





