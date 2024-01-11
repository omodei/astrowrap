#!/usr/bin/env python
import datetime
def met2date(MET,opt=None):
    """                                                                                                                                                                 
    converts a MET time into a date string, in format \"08-07-25 10:26:09\".                                                                                            
    If opt=="grbname", the GRB name format 080725434 is returned.                                                                                                       
    """
    MET  = float(MET)
    leap = 0
    if MET>=252460802:  leap+=1
    if MET>=156677801:  leap+=1
    if MET>=362793603:  leap+=1 # June 2012 leap second
    if MET>=457401604:  leap+=1 # June 2015 leap second
    if MET>=504921605:  leap+=1 # 2017 leap second                                                                                                                     
    MET=MET-leap
    metdate  = datetime.datetime(2001, 1, 1,0,0,0)
    dt=datetime.timedelta(seconds=MET)
    grb_date = metdate + dt
    yy       = grb_date.year
    mm       = grb_date.month
    dd       = grb_date.day
    hr       = grb_date.hour
    mi       = grb_date.minute
    ss       = grb_date.second
    fss      = ss+grb_date.microsecond * 1e-6
    rss      = round(fss)
    fff      = round(float(rss+60.*mi+3600.*hr)/86.4)
    if fff>999: fff=999
    d0       = datetime.datetime(int(yy), 1,1,0,0,0)
    doy      = (grb_date-d0).days+1
    # print(yy,mm,dd,hr,mi,ss,fss,fff)
    text='%04d-%02d-%02dT%02d:%02d:%06.3f' %(yy,mm,dd,hr,mi,fss)
    return text

if __name__=='__main__':
    import sys
    MET=sys.argv[1]
    txt=met2date(MET)
    print(txt)
