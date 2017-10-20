# Count repetition of patterns
# Helper to graphoscore

import graphoquery as oquery
import graphopanda as opanda


def getNij0(iRandomVar, jParentVars, varValuesDictionary, dataframe):
    iVarValues = varValuesDictionary[iRandomVar]
    total = 0
    for iVarValue in iVarValues:
        total = total + getNijkCount(iRandomVar, iVarValue, jParentVars, varValuesDictionary, dataframe)
    return total

# j represents the unique instantiations of parents: eg full joint distribution of parents
def getNijkCount(iRandomVar, kValueForVari, jParentVars, varValuesDictionary, dataframe):
    print "INPUT: " + str(iRandomVar) + " " + str(kValueForVari) + " " + str(jParentVars) + " " + str(varValuesDictionary)
    countQueries = getNijkQueries(iRandomVar, kValueForVari, jParentVars, varValuesDictionary)
    print "Count queries: " + str(countQueries)
    queryResult = opanda.getJointQueryResult(dataframe, countQueries)
    count = len(queryResult)
    return count

def getNijkQueries(iRandomVar, kValueForVari, jParentVars, varValuesDictionary):
    parentJointDistribution = oquery.getParentsJointDistribution(jParentVars, varValuesDictionary)
    fullJointDistribution = oquery.getJointDistribution(iRandomVar, kValueForVari, parentJointDistribution)
    print "Nijk full joint " + str(fullJointDistribution)
    return fullJointDistribution
