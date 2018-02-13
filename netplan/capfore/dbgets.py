from __future__ import absolute_import, unicode_literals
from datetime import date,timedelta
import numpy as np
from django.db import connections



PI_LIST = [
    'rrc_connmean',
    'prb_dlutilization',
    'prb_ulutilization',
    'pdcp_upoctdl',
    'pdcp_upoctul',
    'rrc_effectiveconnmean'
]

ATTR_LIST = [
    'name',
    'city',
    'indoor',
    'scene1',
    'scene2',
    'scene3',
    'band',
    'long',
    'lat',
    'erab_nbrmeanestab',
    'erab_nbrsuccestab',
    'erab_upoctdl',
    'packagetype',
]


def _isExistTime(rectime):
    with connections['capdata'].cursor() as cursor:
        cursor.execute("SELECT tablename from pg_tables where schemaname = 'public' and tablename = 'ull{0:%Y%m}s'".format(rectime))
        row = cursor.fetchone()
    if row : return True
    return False

def _isExistPredictTime(rectime):
    with connections['capdata'].cursor() as cursor:
        cursor.execute("SELECT tablename from pg_tables where schemaname = 'public' and tablename = 'forecast{0:%Y%m}'".format(rectime))
        row = cursor.fetchone()
    if row : return True
    return False

def addmonth(d, md):
    t = d.year*12+d.month-1
    t = t+md
    y = int(t/12)
    m = t%12+1
    return date(year = y, month = m ,day = d.day)

def sixmonth(m):
    result = [m]
    for i  in range(1,6):
        m = addmonth(m,-1)
        result.append(m)
    return result

def getNow():
    m = date.today()
    m = date(m.year,m.month,1)
    for i in range(12):
        if _isExistTime(m) : return m
        m = addmonth(m,-1)
    return None

def getattrdictlist(cursor):
    result = {}
    for row in cursor.fetchall():
        rowdict = {}
        for pi in range(len(ATTR_LIST)):
            rowdict[ATTR_LIST[pi]] = row[pi+1]
        result[row[0]] = rowdict
    return result

def getAllAttr(now):
    with connections['capdata'].cursor() as cursor:
        cursor.execute("""
        with a(cgi,name,city,indoor,scene1,scene2,scene3,band,long,lat,erab_nbrmeanestab,erab_nbrsuccestab,erab_upoctdl) as 
        (select a."小区id" , a."小区名称" ,a."城市", a."室内外属性" , null, null , null, a."频段" , a."经度" , a."纬度" ,a."平均erab数（个）",
               a."erab建立成功数" , case when a."erab建立成功数" <> 0 then a."下行业务信道流量（mbyte）"/a."erab建立成功数" else null end 
        from ull{0:%Y%m}s a left join tco_pro_eutrancell_yah b  on a."小区id" = b.cgi) 
        select cgi,name,city,indoor,scene1,scene2,   scene3,   band, long, lat,  erab_nbrmeanestab,erab_nbrsuccestab,erab_upoctdl, case when erab_upoctdl<0.3 then '小包' when erab_upoctdl>=0.3 then '中包' else '大包' end  from a
        """.format(now[0]))
        dictlist = getattrdictlist(cursor)
    return dictlist

def getpidictlist(cursor):
    result = {}
    for row in cursor.fetchall():
        rowdict = {}
        for pi in range(len(PI_LIST)):
            rowdict[PI_LIST[pi]] = row[pi+1]
        result[row[0]] = rowdict
    return result

def getNowlist(now):
    with connections['capdata'].cursor() as cursor:
        cursor.execute("""
                with a(rectime,id , RRC_ConnMean ,PRB_DlUtilization,PRB_UlUtilization,PDCP_UpOctDl,PDCP_UpOctUl, RRC_EffectiveConnMean) as 
                (select '{0[0]}'::timestamp, "小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0[0]:%Y%m}s
                union select '{0[1]}'::timestamp ,"小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0[1]:%Y%m}s
                union select '{0[2]}'::timestamp ,"小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0[2]:%Y%m}s
                union select '{0[3]}'::timestamp ,"小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0[3]:%Y%m}s
                union select '{0[4]}'::timestamp ,"小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0[4]:%Y%m}s
                union select '{0[5]}'::timestamp ,"小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0[5]:%Y%m}s),
                 b(rectime,id) as 
                 (select  '{0[0]}'::timestamp, "小区id" from ull{0[0]:%Y%m}s
                  union select '{0[1]}'::timestamp ,  "小区id" from ull{0[0]:%Y%m}s
                  union select '{0[2]}'::timestamp ,  "小区id" from ull{0[0]:%Y%m}s
                  union select '{0[3]}'::timestamp ,  "小区id" from ull{0[0]:%Y%m}s
                  union select '{0[4]}'::timestamp ,  "小区id" from ull{0[0]:%Y%m}s
                  union select '{0[5]}'::timestamp ,  "小区id" from ull{0[0]:%Y%m}s)                
                select b.id, json_agg(RRC_ConnMean) , json_agg(PRB_DlUtilization), json_agg(PRB_UlUtilization), json_agg(PDCP_UpOctDl), json_agg(PDCP_UpOctUl), json_agg(RRC_EffectiveConnMean) from b left join a on a.rectime = b.rectime and a.id = b.id  group by b.id
            """.format(now))
        dictlist = getpidictlist(cursor)
    return dictlist

