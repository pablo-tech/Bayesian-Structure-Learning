# Calculate the Bayesian score of a network against a dataset

# PANDAS
try:
    import pandas as pd
except ImportError:
    raise ImportError("PANDAS required for filter()")
except RuntimeError:
    print("PANDAS unable to open")
    raise


############
# GRAPHO components developed
import graphopanda as opanda
import graphoxnet as oxnet
import graphocount as ocount
import graphoquery as oquery

import math

############
# SCORE: get score using factors, or sums of logs
def getScore(graph, dataframe):
    ### Log Cooper & Herscovitz
    logCooperHerscovitsScore = getUpdatedCooperHerscovitsBayesianScore(graph, dataframe)
    # updatedCooperHerscovitsScore = getUpdatedCooperHerscovitsBayesianScore(graph, dataframe, label, False)
    return logCooperHerscovitsScore

# SCORING WITH FACTORS: Cooper & Herscovits, page 320, formula 8
# It is the same as Decisions under Uncertainty, page 47, formula 2.80
# Posterior probability: is proportional to the prior probability
# Cancelling out: prior probability cancels out when two networks are compared by division
# Example: if Score(network1)/Score(network2)>1 then network1 is better representation of the data
def getUpdatedCooperHerscovitsBayesianScore(graph, dataframe):
    logForm = True
    score = 0 # log form
    randomVarNames = opanda.getRandomVarNames(dataframe)
    varValuesDictionary = opanda.getRandomVarDictionary(dataframe)
    print ">>> " + str(varValuesDictionary)
    N = getN(randomVarNames)
    AggregateConsiderationList = []
    IndividualConsiderationList = []
    for i in range(0, N):  # i random var
        iRandomVarName = randomVarNames[i]
        Ri = getNumRandomVarValues(dataframe, iRandomVarName)
        iRandomVarParents = oxnet.getRandomVarParents(iRandomVarName, graph)
        Qi = getQi(iRandomVarParents, varValuesDictionary)
        # for j in range(0, Qi):  # j values taken by parents of random var i ... handled by joint distribution queries
        NijkAll = []
        for k in range(0, Ri):
            iRandomVarValues = opanda.getUniqueRandomVarValues(dataframe, iRandomVarName)
            kValueForRandomVari = iRandomVarValues[k]
            NijkList = ocount.getNijkCountList(iRandomVarName, kValueForRandomVari, iRandomVarParents, varValuesDictionary, dataframe)
            NijkAll.append(NijkList)
        print "NijkALL: " + str(NijkAll)
        score = score + getRandomVarAndParentAggregateConsideration(Ri, NijkAll)
        score = score +getRandomVarAndParentIndividualConsideration(NijkAll)
    print "TOTAL=>"+str(score)
    return score

def getNij0(NijValues):
    flatValues = oquery.getFlatendList(NijValues)
    #print "NijkValues " + str(flatValues)
    total = 0
    for value in flatValues:
        total = total + value
    print "NijkValues " + str(flatValues) + "->TOTAL=" + str(total)
    return total

# VAR AND PARENT AGGREGATE FACTOR: per Cooper & Herscovits
# input NijkAll, random var has no parent: [[5], [5]]
# input NijkAll, random var has parent: [[1, 4], [4, 1]]
def getRandomVarAndParentAggregateConsideration(Ri, NijkAll):
    numerator = Ri-1
    denominatorList = []
    for NijkSingleList in getNijkListOfLists(NijkAll):
        denominator = Ri - 1
        for Nijk in NijkSingleList: # oquery.getFlatendList(NijkSingleList)
            denominator = denominator + Nijk    # add Nijk values to Ri term
            denominatorList.append(denominator)
        print "AGGREGATE>>>>>>Numerator=" + str(numerator) + " >>>>>>Denominator=" + str(denominator) + " FROM NijkSingleList=" + str(NijkSingleList)
    total = 0   # assumes log form
    for denom in denominatorList:       # Dirichlet Prior (all pseudocounts = 1) for a random var
        diff = math.log(math.factorial(numerator))-math.log(math.factorial(denom))
        total = total + diff
        print "total from var and parent " + str(total) + " diff " + str(diff)
    return total

def getNijkListOfLists(NijkAll):
    numParentValues = len(NijkAll[0])
    # get a list to process that looks the same for one or many parents:
    # one parent: [[5, 5]]
    # many parents = [[4, 1], [1, 4]]
    if numParentValues==1:
        NijkListOfLists = [oquery.getFlatendList(NijkAll)]
    else: NijkListOfLists = NijkAll
    print "NijkListOfLists= " + str(NijkListOfLists)
    return NijkListOfLists

# VAR AND PARENT VAR INDIVIDUAL FACTORS
def getRandomVarAndParentIndividualConsideration(NijkAll):
    numerator = 0
    for NijkSingleList in getNijkListOfLists(NijkAll):
        for Nijk in NijkSingleList:
            term = math.factorial(Nijk)
            numerator = numerator + math.log(term)
            print "INDIVIDUAL<<<<<<<<Numerator="+str(Nijk) + " " + str(NijkAll) + " TOTAL="+str(numerator)
    return numerator

def getBaseScore(logForm):
    if not logForm:
        base = float(1)   # multiply neutral
        return base
    else:
        base = float(0)   # add neutral
        return base

# I:0-N iterator over random variables
def getN(randomVarNames):
    return getNumRandomVars(randomVarNames)

def getNumRandomVars(randomVarNames):
    n = len(randomVarNames)
    return n

# J:0-Qi iterator over INSTANTITIONS of random var parents
def getQi(randomVarParents, varValuesDictionary):
    parentsDistribution = oquery.getParentsJointDistribution(randomVarParents, varValuesDictionary)
    qi = len(parentsDistribution)
    #print str(qi) + "=LENGTH FOR DISTRIBUTION \n" + str(parentsDistribution)
    if qi == 0:
        qi = 1  # iterate over var with no parent
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
