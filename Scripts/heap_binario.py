class BinaryHeap:
    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def right(self, i):
        return ((2 * i) + 2)

    def left(self, i):
        return ((2 * i) + 1)

    def parent(self, i):
        return ((i - 1) // 2)

    def get(self, i):
        return self.items[i]

    def get_max(self):
        if self.size() == 0:
            return None
        return self.items[0]

    def extract_max(self):
        if self.size() == 0:
            return None
        largest = self.get_max()
        self.items[0] = self.items[-1]
        del self.items[-1]
        self.max_heapify(0)
        return largest

    def max_heapify(self, i):
        left = self.left(i)
        right = self.right(i)
        if (left <= self.size() - 1 and self.get(left) > self.get(i)):
            largest = left
        else:
            largest = left
        if (right <= self.size() - 1 and self.get(right) > self.get(largest)):
            largest = right
        if (largest != i):
            self.swap(largest, i)
            self.max_heapify(largest)

    def swap(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def insert(self, key):
        index = self.size()
        self.items.append(key)

        while (index != 0):
            p = self.parent(index)
            if self.get(p) < self.get(index):
                self.swap(p, index)
            index = p


bheap = BinaryHeap()

print('Menu')
print('insert <data>')
print('max get')
print('max extract')
print('quit')

while True:
    do = input('What would you like to do? ').split()

    operation = do[0].strip().lower()
    if operation == 'insert':
        data = int(do[1])
        bheap.insert(data)
    elif operation == 'max':
        suboperation = do[1].strip().lower()
        if suboperation == 'get':
            print('Maximum value: {}'.format(bheap.get_max()))
        elif suboperation == 'extract':
            print('Maximum value removed: {}'.format(bheap.extract_max()))

    elif operation == 'quit':
        break
