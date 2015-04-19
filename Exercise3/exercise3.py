'''(
Created on Apr 19, 2015

@author: chrigu, nic
'''

import csv
import random
import math
import operator
from PIL import Image


def loadDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        #x = numer of entries in a dataset, y = number of datafields in an entry In this case we are only interested in the first 4 fields
        for x in range(len(dataset)-1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])


def euclideanDistance(instance1, instance2, length):
    #length = dimension of the feature-vector aka number of extractet features
    #Euclidean Distance = root( (x1-y1)^ 2 + (x2-y2)^ 2 + .... + (xn-yn)^ 2)
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
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


def main():
    # prepare data
    trainingSet = []
    testSet = []
    split = 0.67
    loadDataset('iris.data', split, trainingSet, testSet)
    print 'Train set: ' + repr(len(trainingSet))
    print 'Test set: ' + repr(len(testSet))
    # generate predictions
    predictions = []
    k = 3
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')


def txtToCSVParser(filename):
    with open(filename, 'rb') as txtFile:
        with open(filename + '.data', 'w+') as cvsFile:
            for line in txtFile:
                line = line.replace(' ', ',')
                cvsFile.write(line)
            cvsFile.close()


def appendValueToDataSet(filename, function):
    dataset = []
    with open(filename, 'rU') as csvFile:
        lines = csv.reader(csvFile)
        dataset = list(lines)

    with open(filename, 'w+') as csvFile:
        writer = csv.writer(csvFile)
        for entry in dataset:
            entry.append(function(entry[1]))
            writer.writerow(entry)


def getValueOfChar(string):
    result = 0
    for char in string:
        result += ord(char)
    return result

txtToCSVParser('WashingtonDB.txt')
appendValueToDataSet('WashingtonDB.txt.data', getValueOfChar)


def extractFeature(image, squares):
    features = []
    pic = image.load()
    for i in range(len(squares[1])-1):
        for k in range(len(squares[0])-1):
            black = 0
            area = (squares[1][i+1] - squares[1][i]) * (squares[0][k+1] - squares[0][k])
            for y in range(squares[1][i], squares[1][i+1]):
                for x in range(squares[0][k], squares[0][k+1]):
                    if pic[x, y] == 0:
                        black += 1
            features.append(black / float(area))
            black = 0
    return features


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


if __name__ == "__main__":
    img = Image.open("O-c-t-o-b-e-r.png")
    print extractFeature(img, returnTiles(img, 6))
