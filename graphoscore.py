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
    # print "LOG FORM? " + str(logForm)
    score = getBaseScore(logForm)
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
        print "NijkDict: " + str(NijkAll)
        varAndParentAggregateConsideration = getRandomVarAndParentAggregateConsideration(Ri, NijkAll, logForm)
        # print "varAndParentAggregateConsideration: " + str(varAndParentAggregateConsideration)
        # varValuesIndividualConsideration = getRandomVarAndParentIndividualConsideration(NijkAll, logForm)
        # print "varValuesIndividualConsideration: " + str(varValuesIndividualConsideration)
        AggregateConsiderationList.append(varAndParentAggregateConsideration)
        # IndividualConsiderationList.append(varValuesIndividualConsideration)
    if not logForm: # multiply
        for aggregate in AggregateConsiderationList:
            score = score * aggregate
        for individual in IndividualConsiderationList:
            score = score * individual
        print "TOTAL=>"+str(score)
    else:           # add
        for aggregate in AggregateConsiderationList:
            score = score + aggregate
        for individual in IndividualConsiderationList:
            score = score + individual
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
def getRandomVarAndParentAggregateConsideration(Ri, NijkAll, logForm):
    numParentValues = len(NijkAll[0])
    print "numParentValues " + str(numParentValues) + " for " + str(NijkAll)
    # get a list to process that looks the same for one or many parents:
    # one parent: [[5, 5]]
    # many parents = [[4, 1], [1, 4]]
    if numParentValues==1:
        NijkListOfLists = [oquery.getFlatendList(NijkAll)]
    else: NijkListOfLists = NijkAll
    print "NijkListOfLists " + str(NijkListOfLists)
    numerator = Ri-1
    numeratorFactorial = math.factorial(numerator)            # Dirichlet Prior (all pseudocounts = 1) for a random var
    for NijkSingleList in NijkListOfLists:
        denominator = Ri - 1
        for Nijk in NijkSingleList: # oquery.getFlatendList(NijkSingleList)
            print str(Nijk) + " in NijkSingleList " + str(NijkSingleList)
            denominator = denominator + Nijk    # add Nijk values to Ri term
        print "AGGREGATE>>>>>>Numerator=" + str(numerator) + " >>>>>>Denominator=" + str(denominator) + " FROM NijkSingleList=" + str(NijkSingleList)
        denominatorFactorial = math.factorial(denominator)
        if not logForm:
            return float(numeratorFactorial) / float(denominatorFactorial)  # NOTE this may round to ZERO!
        else:
            return math.log(numeratorFactorial) - math.log(denominatorFactorial)

# VAR AND PARENT VAR INDIVIDUAL FACTORS
def getRandomVarAndParentIndividualConsideration(NijkDict, logForm):
    #print "Individual NijkValues="+str(NijkValues)
    # flatValues = oquery.getFlatendList(NijkValues)
    #print "Consideration NijkValues " + str(flatValues)
    numerator = getBaseScore(logForm)
    for Nijk in list(NijkDict.keys()):
        factor = math.factorial(Nijk)
        if not logForm:
            numerator = numerator * factor
        else:
            numerator = numerator + math.log(factor)
    #print "INDIVIDUAL<<<<<<<<Numerator="+str(numerator) + " " + str(NijkValues) + " TOTAL="+str(numerator)
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
