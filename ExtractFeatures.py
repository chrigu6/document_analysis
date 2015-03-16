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
                black = 0
                radius = 0
                for y in range(a, a+100):
                    for x in range(b, b+100):
                        if pic[x,y] == 0:
                            black+=1
                            test = math.sqrt(float(abs(x-50-b)**2 + abs(y-50-a)**2)
                                            )
                            if test > radius:
                                radius = test

                area = (radius**2) * math.pi
                ratio = (float(black)/float(area))

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

        #print changes

        for element in changes:
            if element != 0:
                if element > 0 and lastPositive == False:
                    lastPositive = True
                    shifts = shifts + 1
                if element < 0 and lastPositive == True:
                    shifts = shifts + 1
                    lastPositive = False




        if shifts > 2:
            return "star"
        else:
            return "triangle"





