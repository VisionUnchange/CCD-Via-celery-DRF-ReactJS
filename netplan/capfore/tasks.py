# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import numpy as np

from capfore.forecast import Forecast

from capfore.models import Task,Cell

from celery.utils.log import get_task_logger
import json

from capfore.dbgets import *
logger = get_task_logger(__name__)


@shared_task
def forecast(taskid):
    task = Task.objects.get(id=taskid)
    task.status = 'Doing'
    task.save()
    period = task.period
    logger.info(str(taskid))
    now = sixmonth(task.curdate)
    logger.info(str(now))
    attrdictlist = getAllAttr(now)
    if attrdictlist :
        logger.info('attrdictlist is done, length is {0}'.format(len(attrdictlist)))
        logger.info(str(list(attrdictlist.values())[0]))
    fdict = getF(now)
    if fdict : logger.info('fdict is done, length is {0}'.format(len(fdict)))
    nowdictlist = getNowlist(now)
    if nowdictlist :
        logger.info('nowdictlist is done, length is {0}'.format(len(nowdictlist)))
        logger.info(str(list(nowdictlist.values())[0]))
    olddictlist = getOldlist(now)
    if olddictlist : logger.info('olddictlist is done, length is {0}'.format(len(olddictlist)))
    edictlist = getE(now,period)
    if edictlist :logger.info('edictlist is done, length is {0}'.format(len(edictlist)))
    oldlist = getOld(now,period)
    if oldlist : logger.info('oldlist is done, length is {0}'.format(len(oldlist)))
    ffactordictlist = getffactorlist(now)
    if ffactordictlist :logger.info('ffactordictlist is done, length is {0}'.format(len(ffactordictlist)))
    fforedictlist = getfforelist(now)
    if fforedictlist : logger.info('fforedictlist is done, length is {0}'.format(len(fforedictlist)))
    allcount = len(nowdictlist)
    rowi = 0
    for k,v in nowdictlist.items() :
        cgi = k
        nowdict = v
        attrdict = attrdictlist[cgi] if cgi in attrdictlist else None
        olddict = olddictlist[cgi] if cgi in olddictlist else None
        old = oldlist[cgi] if cgi in oldlist else None
        f = fdict[cgi] if cgi in fdict else None
        edict = edictlist[cgi] if cgi in edictlist else None
        ffactordict = ffactordictlist[cgi] if cgi in ffactordictlist else None
        fforedict = fforedictlist[cgi] if cgi in fforedictlist else None
        cell = Cell(task=task, cgi = cgi)
        for attr in ATTR_LIST:
            if hasattr(cell, attr):  setattr(cell, attr, attrdict[attr])
        if hasattr(cell, 'f') and f != None:  setattr(cell, 'f', f)
        for pi in PI_LIST:
            if hasattr(cell,pi) and nowdict !=None : setattr(cell,pi,nowdict[pi][-1])
            pi_end = pi+'_nowlist'
            if hasattr(cell,pi_end) and nowdict !=None :  setattr(cell,pi_end,json.dumps(nowdict[pi]))
            pi_end = pi+'_oldlist'
            if hasattr(cell,pi_end) and olddict !=None :  setattr(cell,pi_end,json.dumps(olddict[pi]))
            pi_end = pi + '_old'
            if hasattr(cell, pi_end) and old !=None:  setattr(cell, pi_end, old[pi])
            pi_end = pi + '_e'
            if hasattr(cell, pi_end) and edict != None:  setattr(cell, pi_end, edict[pi])
            pi_end = pi + '_forelist'
            try:
                forecast = Forecast(list(range(1, 7)), nowdict[pi] if nowdict != None else None,\
                                    period, olddict[pi] if olddict != None else None, \
                                    old[pi] if old != None else None,\
                                    f,edict[pi] if edict != None else None)
                if hasattr(cell,pi_end) : setattr(cell,pi_end,json.dumps(forecast.forelist))
                pi_end = pi + '_factorlist'
                # logger.info('{},{},{}'.format(fforedict[pi] if fforedict != None else None, nowdict[pi][-1],
                #                                  ffactordict[pi] if ffactordict != None else None))
                factor = forecast.genFactorList(fforedict[pi] if fforedict != None else None, nowdict[pi][-1],
                                                ffactordict[pi] if ffactordict != None else None)
                # logger.info('{}'.format(factor))
                if hasattr(cell, pi_end): setattr(cell, pi_end, json.dumps(factor))
                pi_end = pi + '_predict'
                predict = _forefact(forecast.forelist, factor)
                if hasattr(cell, pi_end): setattr(cell, pi_end, predict)
            except :
                #print('Error:',e)
                pass
            cell.save()
        # logger.info('{},{},{},{},{},{}'.format(cell.name, pi_end, forecast.forelist, factor, predict,getattr(cell,pi_end)))
        # if rowi > 5: return None
        rowi = rowi+1
        if rowi % 1000 == 0 :
            task.progress = rowi/allcount
            task.save()
            logger.info('task {0} ,row: {1} , process: {2:.2%}'.format(taskid,rowi, task.progress))
    task.progress = 1
    task.status = 'Done'
    task.save()


def _forefact(forelist,factlist):
    for i in range(len(forelist)):
        if forelist[i] is None or factlist[i] is None:
            forelist[i] = None
            factlist[i] = None
    forelist = np.array(list(filter(lambda x: x!=None, forelist)))
    factlist = np.array(list(filter(lambda x: x!=None, factlist)))
    return sum(forelist*factlist)/sum(factlist)

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

if __name__ == '__main__':
    import sys, os , django
    sys.path.insert(0,'/Users/zengqingbo/project/netplan')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "..netplan.settings.dev")
    django.setup()
    print('test is doing')