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
    for randomVarName in opanda.getRandomVarNodeNames(dataframe):  # i random var
        # print getVarNameString(randomVarName)
        parents = oxnet.getRandomVarParents(randomVarName, graph)
        if len(parents)==0:
            print randomVarName + " has no parents!"
        for randomVarParent in parents:  # j parent of random var
            # print getVarParentString(randomVarParent)
            for valueOfRandomVar in opanda.getUniqueRandomVarValues(dataframe, randomVarName):  # k value of random var
                print label + " " + getVarNameString(randomVarName) + getVarParentString(randomVarParent) + getVarValueString(valueOfRandomVar)
    return score


# SCORING WITH SUMS: Decisions Under Uncertainty, page 47, formula, formula 2.83
# Posterior probability: is incremental to prior probability
# Cancelling out: prior probability cancels out when two networks are compared by subtraction
# Example: if Score(network1)-Score(network2)>0 then network1 is a better
def getLogCooperHerscovitsBayesianScore(graph, dataframe, label):
    score = 0
    for randomVarName in opanda.getRandomVarNodeNames(dataframe):  # i random var
        # print getVarNameString(randomVarName)
        parents = oxnet.getRandomVarParents(randomVarName, graph)
        if len(parents)==0:
            print randomVarName + " has no parents!"
        for randomVarParent in parents:  # j parent of random var
            # print getVarParentString(randomVarParent)
            for valueOfRandomVar in opanda.getUniqueRandomVarValues(dataframe, randomVarName):  # k value of random var
                print label + " " + getVarNameString(randomVarName) + getVarParentString(randomVarParent) + getVarValueString(valueOfRandomVar)
    return score

def getVarNameString(varName):
    return "I=" + str(varName) + " "

def getVarParentString(parentName):
    return "J=" + str(parentName) + " "

def getVarValueString(value):
    return "K=" + str(value) + " "