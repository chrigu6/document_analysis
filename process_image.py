import sys
from PIL import Image

im = Image.open('Input/Shapes0.png')
im = im.convert('L')
pic = im.load()
result = []
for b in range(0, 800, 100):
    for a in range(0, 1000, 100):
        black = 0
        last = 0
        gradient = 0
        for y in range(b, b+100):
            for x in range(a, a+100):
                if pic[x,y] == 255:
                    #sys.stdout.write('-')
                    last = 255
                else:
                    #sys.stdout.write('*')
                    black += 1
                    if last == 255:
                        gradient+=1
                    elif pic[x+1,y] == 255:
                        gradient+=1
                    else:
                        if pic[x,y+1] == 255 or pic[x,y-1] == 255:
                            gradient+=1
                    last = 0
            #print '\n'
        ratio = float(gradient**2)/float(black)

        #print 'Number of black pixels: ' + str(black)
        #print 'Length of gradient: ' + str(gradient)
        #print 'Ratio: ' + str(ratio)
        if ratio > 14.4 and ratio < 18:
            result.append('triangle')
        elif ratio > 30:
            result.append('star')
        elif ratio < 10:
            result.append('circle')
        else:
            result.append('square')


with open('Input/Shapes0.txt') as f:
    content = f.read().replace(' ', '').splitlines()

correct = 0
for i in range(0, 80):
    if content[i] == result[i]:
        correct += 1

print correct
print 'Recognition Ratio: ' + str(float(correct)/float(80))
