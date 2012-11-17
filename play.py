import os,sys,glob,shutil
import subprocess as sb
import numpy as np
import pylab as p
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
elif not os.path.exists('names.h5'):
    print usagemsg
    sys.exit(-1)

fid = pd.HDFStore('names.h5')
data = fid['names'] 
fid.close()
    
data = data[data['gender'] == 'F']
gb = data.groupby('name')
agged = gb.agg({'count':np.sum ,'year': np.mean}).sort('count', ascending=False)

print "Most 10 popular names over the last 132 years:"
print agged.ix[:10]

print ''

print "'Least' 10 popular names over the last 132 years:"
print agged.ix[-10:]

p.semilogy(agged['count'])
p.grid(True)
p.title('Sorted name histogram over the last 132 years')
p.show()

print "Proportion of female babies given any of the 50 most popular names:"
print np.sum(agged['count'][:50])/np.sum(agged['count'])

auri_count = agged.ix['Auri']['count']
auri_index = agged.index.get_loc('Auri')

def get(num=50, at=17000):
    return agged.index[at:at+num]

print ' '.join(agged[agged.index.map(len)==4].index[200:300])
