# Calculate the Bayesian score of a network against a dataset

# PANDAS
try:
    import pandas as pd
except ImportError:
    raise ImportError("PANDAS required for filter()")
except RuntimeError:
    print("PANDAS unable to open")
    raise


import graphopanda as opanda
import graphoxnet as oxnet

import math

############
# SCORE: get score using factors, or sums of logs
def getScore(graph, dataframe, label):
    ### Log Bayesian score
    logScore = getLogBayesianScore(graph, dataframe, label)
    print "LOG SCORE: " + str(logScore)
    ### Cooper & Herscovitz
    cooperHscore = getCooperHerscovitsBayesianScore(graph, dataframe, label)
    print "COOPER HERRSCOVITS SCORE: " + str(cooperHscore)
    return cooperHscore


# SCORING WITH FACTORS: Cooper & Herscovits, page 320, formula 8
# It is the same as Decisions under Uncertainty, page 47, formula 2.80
# Posterior probability: is proportional to the prior probability
# Cancelling out: prior probability cancels out when two networks are compared by division
# Example: if Score(network1)/Score(network2)>1 then network1 is better representation of the data
def getCooperHerscovitsBayesianScore(graph, dataframe, label):
    score = float(1)
    values = iterateThroughCombinations(graph, dataframe, label)
    print ">>>>> VALUES: " + str(values)
    # >>>>> VALUES: [(2, [[5, 5]]), (2, [[1, 4], [4, 1]]), (2, [[4, 1], [0, 5]])]
    #
    for value in values:
        print "*********************************** COMPUTING VALUE: " + str(value)
        # *********************************** COMPUTING VALUE: (2, [[5, 5]])
        # *********************************** COMPUTING VALUE: (2, [[1, 4], [4, 1]])
        # *********************************** COMPUTING VALUE: (2, [[4, 1], [0, 5]])
        #
        # NUMERATOR
        # Gamma(alphaIJ)
        alphaIJ0 = value[0]-1   # Design under uncertainty equation 2.80
        print "alphaIJ0=" + str(alphaIJ0)
        alphaIJ0Factorial = math.factorial(alphaIJ0)
        print "alphaIJ0Factorial=" + str(alphaIJ0Factorial)
        score = score * alphaIJ0Factorial
        print "score=" + str(score)
        # mIJK numerator
        for mValues in value[1]:
            print "COUNT VALUE " + str(mValues)
            print "the values mValues=" + str(mValues)
            print "############################# mValues=" + str(mValues)
            # ############################# mValues=[5, 5]
            # ############################# mValues=[1, 4]
            # ############################# mValues=[4, 1]
            # ############################# mValues=[4, 1]
            # ############################# mValues=[0, 5]
            for m in mValues:      # Design under uncertainty equation 2.80
                print "====COMPUTING M: " + str(m)
                print "m=" + str(m)
                mFactorial = math.factorial(m)
                print "mFactorial=" + str(mFactorial)
                score = score * mFactorial
                print "score=" + str(score)
            print "all numerator score=" + str(score)
            # DENOMINATOR
            mAdjustedIJ0 = alphaIJ0;
            print "reset mAdjustedIJ0=" + str(mAdjustedIJ0)
            for m in mValues:      # Design under uncertainty equation 2.80
                print "====COMPUTING DENOMINATOR: " + str(m)
                print "m=" + str(m)
                mAdjustedIJ0 = mAdjustedIJ0 + m
                print "mAdjustedIJ0=" + str(mAdjustedIJ0)
            mfinalIJ0 = mAdjustedIJ0
            print "final mAdjustedIJ0=" + str(mAdjustedIJ0)
            mAdjustedIJ0Factorial = math.factorial(mfinalIJ0)
            print "mAdjustedIJ0Factorial=" + str(mAdjustedIJ0Factorial)
            score = score / mAdjustedIJ0Factorial
            print "all denominator score=" + str(score)
    return score


# SCORING WITH FACTORS: Decisions Under Uncertainty, page 47, formula 2.83
# Posterior probability: is proportional to the prior probability
# Cancelling out: prior probability cancels out when two networks are compared by division
# Example: if Score(network1)-Score(network2)>0 then network1 is better representation of the data
def getLogBayesianScore(graph, dataframe, label):
    score = float(0)
    values = iterateThroughCombinations(graph, dataframe, label)
    alphaIJ0list = getAlphaij0Hyperparam(values)
    mij0list = getMij0GroupedCount(values)
    print "groupled mij0: " + str(mij0list)
    randomVarNames = opanda.getRandomVarNodeNames(dataframe)
    for i in range(0, getNumRandomVars(randomVarNames)):
        # print "i= " + str(i)
        randomVarName = randomVarNames[i]
        parents = oxnet.getRandomVarParents(randomVarName, graph)
        qi = getQi(parents)
        for j in range(0, qi):
            # print "j= " + str(j)
            # sum over random vars and parents
            numeratorAlpha = alphaIJ0list[i]-1
            # print str(i) + " numeratorAlpha " + str(numeratorAlpha)
            numeratorFactorialAlpha = math.factorial(numeratorAlpha)
            # print str(i) + " numeratorFactorialAlpha " + str(numeratorFactorialAlpha)
            denominatorAlphaCount = numeratorAlpha
            # print "denominatorAlphaCount INIT " + str(denominatorAlphaCount)
            for mijkSublistList in mij0list[i]:
                # print "actual sub mijkList: " + str(mijkSublistList)
                for mijk in mijkSublistList:
                    # print ">>> mijk: " + str(count)
                    denominatorAlphaCount = denominatorAlphaCount + mijk
                    # print str(i) + " last term mijk count " + str(mijk)
            denominatorFactorialCount = math.factorial(denominatorAlphaCount)
            print str(i) + " denominatorFactorialCount " + str(denominatorFactorialCount)
            score = math.log(numeratorFactorialAlpha) - math.log(denominatorFactorialCount)
            print "***UPDATED score: " + str(score) + " WITH alphaCount " + str(denominatorAlphaCount) + " and mijkList " + str(mij0list[i])
            ri = getNumRandomVarValues(dataframe, randomVarName)
            # iterate over the k values of random var
            for mijkSubList in mij0list[i]:
                # print "*mijk " + str(mijk)
                factorialMijk = math.factorial(mijk)
                # print "factorial *mijk " + str(factorialMijk)
                score = score + math.log(factorialMijk)
                print "$$$UPDATED score: " + str(score) + " with mijkSubList " + str(mijkSubList)
    return score


