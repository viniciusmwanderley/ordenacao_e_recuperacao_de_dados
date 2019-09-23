import random


class Quick(object):
    def particao(self, a, ini, fim):
        pivo = a[fim - 1]
        start = ini
        end = ini
        for i in range(ini, fim):
            if a[i] > pivo:
                end += 1
            else:
                end += 1
                start += 1
                a[i], a[start - 1] = a[start - 1], a[i]
        return start - 1

    def quickSort(self, a, ini, fim):
        if ini < fim:
            pp = self.randparticao(a, ini, fim)
            self.quickSort(a, ini, pp)
            self.quickSort(a, pp + 1, fim)
        return a

    def randparticao(self, a, ini, fim):
        rand = random.randrange(ini, fim)
        a[rand], a[fim - 1] = a[fim - 1], a[rand]
        return self.particao(a, ini, fim)


a = [8, 5, 12, 55, 3, 7, 82, 44, 35, 25, 41, 29, 17]
print(a)
q = Quick()
print(q.quickSort(a, 0, len(a)))
