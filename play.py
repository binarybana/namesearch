import os,sys,glob,shutil
import subprocess as sb
import numpy as np
import pandas as pd

usagemsg = "Usage: %s <location of zipped names>"
if len(sys.argv) == 2:
    assert os.path.exists(sys.argv[1]), usagemsg
    print sys.argv[1]
    assert sb.check_call(('unzip -u %s -d rawdata'%sys.argv[1]).split())==0, "Had problem unpacking data"
    files = glob.glob('rawdata/*.txt')
    data = pd.DataFrame()
    for fname in files:
        x = pd.read_csv(fname, header=None, names=['name','gender','count'])
        x['year'] = int(fname[11:-4])
        data = data.append(x, ignore_index=True)
    fid = pd.HDFStore('names.h5', complib='blosc', complevel=9)
    fid['names'] = data
    fid.close()
    shutil.rmtree('rawdata')
elif os.path.exists('names.h5'):
    fid = pd.HDFStore('names.h5')
    data = fid['names'] 
    fid.close()
else:
    print usagemsg
    sys.exit(-1)
    
data = data[data['gender'] == 'F']
gb = data.groupby('name')
agged = gb.agg({'count':np.sum ,'year': np.mean}).sort('count', ascending=False)

print "Most 20 popular names over the last 132 years:"
print agged.ix[:10]

print "'Least' 20 popular names over the last 132 years:"
print agged.ix[-10:]

