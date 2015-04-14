from PIL import Image
import os

original = Image.open("DC/DC1/DC1.1/3243a181-1.jpg")
im = original.convert("L")


def binarize(image):
    pic = image.load()
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            if pic[x,y] < 127:
                pic[x,y] = 0
            else:
                pic[x,y] = 255
    return image



def horizontalSmearing(image, limit):
    pic = image.load()
    white = 0
    for y in range(0, image.size[1]):
        white = 0
        for x in range(0, image.size[0]):
            if pic[x,y] == 255:
                white += 1
            elif pic[x,y] == 0 or x == image.size[0]:
                if white >= limit and white < 50:
                    for i in range(x, x-white-1, -1):
                        pic[i,y] = 0
                white = 0
    return image

def verticalSmearing(image, limit):
    pic = image.load()
    white = 0
    for y in range(0, image.size[0]):
        white = 0
        for x in range(0, image.size[1]):
            if pic[y,x] == 255:
                white += 1
            elif pic[y,x] == 0 or x == image.size[0]:
                if white >= limit and white < 50:
                    for i in range(x, x-white-1, -1):
                        pic[y,i] = 0
                white = 0
    return image

def combine(image1, image2):
    pic1 = image1.load()
    pic2 = image2.load()
    newImage = Image.new("1", (image1.size[0], image1.size[1]), "white")
    combinedImage = newImage.load()
    for y in range(0, image1.size[1]):
        for x in range(0, image1.size[0]):
            combinedImage[x,y] = max(pic1[x,y],pic2[x,y])
    return newImage



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
    
            

def getComponent(image,x,y):
    
    pic = image.load()
    component = Component()
    component.update(x,y)
    p0X = x
    p0Y = y
    q0X = x
    q0Y = y-1
    d =  0
    pX = x
    pY = y
    rotated = 0
    
    while (True):
        #Inspired by: http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/theo.html
        #Move one square towards d and one to the left
        p1 = getStepfromDirection((d+1)%8, pX, pY)
        if isElement(image.size, pic, p1):
            component.update(p1[0],p1[1])
            pX = p1[0]
            pY = p1[1]
            d = (d + 2) % 8
            rotated = 0
        else :
            #Move one square towards d
            p2 = getStepfromDirection(d, pX, pY)
            if isElement(image.size, pic, p2):
                component.update(p2[0],p2[1])
                pX = p2[0]
                pY = p2[1]
                rotated = 0
            
            else:
                #Move one square towards d and one to the right
                p3 = getStepfromDirection((d+7)%8, pX, pY)
                if isElement(image.size, pic, p3):
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
                        
    
        if p0X == pX and p0Y == pY:
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
                
def drawPolygon(components, image):
    rgb_img = image.convert('RGB')
    pic = rgb_img.load()

    for c in components:
        for p in c.points:
            pic[p[0],p[1]] = (0,0,255)
    
    return rgb_img

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

#Code for Execution


for fn in os.listdir('Input'):
    i = 0
    print "processing: " + fn
    original = Image.open("Input/"+fn)
    im = original.convert("L")
    im = binarize(im)
    im.save('Output/'+fn+"_binarized.png")

    im = horizontalSmearing(im, 3)
    im.save('Output/'+fn+"_smeared.png")
    
    components = connectedComponents(im)
    f = open("Output/" + fn+ ".txt","w")
    for c in components:
        f.write(str(i) + ", " + str(c.minX) + ", " + str(c.minY) + ", "  + str(c.maxX) + ", " + str(c.minY) + ", " + str(c.maxX) + ", " + str(c.maxY) + ", "  + str(c.minX) + ", " + str(c.maxY) + ", " + str(c.minX) + ", " + str(c.minY)+"\n" )
        i = i + 1
    
    f.close()
    rgbimg = drawBorder(components, original)
    rgbimg.save('Output/'+fn+"_border.png")
    print "Done with: " + fn
    
    
