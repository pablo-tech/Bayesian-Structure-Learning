# Operate on Python Pandas dataframe


# PANDAS
try:
    import pandas as pd
except ImportError:
    raise ImportError("PANDAS required for filter()")
except RuntimeError:
    print("PANDAS unable to open")
    raise

# CSV
try:
    import csv
except ImportError:
    raise ImportError("CSV required for read()")
except RuntimeError:
    print("CSV unable to open")
    raise


import graphoquery as oquery

# READ: a dataframe from a CSV inputfile
def read(infile):
    inputDF = getInputDF(infile)
    return inputDF

# READ: get dataframe, inferring columns
def getInputDF(infile):
    inputDF = pd.read_csv(infile, header='infer')
    return inputDF

def getRandomVarNames(dataframe):
    varNames = list(dataframe)
    # print "Var NAMES: " + str(varNames)
    return varNames

### VAR VALUES: get possible values from the dataset
def getUniqueRandomVarValues(dataframe, varName):
    unique = dataframe[varName].unique()
    # print"{} \t\t UNIQUE: \t\t {} ".format(str(varName), str(unique))
    return unique

### VAR DICTIONARY: get dictionary of every random var and their possible values
# output: {'x2': array([0, 1]), 'x3': array([0, 1]), 'x1': array([1, 0])}
def getRandomVarDictionary(dataframe):
    varValuesDict = {}
    varNames = getRandomVarNames(dataframe)
    for name in varNames:
        varValuesDict[name] =  getUniqueRandomVarValues(dataframe, name)
    return varValuesDict

# COUNT: count number of pattern repeats by filtering a dataframe and counting how many rows are left
def getQueryCounts(dataframe, queryArray):
    queryTuple = queryArray[0]
    filteredDF = queryDataframe(dataframe, queryTuple)
    count = len(filteredDF)
    return count

# def getJointQueryCounts(dataframe, queryArray):
#     filteredDF = dataframe
#     fieldNames = []
#     for queryTuple in queryArray:
#         filteredDF = queryDataframe(filteredDF, queryTuple)
#         fieldNames.append(queryTuple[0])
#     finalDF = filteredDF[fieldNames]
#     count = len(finalDF)
#     return count

# JOINT QUERY RESULT
# execute queries in the array one by one to arrive at a filtered dataframe
def getJointQueryResult(dataframe, queryArray):
    print "getJointQueryResult query: " + str(queryArray) + " " + str(len(queryArray))
    filteredDF = dataframe
    fieldNames = []
    if len(queryArray)>1: # random var has parents
        for querySingle in queryArray:
            print "querySingle query: " + str(querySingle) + " " + str(len(querySingle))
            for queryTuple in querySingle:
                print "queryTuple query: " + str(queryTuple) + " " + str(len(queryTuple))
                updatedTuple = [queryTuple[0], queryTuple[1]]
                print "WITH PARENT QUERY TUPLE: " + str(updatedTuple)
                filteredDF = queryDataframe(filteredDF, updatedTuple)
                print "filteredDF " + str(filteredDF)
                fieldNames.append(queryTuple[0])
        print "COLUMN FILTER: " + str(fieldNames) + " FOR DF " + str (filteredDF)
        finalDF = filteredDF[fieldNames]
    else:
        queryTuple = oquery.getFlatendList(queryArray)
        print "NO PARENT QUERY TUPLE: " + str(queryTuple)
        finalDF = queryDataframe(dataframe, queryTuple)
    return finalDF

# FILTER: reduce the dataframe to the rows that match a query, with only the columns that match the query
# queryArray = [('age', 1), ('sex', 2)]
def queryDataframe(dataframe, tuple):
    print "FINAL QUERY TUPLE " + str(tuple)
    filteredDF = dataframe
    field_name = tuple[0]
    field_value = tuple[1]
    print "FIELD NAME: " + str(field_name) + " FIELD VALUE " + str(field_value)
    if field_name in getRandomVarNames(dataframe):
        filteredDF = filteredDF.loc[(filteredDF[field_name] == field_value)]
        return filteredDF
    else:   # skip filtering vars that are not present in the already filtered dataframe
        return dataframe

