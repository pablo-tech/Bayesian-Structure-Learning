# Operate on Python Pandas dataframe

def getRandomVarNodeNames(dataframe):
    return list(dataframe)

def getUniqueRandomVarValues(dataframe, varName):
    unique = dataframe[varName].unique()
    print"{} \t\t UNIQUE: \t\t {} ".format(varName, unique)
