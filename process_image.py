import sys
from PIL import Image

im = Image.open('Input/Shapes0.png')
im = im.convert('L')
pic = im.load()
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
            print 'triangle'
        elif ratio > 30:
            print 'star'
        elif ratio < 10:
            print 'circle'
        else:
            print 'cube'
