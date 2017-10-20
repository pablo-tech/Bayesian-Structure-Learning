# Test class for graphoiteration


import graphoquery as oit

query1 = oit.getPairQuery("x2", 2, "x1", 1)
print str(query1)

query2 = oit.getPairQueryDistribution("x2", ['1', '2'], "x1", ['3', '4'])
print str(query2)

query3 = oit.getJointDistribution("x3", 9, query2)
print str(query3)