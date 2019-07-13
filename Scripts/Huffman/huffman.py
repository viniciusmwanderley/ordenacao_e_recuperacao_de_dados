from collections import Counter

''' EQUAL: READ AND COUNT FREQUENCY -> WORKING '''
equal = open("generated.equal", mode='r', encoding='latin1').read()
# print(equal)
print(Counter(equal))

print("********************************************************************************************************************************************")

''' FIB25: READ AND COUNT FREQUENCY -> WORKING '''
fib25 = open("generated.fib25", encoding='latin1', newline='\n').read()
# print(fib25)
print(Counter(fib25))

''' TEST: WRITE BYTE '''
# f = open("teste.bin", "wb")
# f.write(bytearray((0, 0, 255, 255, 128, 128)))
# f.close()
# print(open("teste.bin", encoding="latin1").read())
