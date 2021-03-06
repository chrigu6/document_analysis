'''
Created on Feb 24, 2015

@author: chrigu
'''

import ConfusionMatrix
import ExtractFeatures
import ImageFilter
from PIL import Image
import ImageFilter
from scipy import misc
import os.path


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
    results = []
    extractor = ExtractFeatures.ExtractFeatures()

    #Shapes_Border_Easy_Test
    print "Shapes_Border_Easy_Test\n"
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Validation/Shapes_Border_Easy_Test.txt")
    image = Image.open('Validation/Shapes_Border_Easy_Test.png')
    result = extractor.boundingCircle(image)

    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])

    results.append(float(correct)/float(80))

    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix
    print("------------------------------------------------------------------------------")
    
    #Shapes_Border_Heavy_Test
    print "Shapes_Border_Heavy_Test\n"
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Validation/Shapes_Border_Heavy_Test.txt")
    image = Image.open('Validation/Shapes_Border_Heavy_Test.png')
    result = extractor.boundingCircle(image)

    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])

    results.append(float(correct)/float(80))

    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix
    print("------------------------------------------------------------------------------")
    
    #Shapes_Border_Medium_Test
    print "Shapes_Border_Medium_Test\n"
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Validation/Shapes_Border_Medium_Test.txt")
    image = Image.open('Validation/Shapes_Border_Medium_Test.png')
    result = extractor.boundingCircle(image)

    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])

    results.append(float(correct)/float(80))

    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix
    print("------------------------------------------------------------------------------")
    
    #Shapes_Clean_Test
    print "Shapes_Clean_Test\n"
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Validation/Shapes_Clean_Test.txt")
    image = Image.open('Validation/Shapes_Clean_Test.png')
    result = extractor.boundingCircle(image)

    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])

    results.append(float(correct)/float(80))

    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix
    print("------------------------------------------------------------------------------")
    
    #Shapes_Noise_Easy_Test
    print "Shapes_Noise_Easy_Test\n"

    if not os.path.exists('Validation/Shapes_Noise_Easy_TestFiltered.png'):
        imageFilter = ImageFilter.ImageFilter()
        image = misc.imread('Validation/Shapes_Noise_Easy_Test.png')
        image = imageFilter.MedianFilter(image, 5)
        misc.imsave('Validation/Shapes_Noise_Easy_TestFiltered.png', image)

    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Validation/Shapes_Noise_Easy_Test.txt")
    image = Image.open('Validation/Shapes_Noise_Easy_TestFiltered.png')
    result = extractor.boundingCircle(image)

    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])

    results.append(float(correct)/float(80))

    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix
    print("------------------------------------------------------------------------------")
    
    #Shapes_Noise_Heavy_Test
    print "Shapes_Noise_Heavy_Test\n"

    if not os.path.exists('Validation/Shapes_Noise_Heavy_TestFiltered.png'):
        imageFilter = ImageFilter.ImageFilter()
        image = misc.imread('Validation/Shapes_Noise_Heavy_Test.png')
        image = imageFilter.MedianFilter(image, 5)
        misc.imsave('Validation/Shapes_Noise_Heavy_TestFiltered.png', image)

    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Validation/Shapes_Noise_Heavy_Test.txt")
    image = Image.open('Validation/Shapes_Noise_Heavy_TestFiltered.png')
    result = extractor.boundingCircle(image)

    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])

    results.append(float(correct)/float(80))

    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix
    print("------------------------------------------------------------------------------")
    
    #Shapes_Noise_Medium_Test
    print "Shapes_Noise_Medium_Test\n"

    if not os.path.exists('Validation/Shapes_Noise_Medium_TestFiltered.png'):
        imageFilter = ImageFilter.ImageFilter()
        image = misc.imread('Validation/Shapes_Noise_Medium_Test.png')
        image = imageFilter.MedianFilter(image, 5)
        misc.imsave('Validation/Shapes_Noise_Medium_TestFiltered.png', image)

    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Validation/Shapes_Noise_Medium_Test.txt")
    image = Image.open('Validation/Shapes_Noise_Medium_TestFiltered.png')
    result = extractor.boundingCircle(image)

    correct = 0
    for i in range(0, 80):
        matrix.addResult([content[i],result[0][i]])
        if content[i] == result[0][i]:
            correct += 1
        else:
            print(i, content[i], result[0][i], result[1][i])

    results.append(float(correct)/float(80))

    print 'Recognition Ratio: ' + str(float(correct)/float(80)) + '\n'
    print 'Confusion-Matrix:\n'
    print matrix
    print("------------------------------------------------------------------------------")
    
    print "Total Recognition Ratio: " + str(sum(results)/len(results))