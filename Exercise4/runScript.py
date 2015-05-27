'''
Created on May 14, 2015

@author: chrigu
'''
import subprocess
import Image
import os
from random import randint
import features
from cv2 import inRange

inputTrainingFile = "mnist" + "." + "train.noClue" + ".txt"
inputTestFile = "mnist" + "." + "test.noClue" + ".txt"
outputTrainingFile = "output_training.txt"
outputResultsFile = "output_results.txt"



def getActivationFunciton(value):
    if value == 0:
        return "SIGMOID"
    if value == 1:
        return "SOFTSIGN"
    if value == 2:
        return "TANH"
    return "SIGMOID"

#Normalizes the feature values between 0 and 1
def normalizeFeatures(features):
    minE = min(features)
    maxE = max(features)
    
    result = []
    
    for feature in features:
        result.append((feature-minE)/(maxE-minE))
        
    return result
    
    
    
def getPixelValues(img):
    featureValues = []
    im = Image.open(img)
    im = im.convert('L')
    im = im.convert('1')
    pic = im.load()
    for y in range(im.size[1]):
            for x in range(im.size[0]):
                featureValues.append(pic[x, y])
    
    featureValues = normalizeFeatures(featureValues)
    return featureValues
                    
                
    

#Takes the path to the parent folder of the different picture sets
#returns two arrays one for the training and one for the test set.
#Each of these arrays contains tuples containing the value of each picture and the feature array.

"""
trainFeatures                                                                testfeatures
[(value#1,[feature1,....,featureN]) ,(value#2,[feature1,....,featureN])], [(value#1,[feature1,....,featureN]) ,(value#2,[feature1,....,featureN])]
"""
def extractFeature(path):
    testFeatures = []
    trainFeatures = []
    print "extracting training features"    
    for imageFile in os.listdir(path + "/train/"): 
        value =  imageFile[7]
        featureValues = getPixelValues(path + "/train/" +imageFile)
        trainFeatures.append((value,featureValues))
    
    print "extracting testing features"  
    for imageFile in os.listdir(path + "/test/"): 
        value =  imageFile[7]
        featureValues = getPixelValues(path + "/test/" +imageFile)
        testFeatures.append((value,featureValues))
        
    
    return [trainFeatures, testFeatures]

#Takes an array of tuples with the following structure as input: [(value#1,[feature1,....,featureN]) ,(value#2,[feature1,....,featureN])]
#Creates a file with the name "fileName" with the following structure: value#1, feature1, .... featureN
def generateOutput(values, fileName):
    if os.path.isfile(fileName):
                os.remove(fileName)
                
    with open(fileName, "a") as f:
        for value in values:
            f.write(value[0])
            for feature in value[1]:
                f.write(","+str(feature))
            f.write("\n")
    
        

def executeJar(inputTraining, inputTest, outputTraining, outputResults, activationFunction, featureSize, numberNeurons, outputSize, learningRate, numberEpochs):
    subprocess.call(["java", "-jar", "-Xmx512m", "NN Tool.jar","-a", getActivationFunciton(activationFunction), "-f",str(featureSize), "-n",str(numberNeurons), "-o", str(outputSize), "-l", str(learningRate), "-e", str(numberEpochs), inputTrainingFile, inputTestFile, outputTrainingFile, outputResultsFile])

def run(numberOfNeurons, learningRate, numberOfEpochs):
    pathToImages = "/home/chrigu/Desktop/images/images/"
    statsFile = "stats.txt"
    outputSize = 10
    featureSize = 8
    
    if not os.path.isfile(inputTrainingFile):
        print "extracting features"
        f = features.Features(pathToImages)
        trainFeatures = f.get_specific_feature(squares=8)
        testFeatures = f.get_specific_feature(squares=8, folder="test")
        
        print "generating training and testing file"
        
        for item in trainFeatures:
            f.write_feature_vector(item[0], item[1], item[2], "noClue")
        
        for item in testFeatures:
            f.write_feature_vector(item[0], item[1], item[2], "noClue")
            
    print "number of neurons: " + str(numberOfNeurons) + "\nlearning rate: " + str(learningRate) + "\nnumber of epoches: " + str(numberOfEpochs)
    
    activationFunction = "SIGMOID"
    executeJar(inputTrainingFile, inputTestFile, outputTrainingFile, outputResultsFile, activationFunction, featureSize, numberOfNeurons, outputSize, learningRate, numberOfEpochs)
    with open(outputResultsFile, "r") as f:
        line = f.readlines()
        line =  line[len(line)-1]
        accuracy = line.split(" ")[1]
        with open(statsFile, "a") as stats:
            stats.write(str(accuracy)+","+activationFunction+","+str(numberOfNeurons)+","+str(learningRate)+","+str(numberOfEpochs)+"\n")    


if __name__ == '__main__':
    numberOfNeurons = 10
    learningRate = 0.1
    i = 2
    while(i<513):
        run(numberOfNeurons, learningRate, i)
        i = i *2
                
            
                
            
        
        
        
                
    
    

    print "finished"
    
    
        
    
    