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
def getScore(graph, dataframe, label):
    ### Log Cooper & Herscovitz
    # logCooperHerscovitsScore = getUpdatedCooperHerscovitsBayesianScore(graph, dataframe, label, True)
    updatedCooperHerscovitsScore = getUpdatedCooperHerscovitsBayesianScore(graph, dataframe, label, False)
    ### Log Bayesian score
    # logBayesianScore = getLogBayesianScore(graph, dataframe, label)
    ### Cooper & Herscovitz
    # cooperHerscovitsScore = getCooperHerscovitsBayesianScore(graph, dataframe, label)
    # print "COOPER HERRSCOVITS SCORE: " + str(cooperHscore)
    return updatedCooperHerscovitsScore

# SCORING WITH FACTORS: Cooper & Herscovits, page 320, formula 8
# It is the same as Decisions under Uncertainty, page 47, formula 2.80
# Posterior probability: is proportional to the prior probability
# Cancelling out: prior probability cancels out when two networks are compared by division
# Example: if Score(network1)/Score(network2)>1 then network1 is better representation of the data
def getUpdatedCooperHerscovitsBayesianScore(graph, dataframe, label, logForm):
    score = getBaseScore(logForm)
    randomVarNames = opanda.getRandomVarNames(dataframe)
    varValuesDictionary = opanda.getRandomVarDictionary(dataframe)
    print ">>> " + str(varValuesDictionary)
    N = getN(randomVarNames)
    for i in range(0, N):  # i random var
        iRandomVarName = randomVarNames[i]
        Ri = getNumRandomVarValues(dataframe, iRandomVarName)
        iRandomVarParents = oxnet.getRandomVarParents(iRandomVarName, graph)
        Qi = getQi(iRandomVarParents, varValuesDictionary)
        # for j in range(0, Qi):  # j values taken by parents of ranom var i ... handled by joint distribution queries
        for k in range(0, Ri):
            iRandomVarValues = opanda.getUniqueRandomVarValues(dataframe, iRandomVarName)
            kValueForRandomVari = iRandomVarValues[k]
            NijkList = ocount.getNijkCountList(iRandomVarName, kValueForRandomVari, iRandomVarParents, varValuesDictionary, dataframe)
            varAndParentAggregateConsideration = getRandomVarAndParentAggregateConsideration(Ri, NijkList, logForm)
            varValuesIndividualConsideration = getRandomVarAndParentIndividualConsideration(NijkList, logForm)
    if not logForm:
        productorialTotal = varAndParentAggregateConsideration * varValuesIndividualConsideration
        print "TOTAL=>"+str(score)+"*" + str(productorialTotal)
        score = score * productorialTotal
    else:
        sumatorialConsideration = varAndParentAggregateConsideration + varValuesIndividualConsideration
        print "TOTAL=>"+str(score)+"+" + str(sumatorialConsideration)
        score = score + sumatorialConsideration
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
def getRandomVarAndParentAggregateConsideration(Ri, NijValues, logForm):
    # flatValues = oquery.getFlatendList(NijValues)
    numerator = Ri-1
    denominator = Ri-1
    for nijk in NijValues:
        denominator = denominator + nijk
    print "AGGREGATE>>>>>>Numerator=" + str(numerator) + " >>>>>>Denominator=" + str(denominator) + " FROM NijkList=" + str(NijValues)
    numeratorFactorial = math.factorial(numerator)            # Dirichlet Prior (all pseudocounts = 1) for a random var
    denominatorFactorial = math.factorial(denominator)
    if not logForm:
        return float(numeratorFactorial) / float(denominatorFactorial)  # NOTE this may round to ZERO!
    else:
        return math.log(numeratorFactorial) - math.log(denominatorFactorial)

# VAR AND PARENT VAR INDIVIDUAL FACTORS
def getRandomVarAndParentIndividualConsideration(NijkValues, logForm):
    print "Individual NijkValues="+str(NijkValues)
    # flatValues = oquery.getFlatendList(NijkValues)
    #print "Consideration NijkValues " + str(flatValues)
    numerator = getBaseScore(logForm)
    for Nijk in NijkValues:
        factor = math.factorial(Nijk)
        if not logForm:
            numerator = numerator * factor
        else:
            numerator = numerator + math.log(factor)
    print "INDIVIDUAL<<<<<<<<Numerator="+str(numerator) + " " + str(NijkValues) + " TOTAL="+str(numerator)
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
    print str(qi) + "=LENGTH FOR DISTRIBUTION \n" + str(parentsDistribution)
    # qi = oquery.getParentsJointDistribution
    # for parent in randomVarParents:
    #     for value in varValuesDictionary[parent]
    #     qi = getNumRandmVarParents(randomVarParents)+1
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

# ==================

