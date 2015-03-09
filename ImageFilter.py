'''
Created on Mar 4, 2015

@author: chrigu
'''

import scipy.ndimage as ndi
import numpy as np

class ImageFilter:

    def MedianFilter(self, image, windowSize):
        result = np.full_like(image, 255)
        window = np.ones(windowSize * windowSize)

        windowCenterX = (windowSize / 2)
        windowCenterY = (windowSize / 2)



        for rowIndex in range(windowCenterX, image.shape[0]-windowCenterX):
            for columnIndex in range(windowCenterY, image.shape[1]-windowCenterY):
                i = 0
                for x in range(0,windowSize):
                    for y in range(0, windowSize):
                        window[i] = image[rowIndex + x - windowCenterX][columnIndex + y - windowCenterY]
                        i = i+1
                window = np.sort(window)
                result[rowIndex][columnIndex] = window[(windowSize * windowSize) / 2]

        return result


    def binarization(self,value):
        if value != 255 or value != 0:
            if value < 127:
                value = 0
            else:
                value = 255

        return value

    def gaussianKernel(self, sigma, truncate=1.0):
        sigma = float(sigma)
        radius = int(truncate * sigma + 0.5)

        x, y = np.mgrid[-radius:radius+1, -radius:radius+1]
        sigma = sigma**2

        k = 2*np.exp(-0.5 * (x**2 + y**2) / sigma)
        k = k / np.sum(k)

        return k
