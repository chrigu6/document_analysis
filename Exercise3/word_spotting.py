import os
import math
from PIL import Image
import matplotlib.pyplot as plt


def groundTruth(filename, keyword):
    groundTruth = {}
    keywordOccurences = 0
    with open(filename, "r") as f:
        for line in f.readlines():
            lines = line.split(" ")
            groundTruth[lines[0] + ".png"] = lines[1]
            if lines[1].strip() == keyword:
                keywordOccurences += 1
    return (groundTruth, keywordOccurences)


def euclideanDistance(instance1, instance2, numberOfFeatures):
    #numberOfFeatures = dimension of the feature-vector aka number of extractet
    #features
    #Euclidean Distance = root( (x1-y1)^ 2 + (x2-y2)^ 2 + .... + (xn-yn)^ 2)
    distance = 0
    for x in range(0, numberOfFeatures):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def extractFeature(image, squares):
    features = []
    allblacks = 0
    pic = image.load()
    for i in range(len(squares[1])-1):
        for k in range(len(squares[0])-1):
            black = 0
            for y in range(squares[1][i], squares[1][i+1]):
                for x in range(squares[0][k], squares[0][k+1]):
                    if pic[x, y] == 0:
                        black += 1
            allblacks += black
            features.append(black)
            black = 0
    result = []
    for feature in features:
        result.append(feature / float(allblacks))
    return result


def returnTiles(image, squares):
    tiles_y = 2
    if squares % 2 is not 0:
        print "The number of squares has to be even"
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


def loadDataSet(numberOfFeatures, dataset):
    Datafeatures = {}
    for _file in os.listdir(dataset + "/words") :
        img = Image.open(dataset + "/words/" + _file)
        Datafeatures[_file] = extractFeature(
            img, returnTiles(img, numberOfFeatures)
        )
    return Datafeatures


def compareFeatures(keywordfeature, datafeatures, numberOfFeatures):
    FeatureDistances = {}
    for _file in datafeatures.keys():
        FeatureDistances[_file] = euclideanDistance(
            keywordfeature, datafeatures[_file], numberOfFeatures
        )
    return FeatureDistances


def rankFiles(d, groundTruth):
    Ranking = []
    i = 1
    for _file in sorted(d.items(), key=lambda x: x[1]):
        Ranking.append((i, groundTruth[_file[0]], _file[0]))
        i += 1
    return Ranking


def printRanking(ranking):
    for t in ranking:
        print str(t[0]) + ". " + t[1]


def calculateROC(ranking, correctResult, keywordOccurences):
    Datapoints = []
    for i in range(0, len(ranking)):
        correct = false = 0
        for k in range(i+1):
            #print i, k, len(ranking)
            if ranking[k][1].strip() == correctResult:
                correct += 1
            else:
                false += 1
        Datapoints.append((
            i,
            correct / float(keywordOccurences),
            false / float(len(ranking))
        ))
    return Datapoints


def DatapointsToCSV(datapoints, dataset, name):
    with open(dataset + "/" + name + ".csv", "w") as f:
        f.write("FPR, TPR\n")
        for point in datapoints:
            f.write(str(point[2]) + ", " + str(point[1]) + "\n")


def rank(filename, numberOfFeatures, groundTruth, dataset, correctResult):
    correctResult = correctResult[:-4]
    img = Image.open(filename)
    keywordfeature = extractFeature(img, returnTiles(img, numberOfFeatures))
    datafeatures = loadDataSet(numberOfFeatures, dataset)
    comparedFeatures = compareFeatures(
        keywordfeature, datafeatures, numberOfFeatures
    )
    ranking = rankFiles(comparedFeatures, groundTruth[0])
    
    truePositiveRates = []
    falsePositiveRates = []
    recalls = []
    precisions = []
    truePositive = 0
    falsePositive = 0
    totalPositive = groundTruth[1]
    totalNegative = len(ranking) - totalPositive
    
    keywordName = filename.split("/")[-1].split(".")[0]
    
    
    for word in ranking:
        if (word[1][:len(word[1])-1] == keywordName):
            truePositive += 1
        else:
            falsePositive += 1
                                  
        if totalNegative == 0:
            fpr = 0
        else:
            fpr = falsePositive/float(totalNegative)
            
        if totalPositive == 0:
            tpr = 0
            recall = 0
        else:
            precision = truePositive/float(truePositive+falsePositive)
            tpr = truePositive/float(totalPositive)
            recall = truePositive/float(truePositive+(totalPositive-truePositive))
            
            
        recalls.append(recall)
        precisions.append(precision)
        truePositiveRates.append(tpr)
        falsePositiveRates.append(fpr)
        
    printROCCurve(truePositiveRates, falsePositiveRates, keywordName)      
    printRecallCurve(precisions,recalls, keywordName) 
    
    
    #datapoints = calculateROC(ranking, correctResult, groundTruth[1])
    #DatapointsToCSV(datapoints, dataset, correctResult)
    
    

    return ranking
        


def printROCCurve(tpr, fpr, name):
    plt.figure(figsize=(4,4), dpi=80)
    
    plt.xlabel("FPR", fontsize=14)
    plt.ylabel("TPR", fontsize=14)
    plt.title("ROC Curve", fontsize=14)
    
    plt.plot(fpr,tpr, color="blue", linewidth=2, label="Let's ROC")
    plt.plot([1,0],[0,1], "r--", label="EER")
        
    plt.xlim(0.0,1.0)
    plt.ylim(0.0,1.0)
    plt.legend(fontsize = 10, loc='best')
    plt.tight_layout()
    plt.savefig("Output/Words/word_roc_"+name+".png")

def printRecallCurve(precision, recall, name):
    plt.figure(figsize=(4,4), dpi=80)
    
    plt.xlabel("Recall", fontsize=14)
    plt.ylabel("Precision", fontsize=14)
    plt.title("Recall-Precision Curve", fontsize=14)
    
    plt.plot(recall,precision, color="red", linewidth=2)
        
    plt.xlim(0.0,1.0)
    plt.ylim(0.0,1.0)
    plt.legend(fontsize = 10, loc='best')
    plt.tight_layout()
    plt.savefig("Output/Words/word_recall_"+name+".png")


def main(dataset):
    if not os.path.exists("Output"):
        os.mkdir("Output")
        
    if not os.path.exists("Output/Words"):
        os.mkdir("Output/Words")
    
    
    for keyword in os.listdir(dataset + "/keywords"):
        if not keyword.startswith("."):
            ranking = rank(
                dataset + "/keywords/" + keyword,
                12,
                groundTruth(dataset + "/" + dataset + ".txt", keyword[:-4]),
                dataset,
                keyword
            )
            
            if os.path.isfile("Output/Words/"+dataset+"_word_"+keyword.split(".")[0]+".txt"):
                os.remove("Output/Words/"+dataset+"_word_"+keyword.split(".")[0]+".txt")
            
            for word in ranking:
                with open("Output/Words/"+dataset+"_word_"+keyword.split(".")[0]+".txt", "a") as f:
                    f.write(word[2]+"\n")
        print "Finished processing " + keyword[:-4]

if __name__ == "__main__":
    main("Washington")
    main("Parzival")
