import pandas as pd
import re
import numpy as np
from . import cbwe
def readscan(specfile,scanno):
    with open(specfile,'r') as fp:
            mpairs = []
            break_out = False
            for i, line in enumerate(fp):
                if break_out:
                    break
                if '#O' in line:
                    tmnames = line[4:-1].split('  ')
                    for ttmnames in tmnames:
                        if len(ttmnames) > 0:
                            mpairs.append([ttmnames,0.0])
                if '#S {0:d}'.format(scanno) in line:
                    title = line
                    nlines = int(line.split()[-2])+1
                    nother = 0
                    mindex = 0
                    nrows = 0 
                    filestart = i+1
                    start = False
                    for line  in fp:
                        if break_out:
                            break
                        if not start:
                            if '#L' in line:
                                cnames = re.split('\s{2,}',line[3:-1])   
                                nother += 1
                            elif '#P' in line:
                                tmvals = line[4:-1].split(' ')
                                for ttmval in tmvals:
                                    if len(ttmval) > 0:
                                        mpairs[mindex][1] += float(ttmval)
                                        mindex += 1
                                nother +=1
                            elif ('#' in line):
                                nother += 1
                            elif (not '#' in line):
                                nrows += 1
                                start = True
                        else:
                            if ('#C' in line):
                                break_out = True
                                break
                            elif (nrows == nlines):
                                break_out = True
                                break
                            else:
                                nrows += 1
    # clean up mvals
    mvals = {}
    for tpair in mpairs:
        mvals[tpair[0]] = tpair[1]
    scan_info = {'columns':cnames[1:],'title':title,'mvals':mvals}
    if nrows == 0:
        print('scan aborted')
        return([],scan_info)
    else:
        data = pd.read_csv(specfile,skiprows=filestart+nother,
                       nrows=nrows,delim_whitespace=True,header=None)                                
        data.columns=cnames        
        return(data,scan_info)
    
def readscascan(specfile,scanno):
    with open(specfile,'r') as fp:
        # read down to start of scan
        start = False
        mca = False
        mca_i = 0
        nmca = 0
        mca_data = []
        M_mca_data = []
        start_chan = 0
        end_chan = 0
        data = []
        for i, line in enumerate(fp):
            if not start and '#S {0:d} '.format(scanno) in line:
                print(f'found scan {scanno:d} at line {i:d}')
                start = True
                continue
            if start and '#@CHANN ' in line:
                channels = re.split('\s{1,}',line[8:-1])
                start_chan = int(channels[1])
                end_chan = int(channels[2])
                print(f'start chan {start_chan:d} end_chan {end_chan:d}')
                continue
            if start and '#@MCA ' in line:
                data_per_line = int(line[-4:-2])
                continue
            if start and '@A' in line:
                mca = True
                nmca = (end_chan-start_chan)
                mca_data = np.zeros(nmca)
                mca_i = 0
            if start and mca:
                if mca_i == 0:
                    ifst = 3
                else:
                    ifst = 1
                if ord(line[-1]) == 10:
                    line = line[:-1]
                if ord(line[-1]) == 92:
                    line = line[:-1]
                tdata = list(map(int,line[ifst:].split())) 
                n1 = mca_i+data_per_line
                n2 = nmca 
                mca_data[mca_i:min(n1,n2)] = tdata
                mca_i += np.size(tdata)
                if mca_i == nmca:
                    M_mca_data.append(mca_data)
                    mca = False
                continue
            if start and not mca and not '#' in line:
                tdata = list(map(float,line[0:-1].split()))
                data.append(tdata)
            if start  and '#S' in line:
                start = False
    return(M_mca_data)
def readscan_2():
    print('ERROR: readscan_2 still needs to be written')
    return 0
