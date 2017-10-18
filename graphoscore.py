# Calculate the Bayesian score of a network against a dataset

# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise


def getScore(graph, dataframe):
    # filter(dataframe)
    return 0

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


# SCORING WITH FACTORS: Cooper & Herscovits, page 320, formula 8
# It is the same as Decisions under Uncertainty, page 47, formula 2.80
# Posterior probability: is proportional to the prior probability
# Cancelling out: prior probability cancels out when two networks are compared by division
# Example: if Score(network1)/Score(network2)>1 then network1 is better representation of the data
def getCooperHerscovitsBayesianScore(graph):
    score = 1
    return 1


# SCORING WITH SUMS: Decisions Under Uncertainty, page 47, formula, formula 2.83
# Posterior probability: is incremental to prior probability
# Cancelling out: prior probability cancels out when two networks are compared by subtraction
# Example: if Score(network1)-Score(network2)>0 then network1 is a better
def getLogCooperHerscovitsBayesianScore(graph):
    score = 0
    return 1