def getOldlist(now):
    old =  [ addmonth(m,-12) for m in now]
    if _isExistTime(old[0]) != True : return {}
    with connections['capdata'].cursor() as cursor:
        a_pi = ','.join(PI_LIST)
        a = ' union '.join(filter(None,["""
            select '{0}'::timestamp, "小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0:%Y%m}s
            """.format(n) if _isExistTime(n) else None
            for n in old]))
        b = ' union '.join(['select  \'{0}\'::timestamp, "小区id" from ull{1:%Y%m}s'.format(n,now[0]) for n in old])
        agg_pi = ','.join(['json_agg({0})'.format(pi) for pi in PI_LIST])
        cursor.execute("""
                with a(rectime,id ,{0}) as ({1}),
                     b(rectime,id) as ({2})                
                select b.id, {3} from b left join a on a.rectime = b.rectime and a.id = b.id  group by b.id
        """.format(a_pi,a,b,agg_pi))
        dictlist = getpidictlist(cursor)
    return dictlist

def getOld(now, period = 1):
    m = addmonth(now[0],period-12)
    if _isExistTime(m) != True: return {}
    with connections['capdata'].cursor() as cursor:
        cursor.execute("""
        select "小区id" , "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"  from ull{0:%Y%m}s
        """.format(m))
        dictlist = getpidictlist(cursor)
    return dictlist

def getF(now):
    if _isExistPredictTime(now[0]) == False : return {}
    with connections['capdata'].cursor() as cursor:
        cursor.execute("""
        with p(id,RRC_ConnMean,rrc_act_rate,rrc_upoctdl) as 
            (select cgi , RRC_ConnMean_predict::numeric , 
            case when RRC_ConnMean_predict =0 then 1 else RRC_EffectiveConnMean_predict::numeric/RRC_ConnMean_predict::numeric end ,
             case when RRC_ConnMean_predict = 0 then 1 else PDCP_UpOctDl_predict::numeric/RRC_ConnMean_predict::numeric end 
             from forecast{0:%Y%m})
            ,n(id,RRC_ConnMean,rrc_act_rate,rrc_upoctdl) as 
            (select "小区id" , "rrc连接平均数（个）", 
            case when  "rrc连接平均数（个）" = 0 then 1 else "有效rrc连接平均数（个）"/"rrc连接平均数（个）" end,
             case when "rrc连接平均数（个）" = 0 then 1 else "下行业务信道流量（mbyte）" / "rrc连接平均数（个）" end 
             from ull{0:%Y%m}s)
            ,r(id,ff) as 
            (select n.id, (case when n.RRC_ConnMean = 0 then 1 else p.RRC_ConnMean/n.RRC_ConnMean end) * (case when n.rrc_act_rate = 0 then 1 else p.rrc_act_rate/n.rrc_act_rate end )*( case when n.rrc_upoctdl = 0 then 1 else p.rrc_upoctdl/n.rrc_upoctdl end)from n left join p on n.id = p.id
            )
            select id,case when ff < 0 then 1 else sqrt(ff) end from r
        """.format(now[0]))
        f = {}
        for row in cursor.fetchall():
            f[row[0]] = row[1]
    return f

def getE(now,period = 1):
    if _isExistPredictTime(now[0]) == False: return {}
    with connections['capdata'].cursor() as cursor:
        cursor.execute("""
        with p(id , RRC_ConnMean,PRB_DlUtilization,PRB_UlUtilization,PDCP_UpOctDl,PDCP_UpOctUl, RRC_EffectiveConnMean) as  
            (select cgi , RRC_ConnMean_predict,PRB_DlUtilization_predict,PRB_UlUtilization_predict,PDCP_UpOctDl_predict,PDCP_UpOctUl_predict, RRC_EffectiveConnMean_predict  from forecast{0:%Y%m}),
            n(id , RRC_ConnMean,PRB_DlUtilization,PRB_UlUtilization,PDCP_UpOctDl,PDCP_UpOctUl, RRC_EffectiveConnMean) as 
            (select "小区id" ,  "rrc连接平均数（个）", "下行PRB平均利用率（%）", "上行PUSCHPRB平均利用率（%）", "下行业务信道流量（mbyte）" , "上行业务信道流量（mbyte）" , "有效rrc连接平均数（个）"   from ull{0:%Y%m}s)
        select n.id,n.RRC_ConnMean-p.RRC_ConnMean , n.PRB_DlUtilization-p.PRB_DlUtilization , n.PRB_UlUtilization-p.PRB_UlUtilization,
            n.PDCP_UpOctDl-p.PDCP_UpOctDl, n.PDCP_UpOctUl-p.PDCP_UpOctUl, n.RRC_EffectiveConnMean - p.RRC_EffectiveConnMean from n left join p on n.id = p.id
        """.format(now[0]))
        dictlist = getpidictlist(cursor)
    return dictlist

def getffactorlist(now):
    if _isExistPredictTime(now[0]) == False: return {}
    with connections['capdata'].cursor() as cursor:
        cursor.execute("""
        select cgi , RRC_ConnMean_factorlist,PRB_DlUtilization_factorlist,PRB_UlUtilization_factorlist,PDCP_UpOctDl_factorlist,PDCP_UpOctUl_factorlist, RRC_EffectiveConnMean_factorlist from forecast{0:%Y%m}
        """.format(now[0]))
        dictlist = getpidictlist(cursor)
    return dictlist

def getfforelist(now):
    if _isExistPredictTime(now[0]) == False: return {}
    with connections['capdata'].cursor() as cursor:
        cursor.execute("""
        select cgi , RRC_ConnMean_forelist,PRB_DlUtilization_forelist,PRB_UlUtilization_forelist,PDCP_UpOctDl_forelist,PDCP_UpOctUl_forelist, RRC_EffectiveConnMean_forelist from forecast{0:%Y%m}
        """.format(now[0]))
        dictlist = getpidictlist(cursor)
    return dictlist