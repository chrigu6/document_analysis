'''
Created on Apr 28, 2015

@author: chrigu
'''
import os
import Image
import math
from matplotlib.cbook import Null
import matplotlib.pyplot as plt
from cv2 import transform

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

def checkRange(components, x, y):
    for c in components:
        if(c.isinRange(x,y)):
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

def isElement(size,pic,p):
    if p[0] >= 0 and p[0] < size[0] and p[1] >= 0 and p[1] < size[1]:
        return pic[p[0],p[1]] == 0
    else:
        return False

def removeNested(components):
    for checkedComponent in components:
        for otherComponent in components:
            if otherComponent.componentInRange(checkedComponent) and not otherComponent.isEqual(checkedComponent):
                components.remove(checkedComponent)
                break

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

def getRanges(wordlength, fn, short):
    original = Image.open(fn)
    im = original.convert("L")
    im = horizontalSmearing(im, 5,10)
    #if not os.path.exists('Output/'+short.split(".")[0]):
             #       os.makedirs('Output/'+short.split(".")[0])
    #im.save("Output/"+short.split(".")[0]+"/0000smeared.png")
    components = connectedComponents(im)
    #rgbimg = drawBorder(components, original)
    #rgbimg.save("Output/"+short.split(".")[0]+"/0000border.png")
    ranges = []        
        
    for c in components:
        if c.maxX - c.minX < wordlength*1.4263 and c.maxX - c.minX  > wordlength*0.74:
            ranges.append((c.minX,c.maxX))
        for c2 in components:
            if c.minX < c2.minX and c2.maxX - c.minX < wordlength*1.4263 and  c2.maxX - c.minX > wordlength*0.74:
                ranges.append((c.minX, c2.maxX))
    
    
    return ranges
         
def extractFeature(image,  squares):
    features = []
    allblacks = 0
    pic = image.load()
    for i in range(len(squares[1])-1):
        for k in range(len(squares[0])-1):
            black = 0
            for y in range(squares[1][i], squares[1][i+1]):
                for x in range(squares[0][k], squares[0][k+1]):
                    if pic[x, y] == 0:
                        black += 1
            allblacks += black
            features.append(black)
            black = 0
    result = []
    for feature in features:
        result.append(feature / float(allblacks))
    return result

def returnTiles(image, squares):
    tiles_y = 2
    if squares % 2 is not 0:
        print "The number of squares has to be even"
    tiles_x = squares / tiles_y
    tiles_sizeX = round(image.size[0] / float(tiles_x))
    tiles_sizeY = round(image.size[1] / 2.0)
    squares_x = []
    squares_y = []
    x = y = 0
    for i in range(tiles_x):
        squares_x.append(int(x))
        x += tiles_sizeX
    squares_x.append(image.size[0])
    for k in range(tiles_y):
        squares_y.append(int(y))
        y += tiles_sizeY
    squares_y.append(image.size[1])
    return [squares_x, squares_y]        
    

def sliceImg(r, img):
    sliced = Image.new('L',(r[1] - r[0],img.size[1]))
    pic1 = img.load()
    pic2 = sliced.load()
                
    for y in range(0,img.size[1]):
        for x in range(r[0],r[1]):            
            pic2[x-r[0],y] = pic1[x,y]
    
    return sliced

def euclideanDistance(instance1, instance2, numberOfFeatures):
    #numberOfFeatures = dimension of the feature-vector aka number of extractet
    #features
    #Euclidean Distance = root( (x1-y1)^ 2 + (x2-y2)^ 2 + .... + (xn-yn)^ 2)
    distance = 0
    for x in range(0, numberOfFeatures):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)