# # SCORING WITH FACTORS: Cooper & Herscovits, page 320, formula 8
# # It is the same as Decisions under Uncertainty, page 47, formula 2.80
# # Posterior probability: is proportional to the prior probability
# # Cancelling out: prior probability cancels out when two networks are compared by division
# # Example: if Score(network1)/Score(network2)>1 then network1 is better representation of the data
# def getCooperHerscovitsBayesianScore(graph, dataframe, label):
#     score = float(1)
#     values = iterateThroughCombinations(graph, dataframe, label)
#     print ">>>>> VALUES: " + str(values)
#     # >>>>> VALUES: [(2, [[5, 5]]), (2, [[1, 4], [4, 1]]), (2, [[4, 1], [0, 5]])]
#     #
#     for value in values:
#         print "*********************************** COMPUTING VALUE: " + str(value)
#         # *********************************** COMPUTING VALUE: (2, [[5, 5]])
#         # *********************************** COMPUTING VALUE: (2, [[1, 4], [4, 1]])
#         # *********************************** COMPUTING VALUE: (2, [[4, 1], [0, 5]])
#         #
#         # NUMERATOR
#         # Gamma(alphaIJ)
#         alphaIJ0 = value[0]-1   # Design under uncertainty equation 2.80
#         print "alphaIJ0=" + str(alphaIJ0)
#         alphaIJ0Factorial = math.factorial(alphaIJ0)
#         print "alphaIJ0Factorial=" + str(alphaIJ0Factorial)
#         score = score * alphaIJ0Factorial
#         print "score=" + str(score)
#         # mIJK numerator
#         for mValues in value[1]:
#             print "COUNT VALUE " + str(mValues)
#             print "the values mValues=" + str(mValues)
#             print "############################# mValues=" + str(mValues)
#             # ############################# mValues=[5, 5]
#             # ############################# mValues=[1, 4]
#             # ############################# mValues=[4, 1]
#             # ############################# mValues=[4, 1]
#             # ############################# mValues=[0, 5]
#             for m in mValues:      # Design under uncertainty equation 2.80
#                 print "====COMPUTING M: " + str(m)
#                 print "m=" + str(m)
#                 mFactorial = math.factorial(m)
#                 print "mFactorial=" + str(mFactorial)
#                 score = score * mFactorial
#                 print "score=" + str(score)
#             print "all numerator score=" + str(score)
#             # DENOMINATOR
#             mAdjustedIJ0 = alphaIJ0;
#             print "reset mAdjustedIJ0=" + str(mAdjustedIJ0)
#             for m in mValues:      # Design under uncertainty equation 2.80
#                 print "====COMPUTING DENOMINATOR: " + str(m)
#                 print "m=" + str(m)
#                 mAdjustedIJ0 = mAdjustedIJ0 + m
#                 print "mAdjustedIJ0=" + str(mAdjustedIJ0)
#             mfinalIJ0 = mAdjustedIJ0
#             print "final mAdjustedIJ0=" + str(mAdjustedIJ0)
#             mAdjustedIJ0Factorial = math.factorial(mfinalIJ0)
#             print "mAdjustedIJ0Factorial=" + str(mAdjustedIJ0Factorial)
#             score = score / mAdjustedIJ0Factorial
#             print "all denominator score=" + str(score)
#     return score


# # SCORING WITH FACTORS: Decisions Under Uncertainty, page 47, formula 2.83
# # Posterior probability: is proportional to the prior probability
# # Cancelling out: prior probability cancels out when two networks are compared by division
# # Example: if Score(network1)-Score(network2)>0 then network1 is better representation of the data
# def getLogBayesianScore(graph, dataframe, label):
#     score = float(0)
#     values = iterateThroughCombinations(graph, dataframe, label)
#     alphaIJ0list = getAlphaij0Hyperparam(values)
#     mij0list = getMij0GroupedCount(values)
#     # print "groupled mij0: " + str(mij0list)
#     randomVarNames = opanda.getRandomVarNames(dataframe)
#     for i in range(0, getNumRandomVars(randomVarNames)):
#         # print "i= " + str(i)
#         randomVarName = randomVarNames[i]
#         parents = oxnet.getRandomVarParents(randomVarName, graph)
#         qi = getQi(parents)
#         for j in range(0, qi):
#             # print "j= " + str(j)
#             # sum over random vars and parents
#             numeratorAlpha = alphaIJ0list[i]-1
#             # print str(i) + " numeratorAlpha " + str(numeratorAlpha)
#             numeratorFactorialAlpha = math.factorial(numeratorAlpha)
#             # print str(i) + " numeratorFactorialAlpha " + str(numeratorFactorialAlpha)
#             denominatorAlphaCount = numeratorAlpha
#             # print "denominatorAlphaCount INIT " + str(denominatorAlphaCount)
#             for mijkSublistList in mij0list[i]:
#                 # print "actual sub mijkList: " + str(mijkSublistList)
#                 for mijk in mijkSublistList:
#                     # print ">>> mijk: " + str(count)
#                     denominatorAlphaCount = denominatorAlphaCount + mijk
#                     # print str(i) + " last term mijk count " + str(mijk)
#             denominatorFactorialCount = math.factorial(denominatorAlphaCount)
#             # print str(i) + " denominatorFactorialCount " + str(denominatorFactorialCount)
#             score = math.log(numeratorFactorialAlpha) - math.log(denominatorFactorialCount)
#             # print "***UPDATED score: " + str(score) + " WITH alphaCount " + str(denominatorAlphaCount) + " and mijkList " + str(mij0list[i])
#             ri = getNumRandomVarValues(dataframe, randomVarName)
#             # iterate over the k values of random var
#             for mijkSubList in mij0list[i]:
#                 # print "*mijk " + str(mijk)
#                 factorialMijk = math.factorial(mijk)
#                 # print "factorial *mijk " + str(factorialMijk)
#                 score = score + math.log(factorialMijk)
#                 # print "$$$UPDATED score: " + str(score) + " with mijkSubList " + str(mijkSubList)
#     return score
#
#
# # ri: the number of values each random var takes
# def getAlphaij0Hyperparam(values):
#     Alphaij = []
#     for value in values:
#         alpha = value[0]
#         # print "alpha=" + str(alpha)
#         Alphaij.append(alpha)
#     return Alphaij
#
# # Mij0
# # the number of times a random var takes a value, given it's parents
# def getMij0Count(values):
#     Mij0 = []
#     for value in values:
#         for m in value[1]:
#             # print "m=" + str(m)
#             Mij0.append(m)
#     return Mij0
#
# def getMij0GroupedCount(values):
#     Mij0 = []
#     for value in values:
#         Mijk = []
#         for m in value[1]:
#             # print "m=" + str(m)
#             Mijk.append(m)
#         Mij0.append(Mijk)
#     return Mij0