def getscan_mca(filename,scan_no,lld,uld):
    data, scan_info,M_mca_data,start_ch,end_ch = readscan_2(filename,scan_no)
    x = data['Two Theta']
    y = data['Detector']
    mon = data['Seconds']
    dy = np.sqrt(y)
    y /= mon
    dy /= mon
    y_mca = y*0
    for i,mca_data in enumerate(M_mca_data):
        y_mca[i] = np.sum(mca_data[lld-start_ch:uld-start_ch])
    dy_mca = np.sqrt(y_mca)
    y_mca/=mon
    dy_mca /= mon
    return x,y,dy,y_mca,dy_mca                
def merge_scans(specfile,scanset,norm='mca'):
    x = np.array([])
    y = np.array([])
    dy = np.array([])
    for scanno, bg, att in scanset:
        if bg:
            tx,ty,tdy = getscan_bg(specfile,scanno,norm)
            ty *= att
            tdy *= att
        else:
            tx,ty,tdy = getscan(specfile,scanno,norm)
            ty *= att
            tdy *= att
        x = np.append(x,tx)
        y = np.append(y,ty)
        dy = np.append(dy,tdy)
    ind = np.argsort(x)
    x = x[ind]
    y = y[ind]
    dy = dy[ind]
    return x,y,dy
def merge_duplicates(x,y,dy):
    # sort and reorder x
    w = np.argsort(x)
    x=x[w]
    y=y[w]
    dy=dy[w]
    # now look for duplicates
    wdup = x[0:-1]-x[1:]==0
    while np.sum(wdup)>0:
        ofst = 0
        for j in np.argwhere(wdup):
            i = int(j-ofst)
            y[i],dy[i] = cbwe.cbwe_s(y[i],dy[i],y[i+1],dy[i+1])
            y = np.append(y[0:i+1],y[i+2:])
            x = np.append(x[0:i+1],x[i+2:])
            dy = np.append(dy[0:i+1],dy[i+2:])
            ofst += 1
        wdup = x[0:-1]-x[1:]==0
    return(x,y,dy)
        
def getscan(filename,scan_no,norm):
    data, scan_info = readscan(filename,scan_no)
    x = data['Two Theta']
    y = data['Detector']
    if norm == 'mca':
        mon = data['mca']
        if np.mean(mon)<1000:
            mon = mon*0+np.mean(mon)
        mon = mon*np.mean(data['Seconds']/data['mca'])
    else:
        mon = data['Seconds']
    dy = np.sqrt(y)
    y /= mon
    dy /= mon
    return x,y,dy
def getscan_bg(filename,scan_no,norm):
    x,y,dy = getscan(filename,scan_no,norm)
    x,yb1,dyb1 = getscan(filename,scan_no+1,norm)
    x,yb2,dyb2 = getscan(filename,scan_no+2,norm)
    ys = y-(yb1+yb2)/2
    dys = np.sqrt(dy**2 + dyb1**2 + dyb2**2)
    return x,ys,dys
def readscan_2_DND(specfile,scanno):
    with open(specfile,'r') as fp:
        # read down to start of scan
        start = False
        mca = False
        mca_i = 0
        nmca = 0
        mca_data = []
        M_mca_data = []
        start_chan = 0
        end_chan = 2047
        channels = 2048
        data = []
        for i, line in enumerate(fp):
            if not start and '#S {0:d} '.format(scanno) in line:
                print(f'found scan {scanno:d} at line {i:d}')
                start = True
                title = line
                continue
            if start and '#L' in line:
                cnames = re.split('\s{2,}',line[3:-1]) 
                continue
            if start and '@0' in line:
                mca = True
                nmca = (end_chan-start_chan+1)
                mca_data = np.zeros(nmca)
                mca_i = 0          
            if start and mca:
                line0=line
                if mca_i == 0:
                    ifst = 1
                else:
                    ifst = 1
                if ord(line[-2]) == 92:
                    line = line[:-2]
                tdata = list(map(int,line[ifst:].split())) 
                mca_data[mca_i:min(mca_i+32,nmca)] = tdata
                mca_i += np.size(tdata)
                if mca_i == nmca:
                    M_mca_data.append(mca_data)
                    mca = False
                continue
            if start  and '#S' in line:
                start = False
    return(np.array(M_mca_data))
