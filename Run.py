'''
Created on Feb 24, 2015

@author: chrigu
'''

import ConfusionMatrix
import ExtractFeatures
import Image


def split_image(image):
    images = []
    
    for y in range(0,image.shape[0], 100):
        for x in range(0, image.shape[1], 100):
            images.append(image[y:(y+99), x:(x+99)])
    
    return images



def extractGroundTruth(file):
    with open(file) as f:
            content = f.read().replace(' ', '').splitlines()
            return content

if __name__ == '__main__':
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes2.txt")
    extractor = ExtractFeatures.ExtractFeatures()
    image = Image.open('Input/Shapes2.png')
    result = extractor.boundingCircle(image)
    
    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])
            
    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix  

    
    
    