def main(dataset):
    lines = generateGroundTrouth(dataset+"/Lines"+dataset+".txt",dataset + "/lines/")    
    with open("result" + dataset+".txt", "w") as f:
                f.write("Rank\t\t\t\tKeyword\t\t\t\tLinename\t\t\t\tSimularity\t\t\t\tCorrect\n")
                f.write("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    for keyword in os.listdir(dataset + "/keywords"):
        print "Processing: " + keyword
        img = Image.open(dataset + "/keywords/" + keyword)
        wordlength = img.size[0]
        keywordfeature = extractFeature(img, returnTiles(img, 12))
        keywordName = keyword.split(".")[0]
        matches = []
        
        
        
        for fn in os.listdir(dataset + "/lines"):
            currentLine = Null
            #print "Processing: " + fn
            for l in lines:
                #print l.name
                #print fn.split(".")[0]
                if l.name == fn.split(".")[0]:
                    currentLine = l
            
            
            img = Image.open(dataset + "/lines/" +  fn)
            #img.show()
            #raw_input("wait..")
            ranges = getRanges(wordlength, dataset + "/lines/" +  fn, fn)
            match = (100,"test")
            #if not os.path.exists('Output/'+fn.split(".")[0]):
                    #os.makedirs('Output/'+fn.split(".")[0])
            i = 0
            for r in ranges:
                subImg = sliceImg(r,img)
                
    
                #subImg.save("Output/"+fn.split(".")[0]+"/"+fn.split(".")[0]+str(i)+".png")
                feature = extractFeature(subImg, returnTiles(subImg, 12))
                distance = euclideanDistance(keywordfeature, feature, 12)
                if match[0] > distance:
                    match = (distance,fn.split(".")[0]+str(i)+".png") 
                    #subImg.show()
                    #raw_input("wait..")
                i += 1
            matches.append((fn,match,currentLine.contains(keywordName)))
            matches.sort(key=lambda tup: tup[1][0])
        
        
        totalPositive = 0
        for l in lines:
                if l.contains(keywordName):
                    totalPositive += 1
                    
        totalLines = len(lines)
        totalNegative = totalLines - totalPositive
        print totalNegative
        print totalPositive
        truePositiveRates = []
        falsePositiveRates = []
        recall = []
        precision = []
        truePositive = 0
        falsePositive = 0
        
        with open("result" + dataset+".txt", "a") as f:
            j = 1
            for match in matches:
                f.write(str(j) + "\t\t\t\t" +  str(keywordName) + "\t\t\t\t" + str(match[0]) + "\t\t\t\t" + str(match[1][0]) + "\t\t\t\t" + str(match[2]) + "\n")
                j += 1
                if match[2]:
                    truePositive += 1
                else:
                    falsePositive += 1
                                  
                if totalNegative == 0:
                    fpr = 0
                else:
                    fpr = falsePositive/float(totalNegative)
                    
                if totalPositive == 0:
                    tpr = 0
                else:
                    tpr = truePositive/float(totalPositive)
                    
                truePositiveRates.append(tpr)
                falsePositiveRates.append(fpr)
                recall.append(truePositive/(truePositive+falsePositive))
                
        print truePositiveRates
        print falsePositiveRates
        printROCCurve(truePositiveRates, falsePositiveRates, keywordName)               
            
            #raw_input("done")
    #print lines

def printROCCurve(tpr, fpr, name):
    plt.figure(figsize=(4,4), dpi=80)
    
    plt.xlabel("FPR", fontsize=14)
    plt.ylabel("TPR", fontsize=14)
    plt.title("ROC Curve", fontsize=14)
    
    plt.plot(fpr,tpr, color="blue", linewidth=2, label="Let's ROC")
    plt.plot([1,0],[0,1], "r--", label="EER")
        
    plt.xlim(0.0,1.0)
    plt.ylim(0.0,1.0)
    plt.legend(fontsize = 10, loc='best')
    plt.tight_layout()
    plt.savefig("roc_"+name+".png")
    

class Line:
    name = ""
    words = []
    
    def contains(self,keyword):
        for word in self.words:
            if keyword == word:
                return True
        return False


def generateGroundTrouth(filename, path):
    lines = []
    with open(filename, "r") as f:
        for line in f.readlines():
            rawLine = line.replace("\n","")
            data = rawLine.split(" ")
            words = data[1].split("|")
            data[1] = words
            if(os.path.isfile(path + data[0]+".png")):
                a = Line()
                a.name = data[0]
                a.words = data[1]
                lines.append(a)
            
    return lines
                    
        
if __name__ == "__main__":
    main("Washington")
    main("Parzival")
    