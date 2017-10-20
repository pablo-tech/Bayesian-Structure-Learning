# Helper functions to compute score

def getNijkForIteration(i, j, k):
    return 1


# def getNijkQueries(iRandomVar, kValueForRandomVari):
#     queries = []
#     for



# QUERY BUILDER: Build a query for the iteration
# queryArray = [('age', 1), ('sex', 2)]
# [(randomVarParentName, parentVarValue), (randomVarName, randomVarValue)]
def getNijCount(iVar, kValueForVari, jParentVar, valueForParentj):
    query = [(iVar, kValueForVari), (jParentVar, valueForParentj)]
    print "returning " + str(query)
    return query

# PARENT DISTRIBUTION
# Get queries for all parent value combinations
# def getParentVarDistribution(randomVarParentsDictionary):
#     queryDistribution = []
#     for parent in list(randomVarParentsDictionary.keys()):
#         for valueForParent in randomVarParentsDictionary[parent]:
#             getParentQueries = getPairQueryDistribution()


# PARENTS JOINT DISTRIBUTION: get a full joint distribution
# it joins all the vars in the dictionary, except the ignore var(i var in question), to produce a distribution of parents
def getParentsJointDistribution(randomVar, parentRandomVars, varValuesDictionary):
    print "joint dictionary " + str(varValuesDictionary)
    parentJointDistribution = []
    allVarNames = list(varValuesDictionary.keys())
    iteration = 0
    for varName in allVarNames:
        if varName!=randomVar:
            if varName in parentRandomVars:
                print "parent var: " + str(varName)
                if iteration==0:    # do the first var by itself
                    parentJointDistribution = getVarDistribution(varName, varValuesDictionary)
                    iteration = iteration + 1
                else:               # do the other vars against the first
                    newJoins = []
                    for varValue in varValuesDictionary[varName]:
                        newJoins.append(getJointDistribution(varName, varValue, parentJointDistribution))
                    parentJointDistribution.append(newJoins)
    return parentJointDistribution


# PARTIAL JOINT DISTRIBUTION: for a specific value of a random var
# get a joint distribution from a (varName,varValue) tuple and a distribution of other vars
# input, per: "x3", 9, [[('x2', '1'), ('x1', '3')], [('x2', '1'), ('x1', '4')], [('x2', '2'), ('x1', '3')], [('x2', '2'), ('x1', '4')]]
# output: [[('x3', 9), ('x2', '1'), ('x1', '3')], [('x3', 9), ('x2', '1'), ('x1', '4')], [('x3', 9), ('x2', '2'), ('x1', '3')], [('x3', 9), ('x2', '2'), ('x1', '4')]]
def getJointDistribution(randomVarName, randomVarValue, otherVarsDistribution):
    jointDistribution = []
    randomVar = (randomVarName, randomVarValue)
    for otherOutcome in otherVarsDistribution:
        joinedOutcome = []
        joinedOutcome.append(randomVar)
        for item in otherOutcome:
            joinedOutcome.append(item)
        jointDistribution.append(joinedOutcome)
    return jointDistribution

# SINGLE VAR DISTRIBUTION
# output [('x1', 1), ('x1', 0)]
# input: {'x2': array([0, 1]), 'x3': array([0, 1]), 'x1': array([1, 0])}
def getVarDistribution(varName, varValueDict):
    dist = []
    for value in varValueDict[varName]:
        dist.append((varName,value))
    return dist

# # input: ("x2", ['1', '2'], "x1", ['3', '4'])
# # output: [[('x2', '1'), ('x1', '3')], [('x2', '1'), ('x1', '4')], [('x2', '2'), ('x1', '3')], [('x2', '2'), ('x1', '4')]]
# def getPairQueryDistribution(randomVar1, randomVar1Values, randomVar2, randomVar2Values):
#     queryList = []
#     for valueRandomVar1 in randomVar1Values:
#         for valueRandomVar2 in randomVar2Values:
#             query = getPairQuery(randomVar1, valueRandomVar1, randomVar2, valueRandomVar2)
#             queryList.append(query)
#     return queryList

# QUERY BUILDER: Build a query for two vars
# queryArray = [('age', 1), ('sex', 2)]
# [(randomVarParentName, parentVarValue), (randomVarName, randomVarValue)]
def getPairQuery(randomVar1, randomVar1Value, randomVar2, randomVar2Value):
    query = [(randomVar1, randomVar1Value), (randomVar2, randomVar2Value)]
    # print "returning " + str(query)
    return query


