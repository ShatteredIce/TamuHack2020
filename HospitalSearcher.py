import re

def getInitPossibleLocs(procedure, state, city, comm):
    inpdatalist = []
    with open('inpatientCharges.csv') as inpdatafile:
        for line in inpdatafile:
            inpdatalist.append(line.split(','))

    citStComb = state + ' - ' + city

    resultList = []

    for i in range(len(inpdatalist)):
        for j in range(len(inpdatalist[0])):
            if inpdatalist[i][j][0] == '$':
                inpdatalist[i][j] = float(inpdatalist[i][j][1:])
        containsAll = True
        for token in procedure.upper().split(' '):
            if not (re.search(token, inpdatalist[i][0])):
                containsAll = False
        if containsAll:
            resultList.append(inpdatalist[i])

    resultListState = []
    for result in resultList:
        if result[5] == state:
            resultListState.append(result)

    resultListCity = []
    for result in resultListState:
        if result[7] == citStComb:
            resultListCity.append(result)

    resultListComm = []
    for result in resultListCity:
        if result[4] == comm.upper():
            resultListComm.append(result)

    if len(resultListComm) != 0:
        return resultListComm
    elif len(resultListCity) != 0:
        return resultListCity
    elif len(resultListState) != 0:
        return resultListState
    elif len(resultList) != 0:
        return resultList
    else:
        return 'None found!'


def getPossibleLocs(procedure, state, city, comm):
    hosps = getInitPossibleLocs(procedure, state, city, comm)
    if hosps != 'None found!':
        topChoices = []
        for i in range(5):
            try:
                leastPrice = hosps[0][10]
                leastCostlyHosp = hosps[0]
            except:
                break
            for j in range(len(hosps)):
                if hosps[j][10] < leastPrice:
                    leastPrice = hosps[j][10]
                    leastCostlyHosp = hosps[j]
            topChoices.append(leastCostlyHosp)
            hosps.remove(leastCostlyHosp)
        return topChoices
    else:
        return 'None found!'