# Calculate the Bayesian score of a network against a dataset


import graphopanda as opanda
import graphoxnet as oxnet


############
# SCORE: get score using factors, or sums of logs
def getScore(graph, dataframe, label):
    return getCooperHerscovitsBayesianScore(graph, dataframe, label)
    # return getLogCooperHerscovitsBayesianScore(graph, dataframe, label)


# SCORING WITH FACTORS: Cooper & Herscovits, page 320, formula 8
# It is the same as Decisions under Uncertainty, page 47, formula 2.80
# Posterior probability: is proportional to the prior probability
# Cancelling out: prior probability cancels out when two networks are compared by division
# Example: if Score(network1)/Score(network2)>1 then network1 is better representation of the data
def getCooperHerscovitsBayesianScore(graph, dataframe, label):
    score = 1
    values = iterateThroughCombinations(graph, dataframe, label)
    print "VALUES: " + str(values)
    return score


# SCORING WITH SUMS: Decisions Under Uncertainty, page 47, formula, formula 2.83
# Posterior probability: is incremental to prior probability
# Cancelling out: prior probability cancels out when two networks are compared by subtraction
# Example: if Score(network1)-Score(network2)>0 then network1 is a better
def getLogCooperHerscovitsBayesianScore(graph, dataframe, label):
    score = 0
    values = iterateThroughCombinations(graph, dataframe, label)
    print "VALUES: " + str(values)
    return score

# ITERATE: iterates through i=(1:n), j=(1:qi), k=(1:ri)
# Returns the values necessary to compute the Bayesian score
# NOTE: Python uses 0-based indexing!!!
def iterateThroughCombinations(graph, dataframe, label):
    values = [] # used to return all the necessary values to compute the Bayesian score
    randomVarNames = opanda.getRandomVarNodeNames(dataframe)
    n = len(randomVarNames)
    for i in range(0, n):  # i random var
        randomVarName = randomVarNames[i]
        randomVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarName)
        parents = oxnet.getRandomVarParents(randomVarName, graph)
        qi = len(parents)
        if len(parents)==0:
            qi = 1
        for j in range (0, qi):  # j parent of random var
            try:
                randomVarParentName = parents[j]
                parentVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarParentName)
            except:
                randomVarParentName = ""
                parentVarValues = []
                # print randomVarName + " has no parents!"
            ri = len(randomVarValues)
            queries = getIJquery(randomVarName, randomVarValues, randomVarParentName, parentVarValues)
            MijList = getOccurranceCount(dataframe, queries)
            print randomVarName + " Mijk=" + str(MijList) + " i=" + str(i) + " " + " FOR QUERIES " + str(queries)
            values.append((ri, MijList))
    return values


# RUN QUERIES: run the queries on the dataframe.  A query filters the dataframe.
# The number of rows in the resulting dataframe is the pattern count we are looking for
# A path from the root to a leaf corresponds to some instantiation of the parents of a random var
# TODO: Thus the depth of the tree is equal to the number of parents of that random var
# A given leaf contains the counts for the values of xi in its sample space, that are conditioned on the instantiation of the parents as specified in the tree
def getOccurranceCount(dataframe, queries):
    # print "QUERIES " + str(queries)
    countList = []
    for query in queries:
        print "QUERY " + str(query)
        countSubList=[]
        for subQuery in query:
            counts = opanda.getQueryCounts(dataframe, subQuery)
            countSubList.append(counts)
            print "SUBQUERY " + str(subQuery) + " " + str(countSubList)
        countList.append(countSubList)
    # print "COUNT LIST " + str(countList) + " FOR QUERIES " + str(queries)
    return countList

# GENERATE QUERIES: create a list of filtering queries to run against the dataframe.
# Does the k iteration in the Bayesian score here
#     testQuery = [('age', 1), ('sex', 1)]
def getIJquery(randomVarName, randomVarValues, randomVarParentName, parentVarValues):
    queryList = []
    # K iterations
    if len(parentVarValues)!=0:               # random var has parent
        querySubList = []
        for parentVarValue in parentVarValues:
            for randomVarValue in randomVarValues:
                querySubList.append([(randomVarParentName, parentVarValue), (randomVarName, randomVarValue)])
    if len(parentVarValues)==0:                 # random var has no parents
        querySubList = []
        for randomVarValue in randomVarValues:
            noParentQuery = [(randomVarName, randomVarValue)]
            querySubList.append(noParentQuery)
    queryList.append(querySubList)
    # print "IJK QUERIES: " + str(queryList)
    return queryList


def getVarNameString(varName):
    return "I=" + str(varName) + " "

def getVarParentString(parentName):
    return "J=" + str(parentName) + " "

def getVarValueString(value):
    return "K=" + str(value) + " "