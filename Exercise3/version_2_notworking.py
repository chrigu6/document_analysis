import os
import Image
import operator
from copy import deepcopy

def horizontalSmearing(image, limit, stretch):
    pic = image.load()
    white = 0
    for y in range(0, image.size[1]):
        white = 0
        for x in range(0, image.size[0]):
            if pic[x,y] == 255:
                white += 1
            elif pic[x,y] == 0 or x == image.size[0]:
                if white >= limit and white < stretch:
                    for i in range(x, x-white-1, -1):
                        pic[i,y] = 0
                white = 0
    return image

def whitePerColumn(img):
    pic = img.load()
    
    whitePerColumn = []
    
    for x in range(0, img.size[0]):
        i = 0
        for y in range(0, img.size[1]):
            if pic[x,y] == 255:
                i += 1
        whitePerColumn.append(i)
    
    connectedWhiteColumns = []
    i = 0
    while i < len(whitePerColumn)-1:
        if whitePerColumn[i] == img.size[1]:
            j = i+1
            while whitePerColumn[j] == img.size[1]:
                j += 1
                if j == len(whitePerColumn)-1:
                    break
            connectedWhiteColumns.append([i,j-i])
            i = j-1
        i = i+1
                    
            
    return connectedWhiteColumns 


def connectedComponents(image):
    components = []
    pic = image.load()
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            if pic[x,y] == 0:
                #Check if pixel allready belongs to a component, ignore pixel on the border of the image
                if not checkRange(components,x,y):
                    #If the pixel doesn't belong to a component, create and add a new component
                    components.append(getComponent(image,x,y))
    removeNested(components)
                    
    return components


def isBorderPixel(image, x, y):
    return x == 0 or y == 0 or x == image.size[0] or y == image.size[1]

def isElement(size,pic,p):
    if p[0] >= 0 and p[0] < size[0] and p[1] >= 0 and p[1] < size[1]:
        return pic[p[0],p[1]] == 0
    else:
        return False
    
            

def isBorderElement(image, pic, x, y):
    for i in range(x-1,x+2):
        for j in range(y-1,-y+2):
            if i >= 0 and i < image.size[0] and j >= 0 and j < image.size[1]:
                if pic[i,j] == 255:
                    return True
    
    return False
            


def getComponent(image,x,y):
    pic = image.load()
    component = Component()
    component.update(x,y)
    p0X = x
    p0Y = y
    d =  0
    pX = x
    pY = y
    rotated = 0
    
    
    i = 0
    while (True):
        i+=1
        #Inspired by: http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/theo.html
        #Move one square towards d and one to the left
        p1 = getStepfromDirection((d+1)%8, pX, pY)
        if isElement(image.size, pic, p1) :
            component.update(p1[0],p1[1])
            pX = p1[0]
            pY = p1[1]
            d = (d + 2) % 8
            rotated = 0
        else :
            #Move one square towards d
            p2 = getStepfromDirection(d, pX, pY)
            if isElement(image.size, pic, p2) :
                component.update(p2[0],p2[1])
                pX = p2[0]
                pY = p2[1]
                rotated = 0
            
            else:
                #Move one square towards d and one to the right
                p3 = getStepfromDirection((d+7)%8, pX, pY)
                if isElement(image.size, pic, p3) :
                    component.update(p3[0],p3[1])
                    pX = p3[0]
                    pY = p3[1]
                    rotated = 0
                
                else:
                    #If you rotated three time, the pixel is isolated
                    if rotated > 3:
                        return component
                    else:
                        #if all the pixel towards d, left and right of d are not black rotate 90 degrees to the right
                        d = (d+6)%8
                        rotated = rotated + 1
        
        if p0X == pX and p0Y == pY and rotated == 0:
            return component
                
def getStepfromDirection(d,x,y):
    if d == 0:
        return [x+1,y]
    if d == 1:
        return [x+1,y-1]
    if d == 2:
        return [x,y-1]
    if d == 3:
        return [x-1,y-1]
    if d == 4:
        return [x-1,y]
    if d == 5:
        return [x-1,y+1]
    if d == 6:
        return [x,y+1]
    if d == 7:
        return [x+1,y+1]
    
    return "Fail"
               
def checkRange(components, x, y):
    for c in components:
        if(c.isinRange(x,y)):
            return True
    
    return False

