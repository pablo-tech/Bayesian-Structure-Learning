# Count repetition of patterns
# Helper to graphoscore

import graphoquery as oquery
import graphopanda as opanda


# j represents the unique instantiations of parents: eg full joint distribution of parents
def getNijkCountList(iRandomVar, kValueForVari, jParentVars, varValuesDictionary, dataframe):
    countList = []
    countQueries = getNijkQueries(iRandomVar, kValueForVari, jParentVars, varValuesDictionary)
    # print "countQueries="+str(countQueries)
    if len(countQueries)==1:
        queryResult = opanda.getSingleQueryResult(dataframe, countQueries)
        countList.append(len(queryResult))
    else:
        for query in countQueries:
            queryResult = opanda.getJointQueryResult(dataframe, query)
            count = len(queryResult)
            countList.append(count)
    # print "COUNTS=" + str(countList) + " for Nijk full joint " + str(countQueries)
    return countList

def getNijkQueries(iRandomVar, kValueForVari, jParentVars, varValuesDictionary):
    parentJointDistribution = oquery.getParentsJointDistribution(jParentVars, varValuesDictionary)
    fullJointDistribution = oquery.getJointDistribution(iRandomVar, kValueForVari, parentJointDistribution)
    return fullJointDistribution
