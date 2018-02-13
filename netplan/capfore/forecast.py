from __future__ import absolute_import, unicode_literals

import numpy as np
import json
from scipy.optimize import curve_fit



class Forecast(object):
    #环比forecasts，同比forecast_tb

    def __init__(self,xlist = None,ylist = None, period = None, oldlist = None,old = None ,f = None, e = None ):
        self.popt = None
        self.popt = None
        self.func = None
        self.xdata = None
        self.ydata = None
        self.A = None; self.B = None; self.AF = None; self.BF = None; self.AE = None; self.BE = None
        if xlist !=None and ylist != None and period !=None :
            if type(xlist) == str : xlist = json.loads(xlist)
            if type(ylist) == str : ylist = json.loads(ylist)
            try:
                self.B = self.forecasts(xlist,ylist,period)[-1]
            except :
                self.B = None
        if oldlist !=None and old !=None :
            if type(oldlist) == str : oldlist = json.loads(oldlist)
            self.A = self.forecast_tb(oldlist,ylist,old)
        if f != None :
            self.AF = (float(self.A) * float(f)) if self.A != None else None
            self.BF = (float(self.B) * float(f)) if self.B != None else None
        if e != None :
            self.AE = (self.A + e) if self.A !=None else None
            self.BE = (self.B + e) if self.B !=None else None
        self.forelist = [self.A,self.B,self.AF,self.BF,self.AE,self.BE]


    def line(self, x, a, b):
        return x * a + b

    def exponential(self, x, a, b):
        return np.exp(x * a) * b

    def log10(self, x, a, b):
        return np.log10(x) * a + b

    def forecast(self, xlist, ylist, period = 1, func = None):
        for i in range(len(xlist)):
            if xlist[i] is None or ylist[i] is None:
                xlist[i] = None
                ylist[i] = None
        xlist = list(filter(lambda x: x != None, xlist))
        ylist = list(filter(lambda x: x != None, ylist))
        if func == None : func = self.line
        self.func = func
        self.xdata = np.array(xlist)
        self.ydata = np.array(ylist)
        try:
            self.popt, self.pcov = curve_fit(func, self.xdata, self.ydata)
        except :
            return [None]
        x = np.array(range(period))+max(self.xdata)+1
        return  func(x, *self.popt)

    def avgdiv(self):
        ydata_new = self.func(self.xdata, *self.popt)
        return np.sum(np.power((ydata_new - self.ydata), 2))

    def forecasts(self, xlist, ylist, period = 1, funclist=None):
        avgdiv_min = None
        if funclist == None : funclist = [self.line,self.exponential,self.log10]
        for func in funclist:
            fdata = self.forecast(xlist, ylist,  period,func)
            avgdiv = self.avgdiv()
            #print(fdata)
            if avgdiv_min == None:
                avgdiv_min = avgdiv
                fdata_r = fdata
            elif avgdiv < avgdiv_min:
                avgdiv_min = avgdiv
                fdata_r = fdata
        return fdata_r

    def forecast_tb(self,oldlist,newlist,old):
        v = 0 ; d = 0
        for i in range(len(oldlist)) :
            try:
                v = v+ (newlist[i] - oldlist[i])
                d = d + oldlist[i]
            except :
                pass
        if d != 0 :
            return float(old)*(1+v/d)
        else :
            return float(old)

    def genFactorList(self,forelist, c, factorlistold=None):
        if forelist == None :
            return [0.0 if i > 1 else 0.5 for i in range(6)]
        else:
            if type(forelist) == str: forelist = json.loads(forelist.replace('None', 'null'))
        if c == None: return [0.0 if i > 1 else 0.5 for i in range(6)]
        if factorlistold == None:
            factorlistold = [0.0 for i in range(len(forelist))]
        else:
            if type(factorlistold) == str: factorlistold = json.loads(factorlistold.replace('None','null'))
            if len(factorlistold) > len(forelist): factorlistold.extend([0.0] * (len(factorlistold) - len(forelist)))
            if None in factorlistold: factorlistold = [0 if f is None else f for f in factorlistold]
        clist = [float(c) for i in range(len(forelist))]
        gaplist = list(map(lambda x, y: (x - y) if x != None and y != None else None, forelist, clist))
        positvelist = [g for g in list(filter(lambda x: x != None, gaplist)) if g >= 0]
        negativelist = [g for g in list(filter(lambda x: x != None, gaplist)) if g < 0]
        upper = min(positvelist) if positvelist != [] else None
        under = max(negativelist) if negativelist != [] else None
        factorlist = [0.0 for i in range(len(forelist))]
        if upper == 0 or (upper != None and under == None):
            factorlist[gaplist.index(upper)] = 1
        if upper == None and under != None:
            factorlist[gaplist.index(under)] = 1
        if upper != None and under != None:
            factorlist[gaplist.index(upper)] = abs(upper) / (abs(upper) + abs(under))
            factorlist[gaplist.index(under)] = abs(under) / (abs(upper) + abs(under))
        factorlist = np.array(factorlist)
        factorlistold = np.array(factorlistold)
        factorlist = factorlist + factorlistold
        factorlist = factorlist / np.sum(factorlist)
        return list(factorlist)

def line(x,a,b):
    return x*a+b

def exponential(x,a,b):
    return np.exp(x*a)*b

def log10(x,a,b):
    return np.log10(x)*a+b

def forecast(xlist,ylist,period = 1,func = line):
    for i in range(len(xlist)):
        if xlist[i] is None  or ylist[i] is None : xlist[i] = None ; ylist[i] = None
    xlist = list(filter(None,xlist))
    ylist = list(filter(None,ylist))
    xdata = np.array(xlist)
    ydata = np.array(ylist)
    popt,pcov = curve_fit(func,xdata,ydata)
    x = np.array(range(period))+max(xdata)+1
    return func(x,*popt)

def avgdiv(xlist,ylist,func = line):
    xdata = np.array(xlist)
    ydata = np.array(ylist)
    popt,pcov = curve_fit(func,xdata,ydata)
    ydata_new = func(xdata,*popt)
    return np.sum(np.power(ydata_new - ydata,2))

def forecasts(xlist ,ylist,period = 1,funclist=[line,exponential,log10]):
    avgdiv_min = None
    for func in funclist:
        fdata = forecast(xlist,ylist,period,func)
        ad = avgdiv(xlist,ylist,func)
        print(fdata)
        if avgdiv_min == None :
            avgdiv_min = ad
            fdata_r = fdata
        elif ad < avgdiv_min:
            avgdiv_min = ad
            fdata_r = fdata
    return fdata_r


if __name__ == '__main__' :
    f = Forecast(range(1,7),[80,120,200,250,290,400],3,[50,20,30,60,70,90],100,1.3,30)
    print ( f.forelist)
    #print( forecast([0,2,3,4,5,6],[80,120,200,250,None,400],3))