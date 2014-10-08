'''
Created on Oct 8, 2014

@author: baskaran_k
'''
from getDistanceMatrix import getDistanceMatrix
from getSurfaceResidues import getSurfaceResidues
from random import sample
from pylab import mean,var,sqrt
from MySQLdb import Connect
class analyzeSurface(object):
    
    def calZsocre(self,core,surface,sampleSize):
        coreMean=mean(core)
        s=[]
        for i in range(sampleSize):
            s.append(mean(sample(surface,len(core))))
        sig= sqrt(var(s))
        return (coreMean-mean(s))/sig
    
    def scanSurface(self,pdb,chain,interface,side,cifrepo,host,user,passwd,dbname,n,coreSize,sampleSize,outfolder):
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
        fo.write("ref\tres\torder\tz\tpdb\n")
        for r in range(n):
            refRes=sample(surfRes,1)[0]
            print "Working around residue %d in pdb %s"%(refRes,pdb)
            sortedRes=sorted([[distMatrix[surfRes.index(refRes)][i],surfRes[i]] for i in range(len(surfRes))])
            for res in sortedRes:
                ref=res[1]
                sortedRes2=sorted([[distMatrix[surfRes.index(ref)][i],surfRes[i]] for i in range(len(surfRes))])
                coreRes=[k[1] for k in sortedRes2][1:coreSize+1]
                coreEnt=[surfaceEnt[surfaceRes.index(m)] for m in coreRes]
                surEnt=[surfaceEnt[surfaceRes.index(c)] for c in surfaceRes if c not in coreRes]
                #z=self.calZsocre(coreEnt, surfaceEnt, sampleSize)
                z=self.calZsocre(coreEnt, surEnt, sampleSize)
                fo.write("%d\t%d\t%d\t%f\t%s\n"%(refRes,ref,sortedRes.index(res),z,pdb))
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
                
                

        
      
            
if __name__=="__main__":
    from sys import argv
    p=analyzeSurface()
    p.runDataset(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9], argv[10], argv[11], argv[12])
