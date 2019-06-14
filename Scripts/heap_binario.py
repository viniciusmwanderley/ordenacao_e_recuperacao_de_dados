
class BinaryHeap:
    def __init__(self):
        # self.items = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
        # self.items = [10, 6, 9, 2, 1, 8, 3]
        self.items = [10, 6, 8, 2, 1, 9, 3]

    def size(self):
        return len(self.items)

    def right(self, i):
        return ((2 * i) + 2)

    def left(self, i):
        return ((2 * i) + 1)
        '''
        try:
            if ((2 * i) + 1) < self.size() and i >= 0:
                return ((2 * i) + 1)
            else:
                raise Exception()
                return None
        except Exception:
            print('error with left')
        else:
            print('left OK')
        '''

    def parent(self, i):
        return ((i - 1) // 2)

    def get(self, i):
        return self.items[i]

    def swap(self, i, j):
        try:
            if int(self.items[i]) and int(self.items[j]):
                self.items[i], self.items[j] = self.items[j], self.items[i]
            else:
                raise Exception('error')
        except Exception:
            print('error with swap')

    def is_leaf(self, index):
        if (index >= self.size() // 2) and (index <= self.size() - 1):
            return True
        return False

    def max_heapify(self, index):
        left = self.left(index)
        right = self.right(index)
        # print('right:', right, 'left:', left)

        if ((left < self.size()) and ((self.get(left) > self.get(index)))):
            largest = left
        else:
            largest = index
        if ((right < self.size()) and ((self.get(right) > self.get(largest)))):
            largest = right
        # print('index:', index, 'left:', left, 'right:', right, 'largest:', largest)
        if (largest != index):
            # print('large ', largest, 'indice max heapify', index)
            # print('heap before swap:', self.items)
            self.swap(index, largest)
            # print('heap after swap:', self.items)
            self.max_heapify(largest)

    def build_max_heap(self):
        indice = ((self.size() - 1) // 2)
        # print('indice build before while max heap', indice)
        while(indice >= 0):
            self.max_heapify(indice)
            indice = indice - 1


bheap = BinaryHeap()

print('Menu')
print('insert <data>')
print('max get')
print('max extract')
print('build')
print('print')
print('size')
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
    elif operation == 'build':
        print('before build:', bheap.items)
        bheap.build_max_heap()
        print('after build', bheap.items)
    elif operation == 'parent':
        data = int(do[1])
        print(bheap.parent(data))
    elif operation == 'right':
        data = int(do[1])
        print(bheap.right(data))
    elif operation == 'left':
        data = int(do[1])
        print(bheap.left(data))
    elif operation == 'print':
        print(bheap.items)
    elif operation == 'size':
        print(bheap.size())
    elif operation == 'quit':
        break