def removeNested(components):
    for checkedComponent in components:
        for otherComponent in components:
            if otherComponent.componentInRange(checkedComponent) and not otherComponent.isEqual(checkedComponent):
                components.remove(checkedComponent)
                break

def drawBorder(components, image):
    
    rgb_img = image.convert('RGB')
    pic = rgb_img.load()

    for c in components:
        for x in range(c.minX,c.maxX):
            pic[x,c.minY] = (0,0,255)
            pic[x,c.maxY] = (0,0,255)
        
        for y in range(c.minY,c.maxY):
            pic[c.minX,y] = (0,0,255)
            pic[c.maxX,y] = (0,0,255)
    
    return rgb_img
            

class Component:
    
    points = []
    
    minX = 999999999
    maxX = 0
    minY = 999999999
    maxY = 0
    
    def update(self, x, y):
        self.points.append([x,y])
        
        if x < self.minX:
            self.minX = x
            
        if x > self.maxX:
            self.maxX = x
            
        if y < self.minY:
            self.minY = y
            
        if y > self.maxY:
            self.maxY = y
            
    def isinRange(self,x,y):
        return x >= self.minX and x <= self.maxX and y >= self.minY and y <= self.maxY
    
    def componentInRange(self,c):
        return c.minX >= self.minX and c.maxX <= self.maxX and c.minY >= self.minY and c.maxY <= self.maxY 
    
    def isEqual(self, c):
        return self.minX == c.minX and self.maxX == c.maxX and self.minY == c.minY and self.maxY == c.maxY
    
    def enlarge(self, i, length, hight):
        self.minX = max(0,self.minX - i) 
        self.minY = max(0,self.minY - i)
        self.maxX = min(length,self.maxX + i)
        self.maxY = min(hight, self.maxY + i)


def getMean(whitePerColumn):
    whitePerColumn.sort(key=operator.itemgetter(1))
    mean =  whitePerColumn[len(whitePerColumn)/2][1]
    whitePerColumn.sort(key=operator.itemgetter(0))
    return 5


def drawImage(img, start, end):
    result  = Image.new('L', (end-start,img.size[1]))
    pic1 = result.load()
    pic2 = img.load()
    
    for y in range(0,img.size[1]):
        for x in range(start,end):
            pic1[x-start,y] = pic2[x,y]
            
    result.save("Output/result.png")
    
    return result
            


def split(original, mean, whitePerColumn, fn):
    j = 0
    splitValues = []
    im = original.convert("L")
    for whitespace in whitePerColumn:
        if whitespace[1] >= mean:
            splitValues.append(whitespace)
    
    if len(splitValues)>0:
        if splitValues[0][0] == 0:
            img = drawImage(im, splitValues[0][1],splitValues[1][0])
            img.save('Output/'+str(j)+fn)
            j+=1
        else:
            img = drawImage(im, 0,splitValues[0][0])
            img.save('Output/'+str(j)+fn)
            j+=1
        
    
    for i in range(1,len(splitValues)-2):
        img = drawImage(im, splitValues[i][0]+splitValues[i][1], splitValues[i+1][0])
        img.save('Output/'+str(j)+fn)
        j+=1
    
            


for fn in os.listdir('Input'):
    wordlength = 384
    print "Processing: " + fn
    original = Image.open("Input/"+fn)
    
    im = original.convert("L")
    im = horizontalSmearing(im, 2,5)
    im.save('Output/test'+fn)
    components = connectedComponents(im)
    
    folderName = fn.split(".")[0]
    
    ranges = []
        
    i = 0
    for c in components:
        for c2 in components:
            if c.minX < c2.minX and c2.maxX - c.minX < 191*1.2 and  c2.maxX - c.minX > 191*0.8:
                ranges.append((c.minX, c2.maxX))
    
    
                
                slice = Image.new('L',(c2.maxX - c.minX,im.size[1]))
                pic1 = original.load()
                pic2 = slice.load()
                
                
                for y in range(0,original.size[1]):
                    for x in range(c.minX,c2.maxX):
                        pic2[x-c.minX,y] = pic1[x,y]
                        
                if not os.path.exists('Output/'+folderName):
                    os.makedirs('Output/'+folderName)
                slice.save('Output/'+folderName+"/"+str(i)+fn)
                i += 1
                
    
    
    
    
    print "Done with: " + fn
    
    
    
    '''whitePerColumn = whitePerColumn(original)
    mean = getMean(whitePerColumn)
    im = original.convert("L")
    split(im,mean,whitePerColumn,fn)'''