# # ITERATE: iterates through i=(1:n), j=(1:qi), k=(1:ri)
# # Returns the values necessary to compute the Bayesian score
# # NOTE: Python uses 0-based indexing!!!
# def iterateThroughCombinations(graph, dataframe, label):
#     values = [] # used to return all the necessary values to compute the Bayesian score
#     randomVarNames = opanda.getRandomVarNames(dataframe)
#     n = getNumRandomVars(randomVarNames)
#     for i in range(0, n):  # i random var
#         randomVarName = randomVarNames[i]
#         randomVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarName)
#         ri = len(randomVarValues)
#         parents = oxnet.getRandomVarParents(randomVarName, graph)
#         qi = getQi(parents)
#         for j in range (0, qi):  # j parent of random var
#             MijList = []
#             try:
#                 randomVarParentName = parents[j]
#                 parentVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarParentName)
#                 for parentVarValue in parentVarValues:
#                     querySubList = []
#                     for randomVarValue in randomVarValues:
#                         queries = [(randomVarParentName, parentVarValue), (randomVarName, randomVarValue)]
#                         querySubList.append(queries)
#                     count = getJointOccurranceCount(dataframe, querySubList)
#                     MijList.append(count)
#             except:             # k iteration for nodes that dont have a parent
#                 # print "EXCEPT"
#                 queryList = []
#                 querySubList = []
#                 for randomVarValue in randomVarValues:
#                     noParentQuery = [(randomVarName, randomVarValue)]
#                     querySubList.append(noParentQuery)
#                 queryList.append(querySubList)
#                 count = getOccurranceCount(dataframe, queryList)
#                 MijList.append(count)
#             # print randomVarName + " Mijk=" + str(MijList)
#             values.append((ri, MijList))
#     return values



# # RUN QUERIES: run the queries on the dataframe.  A query filters the dataframe.
# # The number of rows in the resulting dataframe is the pattern count we are looking for
# # A path from the root to a leaf corresponds to some instantiation of the parents of a random var
# # TODO: Thus the depth of the tree is equal to the number of parents of that random var
# # A given leaf contains the counts for the values of xi in its sample space, that are conditioned on the instantiation of the parents as specified in the tree
# def getOccurranceCount(dataframe, queries):
#     # print "QUERIES " + str(queries)
#     countList = []
#     for query in queries:
#         # print "DISJOINT QUERY " + str(query)
#         for subQuery in query:
#             counts = opanda.getQueryCounts(dataframe, subQuery)
#             countList.append(counts)
#         # print "DISJOINT COUNT " + str(countList) + " FOR QUERY " + str(query)
#     return countList
#
# def getJointOccurranceCount(dataframe, queries):
#     # print "QUERIES " + str(queries)
#     countList = []
#     for query in queries:
#         # print "JOINT QUERY " + str(query)
#         counts = opanda.getJointQueryCounts(dataframe, query)
#         countList.append(counts)
#         # print "JOINT COUNT " + str(countList) + " FOR QUERY " + str(query)
#     return countList


def getVarNameString(varName):
    return "I=" + str(varName) + " "

def getVarParentString(parentName):
    return "J=" + str(parentName) + " "

def getVarValueString(value):
    return "K=" + str(value) + " "