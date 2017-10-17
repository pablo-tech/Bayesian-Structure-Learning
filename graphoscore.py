# NETWORKX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Networkx required for graph()")
except RuntimeError:
    print("Networkx unable to open")
    raise


def getScore(graph, dataframe):
    filter(dataframe)
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

