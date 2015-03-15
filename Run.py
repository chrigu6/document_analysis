'''
Created on Feb 24, 2015

@author: chrigu
'''

import ConfusionMatrix
import ExtractFeatures
import Image
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
    
    """
    image = Image.open('Input/Shapes1N1.png')
    image = image.convert('L')
    pic = image.load()
    extractor.starTriangleChecker(pic, 700, 900)
    
    """
    #Shapes0
    print "Shapes0\n"
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes0.txt")
    image = Image.open('Input/Shapes0.png')
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
    
    #Shapes1
    print "Shapes1\n"
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes1.txt")
    image = Image.open('Input/Shapes1.png')
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
    
    #Shapes1N1    
    print "Shapes1N1\n"
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes1.txt")
    image = Image.open('Input/Shapes1N1.png')
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
    
    #Shapes2
    print "Shapes2\n" 
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes2.txt")
    image = Image.open('Input/Shapes2.png')
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
    
    #Shapes2N2A
    print "Shapes2N2A\n"
    
    if not os.path.exists('Input/Shapes2N2AFiltered.png'):
        imageFilter = ImageFilter.ImageFilter()
        image = misc.imread('Input/Shapes2N2A.png')
        image = imageFilter.MedianFilter(image, 5)
        misc.imsave('Input/Shapes2N2AFiltered.png', image)
    
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes2.txt")
    image = Image.open('Input/Shapes2N2AFiltered.png')
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
    
    #Shapes2N2B
    print "Shapes2N2B\n" 
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes2.txt")
    image = Image.open('Input/Shapes2N2B.png')
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
    
    #Shapes_Border_Easy_Validation
    print "Shapes_Border_Easy_Validation\n" 
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes_Border_Easy_Validation.txt")
    image = Image.open('Input/Shapes_Border_Easy_Validation.png')
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
    
    #Shapes_Border_Heavy_Validation
    print "Shapes_Border_Heavy_Validation\n" 
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes_Border_Heavy_Validation.txt")
    image = Image.open('Input/Shapes_Border_Heavy_Validation.png')
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
    
    #Shapes_Border_Medium_Validation
    print "Shapes_Border_Medium_Validation\n" 
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes_Border_Medium_Validation.txt")
    image = Image.open('Input/Shapes_Border_Medium_Validation.png')
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
    
    #Shapes_Clean_Validation
    print "Shapes_Clean_Validation\n" 
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes_Clean_Validation.txt")
    image = Image.open('Input/Shapes_Clean_Validation.png')
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
    
    #Shapes_Noise_Easy_Validation
    print "Shapes_Noise_Easy_Validation\n"
    
    if not os.path.exists('Input/Shapes_Noise_Easy_ValidationFiltered.png'):
        imageFilter = ImageFilter.ImageFilter()
        image = misc.imread('Input/Shapes_Noise_Easy_Validation.png')
        image = imageFilter.MedianFilter(image, 5)
        misc.imsave('Input/Shapes_Noise_Easy_ValidationFiltered.png', image)
    
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes_Noise_Easy_Validation.txt")
    image = Image.open('Input/Shapes_Noise_Easy_ValidationFiltered.png')
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
    
    #Shapes_Noise_Heavy_Validation
    print "Shapes_Noise_Heavy_Validation\n" 
    
    if not os.path.exists('Input/Shapes_Noise_Heavy_ValidationFiltered.png'):
        imageFilter = ImageFilter.ImageFilter()
        image = misc.imread('Input/Shapes_Noise_Heavy_Validation.png')
        image = imageFilter.MedianFilter(image, 5)
        misc.imsave('Input/Shapes_Noise_Heavy_ValidationFiltered.png', image)
    
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes_Noise_Heavy_Validation.txt")
    image = Image.open('Input/Shapes_Noise_Heavy_ValidationFiltered.png')
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
    
    #Shapes_Noise_Medium_Validation
    print "Shapes_Noise_Medium_Validation\n" 
    if not os.path.exists('Input/Shapes_Noise_Medium_ValidationFiltered.png'):
        imageFilter = ImageFilter.ImageFilter()
        image = misc.imread('Input/Shapes_Noise_Medium_Validation.png')
        image = imageFilter.MedianFilter(image, 5)
        misc.imsave('Input/Shapes_Noise_Medium_ValidationFiltered.png', image)
    
    matrix = ConfusionMatrix.ConfusionMatrix()
    content = extractGroundTruth("Input/Shapes_Noise_Medium_Validation.txt")
    image = Image.open('Input/Shapes_Noise_Medium_ValidationFiltered.png')
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

    
    