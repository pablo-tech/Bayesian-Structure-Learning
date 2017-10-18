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
        parents = oxnet.getRandomVarParents(randomVarName, graph)
        qi = len(parents)
        if len(parents)==0:
            qi = 1
        for j in range (0, qi):  # j parent of random var
            randomVarValues = opanda.getUniqueRandomVarValues(dataframe, randomVarName)
            ri = len(randomVarValues)
            # print "RI " + str(ri) + " FOR " + str(randomVarName) + " FROM " + str(randomVarValues)
            try:
                randomVarParentName = parents[j]
            except:
                randomVarParentName = []
                # print randomVarName + " has no parents!"
            patternCount = []
            for k in range(0, ri):  # k value of random var
                valueOfRandomVar = randomVarValues[k]
                # print label + " " + getVarNameString(randomVarName) + getVarParentString(randomVarParentName) + getVarValueString(valueOfRandomVar)
                if len(randomVarParentName)==0: # random var has no parent
                    score = 1
                else:
                    queries = getIJKqueries(randomVarName, valueOfRandomVar, randomVarParentName, dataframe)
                    Mijk = countPatternOccurrances(dataframe, queries)
                    print "Mijk="+str(Mijk) + " i="+str(i) + " j="+str(j) + " k="+str(k) + " " + " FOR QUERIES " + str(queries)
                    patternCount.append(Mijk)
            values.append((ri, patternCount))
    return values


# RUN QUERIES: run the queries on the dataframe.  A query filters the dataframe.
# The number of rows in the resulting dataframe is the pattern count we are looking for
# A path from the root to a leaf corresponds to some instantiation of the parents of a random var
# TODO: Thus the depth of the tree is equal to the number of parents of that random var
# A given leaf contains the counts for the values of xi in its sample space, that are conditioned on the instantiation of the parents as specified in the tree
def countPatternOccurrances(dataframe, queries):
    count = 0
    for query in queries:
        filteredDF = opanda.queryDataframe(dataframe, query)
        count = count + len(filteredDF)
    # print "COUNT " + str(count) + " FOR QUERIES " + str(queries)
    return count

# GENERATE QUERIES: create a list of filtering queries to run against the dataframe.
#     testQuery = [('age', 1), ('sex', 1)]
def getIJKqueries(randomVarName, valueOfRandomVar, randomVarParentName, dataframe):
    queryList = []
    queryRandomVar = (randomVarName, valueOfRandomVar)
    parentValues = opanda.getUniqueRandomVarValues(dataframe, randomVarParentName)
    for parentValue in parentValues:
        queryParentValue = (randomVarParentName, parentValue)
        queryList.append([queryRandomVar,queryParentValue])
    # print "IJK QUERY: " + str(queryList)
    return queryList


def getVarNameString(varName):
    return "I=" + str(varName) + " "

def getVarParentString(parentName):
    return "J=" + str(parentName) + " "

def getVarValueString(value):
    return "K=" + str(value) + " "