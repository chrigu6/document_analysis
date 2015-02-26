'''
Created on Feb 24, 2015

@author: chrigu
'''

from scipy import misc
import numpy


def split_image(image):
    images = []
    
    for y in range(0,image.shape[0], 100):
        for x in range(0, image.shape[1], 100):
            images.append(image[y:(y+99), x:(x+99)])
    
    return images

def extract_feature(image):
    
    result = numpy.zeros(image.shape)
    last = 255
    surface = 0
    
    #Traverse image from left to right
    for y in range(0,image.shape[0]):
        #Skip lines, that are totaly white
        if numpy.amin(image[y]) > 0:
            continue
        
        for x in range(0, image.shape[1]):
            #If color change mark a border pixel in the result array
            if last != image[y][x]:
                if image[y][x] == 255:
                    result[y][x-1] = 1
                else:
                    result[y][x] = 1
                    
            #Count all black pixels
            if image[y][x] == 0:
                surface = surface + 1
            last = image[y][x]
            
    last = 255
    
    #Traverse Image from top to bottom        
    for x in range(0,image.shape[1]):
        if numpy.amin(image[:,x]) > 0:
            continue
        for y in range(0, image.shape[0]):
            #If color change mark a border pixel in the result array
            if last != image[y][x]:
                if image[y][x] == 255:
                    result[y-1][x] = 1
                else:
                    result[y][x] = 1
                    
            last = image[y][x]
                      
    return [result,surface]
            
            
            
    
                          
            

if __name__ == '__main__':
    
    image = misc.imread('Input/Shapes1.png')
    images = split_image(image)
    
    
    i = 0
    
    for image in images:
        result = extract_feature(image)
        surface = result[1]
        border = numpy.sum(result[0])
        print i.__str__() + ' border: ' + border.__str__() + ' surface: ' + surface.__str__() + ' feature: ' + (surface/border).__str__()
        i = i+1