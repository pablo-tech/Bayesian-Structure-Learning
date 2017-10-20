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
def getParentsJointDistribution(parentRandomVars, varValuesDictionary):
    print "joint dictionary " + str(varValuesDictionary)
    parentJointDistribution = []
    iteration = 0
    firstVar = ""
    for parentName in parentRandomVars:
        if iteration==0:    # do the first var by itself
            firstVar = parentName
            parentJointDistribution = getVarDistribution(parentName, varValuesDictionary)
        if iteration==1:
            secondVar = parentName
            firstTwoVarJoint = getPairQueryDistribution(firstVar, varValuesDictionary[firstVar], secondVar, varValuesDictionary[secondVar])
            parentJointDistribution = firstTwoVarJoint
            #print "firstTwoVarJoint " + str(firstTwoVarJoint)
        if iteration!=0:
            if iteration!=1:
                # start fresh
                newJoins = []
                savedTwoVarDistribution = parentJointDistribution
                parentJointDistribution = []
                # join to result of first two var joins
                for parentValue in varValuesDictionary[parentName]:
                    joined = getJointDistribution(parentName, parentValue, savedTwoVarDistribution)
                    toAppend = joined
                    newJoins.append(toAppend)
                outerAppend = getFlatendList(newJoins)
                parentJointDistribution.append(outerAppend)
                parentJointDistribution = getFlatendList(parentJointDistribution)
                # print "parentJointDistribution " + str(parentJointDistribution)
        iteration = iteration + 1
    return parentJointDistribution

# FLATEN:
# output: [180.0], [173.8], [164.2], [156.5], [147.2], [138.2]
# input: [[180.0], [173.8], [164.2], [156.5], [147.2], [138.2]]
def getFlatendList(listOfLists):
    flattened = []
    for sublist in listOfLists:
        for val in sublist:
            flattened.append(val)
    return flattened

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
        dist.append([(varName,value)])
    return dist

# input: ("x2", ['1', '2'], "x1", ['3', '4'])
# output: [[('x2', '1'), ('x1', '3')], [('x2', '1'), ('x1', '4')], [('x2', '2'), ('x1', '3')], [('x2', '2'), ('x1', '4')]]
def getPairQueryDistribution(randomVar1, randomVar1Values, randomVar2, randomVar2Values):
    queryList = []
    for valueRandomVar1 in randomVar1Values:
        for valueRandomVar2 in randomVar2Values:
            query = getPairQuery(randomVar1, valueRandomVar1, randomVar2, valueRandomVar2)
            queryList.append(query)
    return queryList

# QUERY BUILDER: Build a query for two vars
# queryArray = [('age', 1), ('sex', 2)]
# [(randomVarParentName, parentVarValue), (randomVarName, randomVarValue)]
def getPairQuery(randomVar1, randomVar1Value, randomVar2, randomVar2Value):
    query = [(randomVar1, randomVar1Value), (randomVar2, randomVar2Value)]
    # print "returning " + str(query)
    return query


