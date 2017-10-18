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
    print"{} \t\t UNIQUE: \t\t {} ".format(varName, unique)

def filter(dataframe):
    testQuery = [('age', 1), ('sex', 1)]
    filteredDF = queryDataframe(dataframe, testQuery)
    print(filteredDF)

# FILTER: reduce the dataframe to the rows that match a query, with only the columns that match the query
# queryArray = [('age', 1), ('sex', 2)]
def queryDataframe(dataframe, queryArray):
    filteredDF = dataframe
    fieldNames = []
    for tuple in queryArray:
        field_name = tuple[0]
        field_value = tuple[1]
        filteredDF = filteredDF.loc[(filteredDF[field_name] == field_value)]
        fieldNames.append(field_name)
    return filteredDF[fieldNames]

# def query(dataframe):
#     #print(inputDF.loc[(inputDF['age']==1) & (inputDF['sex']==2)])
#     print(dataframe.loc[(dataframe['age']==1) & (dataframe['sex']==2)][['age', 'sex']])
#     pass
