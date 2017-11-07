from math import log
import operator

#calculate shannon Ent
def calcShannonEnt(dataSet):
    '''
    :param
    dataSet:the dataSet to calculate the ent,the last column is label
    :return:
    the ent of the dataset
    '''
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0
        labelCount[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCount:
        prob = float(labelCount[key])/numEntries
        shannonEnt -=prob * log(prob,2)
    return shannonEnt


def splitDataSet(dataSet,axis,value):
    """
    :parameter
    dataSet: the dataSet to split
    axis:the feature to split the dataSet
    value:the feature value to split the dataSet
    :returns
    the value to the feature's dataSet
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value :
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    '''
    :param
    dataSet:the dataset to crete a tree
    :return:
    the best feature to split the node
    '''
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0;bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy-newEntropy
        if infoGain>bestInfoGain :
            bestInfoGain = infoGain
            bestFeature =  i
    return bestFeature

def majorityCnt(labelList):
    classcount = {}
    for vote in labelList:
        if vote not in classcount.keys():
            classcount[vote] = 0
        classcount[vote] +=1
        sortedClassCount = sorted(classcount.iteritems(),key=operator.itemgetter,reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0] == len(classList)):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree




#create dataSet
def createDataSet():
    dataset = [[1,1,'yes'],
               [1,1,'yes'],
               [0,1,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataset,labels



if __name__ == '__main__':
    print createDataSet()
    ds,lbs = createDataSet()
    print chooseBestFeatureToSplit(ds)
    print calcShannonEnt(ds)
    print createTree(ds,lbs)