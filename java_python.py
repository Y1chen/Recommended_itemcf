from itemcf import use
import sys
a = []
for i in range(1, len(sys.argv)):
    a.append((str(sys.argv[i])))
result = use(sys.argv[0])
print(result)




