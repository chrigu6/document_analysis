import math
from PIL import Image
from ConfusionMatrix import ConfusioinMatrix

im = Image.open('Input/Shapes1.png')
im = im.convert('L')
pic = im.load()
result = []
for a in range(0, 800, 100):
    for b in range(0, 1000, 100):
        k = b
        l = a
        m = b+100
        n = a+100
        found = False
        black = 0
        while(k < m and l < n and not found):
            for i in range(l,n):
                if pic[k,i] == 0:
                    outerPoint = (k-b,i-a)
                    found = True
                    break
            k+=1

            for i in range(k,m):
                if pic[i,n-1] == 0 and not found:
                    outerPoint = (i-b,n-1-a)
                    found = True
                    break
            n-=1

            if k < m:
                for i in range(n-1, l-1, -1):
                    if pic[m-1,i] == 0 and not found:
                        outerPoint = (m-1-b,i-a)
                        found = True
                        break
                m-=1

            if l < n:
                for i in range(m-1, k-1, -1):
                    if pic[i,l] == 0 and not found:
                        outerPoint = (i-b,l-a)
                        found = True
                        break
                l+=1

        for y in range(a, a+100):
            for x in range(b, b+100):
                if pic[x,y] == 0:
                    black+=1

        radius = math.sqrt(float(abs(outerPoint[0]-50)**2 +
                            abs(outerPoint[1] -50)**2)
                        )

        area = (radius**2) * math.pi
        ratio = (float(black)/float(area))
        #print ratio

        if ratio < 0.43:
            result.append('star')
        elif ratio < 0.6 and ratio > 0.43:
            result.append('triangle')
        elif ratio < 0.95 and ratio > 0.6:
            result.append('square')
        elif ratio > 0.95:
            result.append('circle')


with open('Input/Shapes1.txt') as f:
    content = f.read().replace(' ', '').splitlines()

matrix = ConfusioinMatrix()

correct = 0
for i in range(0, 80):
    matrix.addResult([content[i],result[i]])
    if content[i] == result[i]:
        correct += 1
    else:
        print(content[i], result[i])

print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
print 'Confusion-Matrix:\n'
print matrix
