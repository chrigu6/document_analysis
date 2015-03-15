import math
import numpy

class ExtractFeatures:
    
    def boundingCircle(self,image):
        image = image.convert('L')
        pic = image.load()
        result = []
        ratios = []
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
        
                if ratio < 0.432:
                    result.append(self.starTriangleChecker(pic, a,b))
                    ratios.append(ratio)
                elif ratio < 0.6 and ratio > 0.43:
                    result.append(self.starTriangleChecker(pic, a,b))
                    ratios.append(ratio)
                elif ratio < 0.95 and ratio > 0.6:
                    result.append('square')
                    ratios.append(ratio)
                elif ratio > 0.95:
                    result.append('circle')
                    ratios.append(ratio)
        
        
        return result, ratios
    
    
    def starTriangleChecker(self,pic, a, b):
        
        blackPerLine = []
        black = 0
        
        for y in range(a,a+100):
            black = 0
            for x in range(b, b+100):
                if pic[x,y] == 0:
                    black = black + 1

            blackPerLine.append(black)
        
        changes = numpy.diff(blackPerLine)
        
        shifts = 0
        lastPositive = True
        
        for element in changes:
            if element != 0:
                if element > 0 and lastPositive == False:
                    lastPositive = True
                    shifts = shifts + 1
                if element < 0 and lastPositive == True:
                    shifts = shifts + 1
                    lastPositive = False
            
        
        

        if shifts > 1:
            return "star"
        else:
            return "triangle"
                
                    
                    
                
                