
a = [2, 5, 3, 0, 2, 3, 0, 3]
b = [0, 0, 0, 0, 0, 0, 0, 0]
tam_c = max(a)
c = [0] * (tam_c + 1)

for i in range(len(a)):
    c[a[i]] = c[a[i]] + 1


for i in range(len(c) - 1):
    c[i + 1] += c[i]

print(c)
for i in range((len(a) - 1), -1, -1):

    b[c[a[i]] - 1] = a[i]
    c[a[i]] -= 1
print(b)
