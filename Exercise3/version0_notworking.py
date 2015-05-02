'''(
Created on Apr 19, 2015

@author: chrigu, nic
'''

import csv
import random
import math
import operator
from PIL import Image
import os.path
import dtw

#Hstogramm slidingwindow
#upperconture
#lowerconture
#number of b/w transisitions
#Toni Rath
#To extract gradients smoothen image with gaussian filter
#Gradient features
#Vincerelli features


def loadDataset(filename, trainingSet=[]):
    with open (filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        #x = nubmer of entries in a dataset, y = number of datafields in an entry In this case we are only interested in the first 4 fields
        for x in range(len(dataset)):
            length = dataset[x][0] = int(dataset[x][0])
            for y in range(1, length+1):
                dataset[x][y] = float(dataset[x][y])
            trainingSet.append(dataset[x])

def loadRandomDataset(filename, split, trainingSet=[], testSet=[]):
    with open (filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        #x = numer of entries in a dataset, y = number of datafields in an entry In this case we are only interested in the first 4 fields
        for x in range(len(dataset)):
            length = dataset[x][0]
            for y in range(1, length+1):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])
    
                

def euclideanDistance(instance1, instance2, startSequence, length):
    #length = dimension of the feature-vector aka number of extractet features
    #Euclidean Distance = root( (x1-y1)^ 2 + (x2-y2)^ 2 + .... + (xn-yn)^ 2)
    distance = 0
    for x in range(startSequence,length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def dynamicTimeWarp(instance1, instance2, startSequence, length1, length2):
    return dtw.dtw(instance1[startSequence:length1],instance2[startSequence:length2])[0]


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    for x in range(len(trainingSet)):
        #dist = dynamicTimeWarp(testInstance,trainingSet[x],1,testInstance[0]+1,trainingSet[x][0]+1)
        dist = euclideanDistance(testInstance, trainingSet[x], 1, trainingSet[0][0]+1)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    print len(distances)
    for x in range(k):
        neighbors.append(distances[x][0])
        print str(x) + "nearest neighbour: " + str(distances[x][0][len(distances[x][0])-2]) + " " + str(distances[x][0][-1]) + " value: " + str(distances[x][1])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1

    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0


def main(filename):
    # prepare data
    trainingSet = []
    loadDataset('WashingtonDB.txt.data', trainingSet)
    print 'Train set: ' + repr(len(trainingSet))
    predictions = []
    k = 10
    img = Image.open("data-week1/WashingtonDB/keywords/"+filename)
    #testSet = extractFeature(img, returnTiles(img, 2))
    testSet = blackPerColumn(img)
    testSet.insert(0, len(testSet))
    testSet.append("goal")
    testSet.append(filename.split(".")[0])
    testSet = [testSet]

    neighbors = getNeighbors(trainingSet, testSet[0], k)
    result = getResponse(neighbors)
    predictions.append(result)
    print('> predicted=' + repr(result) + ', actual=' + repr(testSet[0][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')


def txtToCSVParser(filename):
    with open(filename, 'rb') as txtFile:
        with open(filename + '.data', 'w+') as cvsFile:
            for line in txtFile:
                line = line.replace(' ', ',')
                cvsFile.write(line)
            cvsFile.close()


def appendValueToDataSet(filename, path):
    dataset = []
    with open(filename, 'rU') as csvFile:
        lines = csv.reader(csvFile)
        dataset = list(lines)

    with open(filename, 'w+') as csvFile:
        writer = csv.writer(csvFile)
        for entry in dataset:
            if(os.path.isfile(path + entry[0]+".png")):
                img = Image.open(path + entry[0]+".png")
                features = extractFeature(img, returnTiles(img, 2))
                #features = blackPerColumn(img)
                for f in features:
                    entry.insert(0,f)
                entry.insert(0,len(features))
                writer.writerow(entry)


def extractFeature(image, squares):
    pic = image.load()
    totalBlack = 0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pic[x,y] == 0:
                totalBlack += 1
    
    features = []

    for i in range(len(squares[1])-1):
        for k in range(len(squares[0])-1):
            black = 0
            area = (squares[1][i+1] - squares[1][i]) * (squares[0][k+1] - squares[0][k])
            for y in range(squares[1][i], squares[1][i+1]):
                for x in range(squares[0][k], squares[0][k+1]):
                    if pic[x, y] == 0:
                        black += 1
            features.append(black / float(totalBlack))
            black = 0
    return features

def blackPerColumn(img):
    pic = img.load()
    height = img.size[1]
    
    blackPerColumn = []
    
    for x in range(0, img.size[0]):
        i = 0
        for y in range(0, img.size[1]):
            if pic[x,y] == 0:
                i += 1
        blackPerColumn.append(float(i)/height*2)
    return blackPerColumn


def returnTiles(image, squares):
    tiles_y = 2
    if squares % 2 is not 0:
        print "The number squares has to be even"
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

def getChar(input):
    i = 0
    for c in input:
        i += ord(c)
    return [i]
        


if __name__ == "__main__":
    #structure of data: numberofFeatures|feature1 . . . featuren|filename|groundtruth
    txtToCSVParser('WashingtonDB.txt')
    appendValueToDataSet('WashingtonDB.txt.data', 'testSet/')
    main("O-c-t-o-b-e-r.png")