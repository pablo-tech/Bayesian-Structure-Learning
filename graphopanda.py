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


# READ: a dataframe from a CSV inputfile
def read(infile):
    inputDF = getInputDF(infile)
    return inputDF

# READ: get dataframe, inferring columns
def getInputDF(infile):
    inputDF = pd.read_csv(infile, header='infer')
    return inputDF

def getRandomVarNodeNames(dataframe):
    return list(dataframe)

def getUniqueRandomVarValues(dataframe, varName):
    unique = dataframe[varName].unique()
    # print"{} \t\t UNIQUE: \t\t {} ".format(str(varName), str(unique))
    return unique


# COUNT: count number of pattern repeats by filtering a dataframe and counting how many rows are left
def getQueryCounts(dataframe, queryArray):
    filteredDF = dataframe
    for queryTuple in queryArray:
        filteredDF = queryDataframe(filteredDF, queryTuple)
    count = len(filteredDF)
    print str(filteredDF)
    return count

# FILTER: reduce the dataframe to the rows that match a query, with only the columns that match the query
# queryArray = [('age', 1), ('sex', 2)]
def queryDataframe(dataframe, tuple):
    filteredDF = dataframe
    fieldNames = []
    field_name = tuple[0]
    field_value = tuple[1]
    filteredDF = filteredDF.loc[(filteredDF[field_name] == field_value)]
    fieldNames.append(field_name)
    # finalDataframe = filteredDF[fieldNames] # only return the columns in question
    # print finalDataframe
    # return finalDataframe
    return filteredDF

# except:
# filteredDF = filteredDF.loc[(filteredDF[field_name] == field_value)]
# finalDataframe = filteredDF[field_name]
# return finalDataframe
