from django.test import TestCase

# Create your tests here.
import numpy as np
import json

def genFactorList(forelist, c, factorlistold=None):
    # print str(forelist),str(c)
    if forelist == None: return [0.0 if i > 1 else 0.5 for i in range(6)]
    if c == None: return [0.0 if i > 1 else 0.5 for i in range(forelist)]
    if factorlistold == None:
        factorlistold = [0.0 for i in range(len(forelist))]
    else:
        if type(factorlistold) == str : factorlistold = json.loads(factorlistold)
        if len(factorlistold) > len(forelist) : factorlistold.extend([0.0]*(len(factorlistold)-len(forelist)))
        if None in factorlistold : factorlistold = [0 if f is None else f for f in factorlistold]
    clist = [float(c) for i in range(len(forelist))]
    gaplist = list(map(lambda x, y: (x - y) if x != None and y != None else None, forelist, clist))
    # print(gaplist)
    positvelist = [g for g in list(filter(lambda x: x != None, gaplist)) if g >= 0]
    # print(positvelist)
    negativelist = [g for g in list(filter(lambda x: x != None, gaplist)) if g < 0]
    # print(negativelist)
    upper = min(positvelist) if positvelist != [] else None
    under = max(negativelist) if negativelist != [] else None
    # print(upper, under)
    factorlist = [0.0 for i in range(len(forelist))]
    if upper == 0 or (upper != None and under == None):
        factorlist[gaplist.index(upper)] = 1
    if upper == None and under != None:
        factorlist[gaplist.index(under)] = 1
    print(gaplist,upper,under)
    if upper != None and under != None:
        factorlist[gaplist.index(upper)] = abs(upper) / (abs(upper) + abs(under))
        factorlist[gaplist.index(under)] = abs(under) / (abs(upper) + abs(under))
    factorlist = np.array(factorlist)
    factorlistold = np.array(factorlistold)
    factorlist = factorlist + factorlistold
    factorlist = factorlist / np.sum(factorlist)
    return list(factorlist)

if __name__ == '__main__':
    print(genFactorList([3234,23232,None,None,None,None],434,[None,0.3,None,None,None,None]))