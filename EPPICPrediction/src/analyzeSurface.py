'''
Created on Oct 8, 2014

@author: baskaran_k
'''
from getDistanceMatrix import getDistanceMatrix
from getSurfaceResidues import getSurfaceResidues
from random import sample
from pylab import mean,var,sqrt
from MySQLdb import Connect
from scipy.stats.mstats import zscore

class analyzeSurface(object):
    
    def calZsocre(self,core,surface,sampleSize):
        coreMean=mean(core)
        s=[]
        for i in range(sampleSize):
            s.append(mean(sample(surface,len(core))))
        sig= sqrt(var(s))
        return (coreMean-mean(s))/sig
    def calMeanZ(self,coreR,surfR,zscores):
        z2=[]
        for i in coreR:
            z2.append(zscores[surfR.index(i)])
        return [mean(z2),sqrt(var(z2))]
    
    def scanSurface(self,pdb,chain,interface,side,cifrepo,host,user,passwd,dbname,n,coreSize,sampleSize,outfolder):
        print "Working on pdb %s"%(pdb)
        s=getSurfaceResidues()
        d=getDistanceMatrix()
        surfaceEntropies=s.getSurfaceEntropies(pdb, interface, side, host, user, passwd, dbname)
        surfaceRes=surfaceEntropies[0]
        surfaceEnt=surfaceEntropies[1]
        surfDist=d.surfaceDistances(pdb, chain, interface, side, host, user, passwd, dbname, cifrepo)
        surfRes=surfDist[0]
        distMatrix=surfDist[1]
        foname="%s/%s_zscore.dat"%(outfolder,pdb)
        fo=open(foname,'w')
        fo.write("ref\tres\torder\tavgz\tsigz\tpdb\tc\n")
        #zs=zscore(surfaceEnt)
        zs=surfaceEnt

        for r in range(n):
            coreSize=r
            refRes=sample(surfRes,1)[0]
            print "Working around residue %d in pdb %s"%(refRes,pdb)
            sortedRes=sorted([[distMatrix[surfRes.index(refRes)][i],surfRes[i]] for i in range(len(surfRes))])
            for res in sortedRes:
                ref=res[1]
                sortedRes2=sorted([[distMatrix[surfRes.index(ref)][i],surfRes[i]] for i in range(len(surfRes))])
                coreRes=[k[1] for k in sortedRes2][1:coreSize+1]
                #coreEnt=[surfaceEnt[surfaceRes.index(m)] for m in coreRes]
                #surEnt=[surfaceEnt[surfaceRes.index(c)] for c in surfaceRes if c not in coreRes]
                #z=self.calZsocre(coreEnt, surfaceEnt, sampleSize)
                #z=self.calZsocre(coreEnt, surEnt, sampleSize)
                z=self.calMeanZ(coreRes, surfaceRes, zs)
                fo.write("%d\t%d\t%d\t%f\t%f\t%s\tc%d\n"%(refRes,ref,sortedRes.index(res),z[0],z[1],pdb,r))
        fo.close()
                
    def runDataset(self,dataset,interface, side, cifrepo, host, user, passwd, dbname, n, coreSize, sampleSize, outfolder):
        p=analyzeSurface()
        db=Connect(host=host,user=user,passwd=passwd,db=dbname)
        cur = db.cursor()
        cur.execute("select pdbCode,chain1 from dc_%s where h1>30 and h2>30 and repchain1=repchain2"%(dataset))
        pdblist=cur.fetchall()
        pdbl=[pdb[0] for pdb in list(pdblist)]
        chains=[pdb[1] for pdb in list(pdblist)]
        for pdb in set(pdbl):
            try:
                p.scanSurface(pdb,chains[pdbl.index(pdb)],interface, side, cifrepo, host, user, passwd, dbname, n, coreSize, sampleSize, outfolder)
            except ValueError:
                print pdb
                pass
                
            except IOError:
                print pdb
                pass
#1m4n
        
      
            
if __name__=="__main__":
    from sys import argv
    from string import atoi
    p=analyzeSurface()
    p.runDataset(argv[1], atoi(argv[2]), atoi(argv[3]), argv[4], argv[5], argv[6], argv[7], argv[8], atoi(argv[9]), atoi(argv[10]), atoi(argv[11]), argv[12])