# ri: the number of values each random var takes
def getAlphaij0Hyperparam(values):
    Alphaij = []
    for value in values:
        alpha = value[0]
        # print "alpha=" + str(alpha)
        Alphaij.append(alpha)
    return Alphaij

# Mij0
# the number of times a random var takes a value, given it's parents
def getMij0Count(values):
    Mij0 = []
    for value in values:
        for m in value[1]:
            # print "m=" + str(m)
            Mij0.append(m)
    return Mij0

def getMij0GroupedCount(values):
    Mij0 = []
    for value in values:
        Mijk = []
        for m in value[1]:
            # print "m=" + str(m)
            Mijk.append(m)
        Mij0.append(Mijk)
    return Mij0


# ITERATE: iterates through i=(1:n), j=(1:qi), k=(1:ri)
# Returns the values necessary to compute the Bayesian score
# NOTE: Python uses 0-based indexing!!!
def iterateThroughCombinations(graph, dataframe, label):
    values = [] # used to return all the necessary values to compute the Bayesian score
    randomVarNames = opanda.getRandomVarNodeNames(dataframe)
    n = getNumRandomVars(randomVarNames)
    for i in range(0, n):  # i random var
        randomVarName = randomVarNames[i]
        randomVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarName)
        ri = len(randomVarValues)
        parents = oxnet.getRandomVarParents(randomVarName, graph)
        qi = getQi(parents)
        for j in range (0, qi):  # j parent of random var
            MijList = []
            try:
                randomVarParentName = parents[j]
                parentVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarParentName)
                for parentVarValue in parentVarValues:
                    querySubList = []
                    for randomVarValue in randomVarValues:
                        queries = [(randomVarParentName, parentVarValue), (randomVarName, randomVarValue)]
                        querySubList.append(queries)
                    count = getJointOccurranceCount(dataframe, querySubList)
                    MijList.append(count)
            except:             # k iteration for nodes that dont have a parent
                # print "EXCEPT"
                queryList = []
                querySubList = []
                for randomVarValue in randomVarValues:
                    noParentQuery = [(randomVarName, randomVarValue)]
                    querySubList.append(noParentQuery)
                queryList.append(querySubList)
                count = getOccurranceCount(dataframe, queryList)
                MijList.append(count)
            print randomVarName + " Mijk=" + str(MijList)
            values.append((ri, MijList))
    return values

# I: iterator over random variables
def getNumRandomVars(randomVarNames):
    n = len(randomVarNames)
    return n

# J: iterator over random var parents
def getQi(randomVarParents):
    qi = getNumRandmVarParents(randomVarParents)
    if qi == 0:
        qi = 1  # iterate over no parent
    return qi

def getNumRandmVarParents(randomVarParents):
    qi = len(randomVarParents)
    if len(randomVarParents) == 0:
        qi = 0
    return qi

# K: iterator over instances/values of a random variable
def getNumRandomVarValues(dataframe, randomVarName):
    randomVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarName)
    return len(randomVarValues)

# RUN QUERIES: run the queries on the dataframe.  A query filters the dataframe.
# The number of rows in the resulting dataframe is the pattern count we are looking for
# A path from the root to a leaf corresponds to some instantiation of the parents of a random var
# TODO: Thus the depth of the tree is equal to the number of parents of that random var
# A given leaf contains the counts for the values of xi in its sample space, that are conditioned on the instantiation of the parents as specified in the tree
def getOccurranceCount(dataframe, queries):
    # print "QUERIES " + str(queries)
    countList = []
    for query in queries:
        # print "DISJOINT QUERY " + str(query)
        for subQuery in query:
            counts = opanda.getQueryCounts(dataframe, subQuery)
            countList.append(counts)
        # print "DISJOINT COUNT " + str(countList) + " FOR QUERY " + str(query)
    return countList

def getJointOccurranceCount(dataframe, queries):
    # print "QUERIES " + str(queries)
    countList = []
    for query in queries:
        # print "JOINT QUERY " + str(query)
        counts = opanda.getJointQueryCounts(dataframe, query)
        countList.append(counts)
        # print "JOINT COUNT " + str(countList) + " FOR QUERY " + str(query)
    return countList


def getVarNameString(varName):
    return "I=" + str(varName) + " "

def getVarParentString(parentName):
    return "J=" + str(parentName) + " "

def getVarValueString(value):
    return "K=" + str(value) + " "