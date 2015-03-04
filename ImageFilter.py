'''
Created on Mar 4, 2015

@author: chrigu
'''

import numpy

class ImageFilter:
    
    def MedianFilter(self, image, windowSize):
        result = numpy.zeros(image.shape)
        window = numpy.ones(windowSize * windowSize)
        
        windowCenterX = (windowSize / 2)
        windowCenterY = (windowSize / 2)
        

        
        for rowIndex in range(windowCenterX, image.shape[0]-windowCenterX):
            for columnIndex in range(windowCenterY, image.shape[1]-windowCenterY):
                i = 0
                for x in range(0,windowSize):
                    for y in range(0, windowSize):
                        window[i] = image[rowIndex + x - windowCenterX][columnIndex + y - windowCenterY]
                        i = i+1
                window = numpy.sort(window)
                result[rowIndex][columnIndex] = window[(windowSize * windowSize) / 2]
                
        return result
            
        