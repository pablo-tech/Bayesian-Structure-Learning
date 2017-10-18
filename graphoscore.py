# Calculate the Bayesian score of a network against a dataset


import graphopanda as opanda
import graphoxnet as oxnet


############
# SCORE: get score using factors, or sums of logs
def getScore(graph, dataframe):
    return getCooperHerscovitsBayesianScore(graph, dataframe)
    # return getLogCooperHerscovitsBayesianScore(graph, dataframe)


# SCORING WITH FACTORS: Cooper & Herscovits, page 320, formula 8
# It is the same as Decisions under Uncertainty, page 47, formula 2.80
# Posterior probability: is proportional to the prior probability
# Cancelling out: prior probability cancels out when two networks are compared by division
# Example: if Score(network1)/Score(network2)>1 then network1 is better representation of the data
def getCooperHerscovitsBayesianScore(graph, dataframe):
    score = 1
    for randomVarName in opanda.getRandomVarNodeNames(dataframe):  # i random var
        print "I: " + randomVarName
        for randomVarParent in oxnet.getRandomVarParents(randomVarName, graph):  # j parent of random var
            print "J: " + randomVarParent
            for valueOfRandomVar in opanda.getUniqueRandomVarValues(dataframe, randomVarName):  # k value of random var
                print "K: " + valueOfRandomVar
    return score


# SCORING WITH SUMS: Decisions Under Uncertainty, page 47, formula, formula 2.83
# Posterior probability: is incremental to prior probability
# Cancelling out: prior probability cancels out when two networks are compared by subtraction
# Example: if Score(network1)-Score(network2)>0 then network1 is a better
def getLogCooperHerscovitsBayesianScore(graph, dataframe):
    score = 0
    for randomVarName in opanda.getRandomVarNodeNames(dataframe):  # i random var
        print "I: " + randomVarName
        for randomVarParent in oxnet.getRandomVarParents(randomVarName, graph):  # j parent of random var
            print "J: " + randomVarParent
            for valueOfRandomVar in opanda.getUniqueRandomVarValues(dataframe, randomVarName):  # k value of random var
                print "K: " + valueOfRandomVar
    return score
