import sys
from PIL import Image

im = Image.open('Input/Shapes0.png')
im = im.convert('L')
b = im.load()
for a in range(0, 1000, 100):
    black = 0
    last = 0
    gradient = 0
    for y in range(0, 100):
        for x in range(a, a+100):
            if b[x,y] == 255:
                #sys.stdout.write('-')
                last = 255
            else:
                #sys.stdout.write('*')
                black += 1
                if last == 255:
                    gradient+=1
                elif b[x,y+1] == 255:
                    gradient+=1
                last = 0
        #print '\n'

    print 'Number of black pixels: ' + str(black)
    print 'Length of gradient: ' + str(gradient)
    print 'Ratio: ' + str(float(gradient)/float(black))
