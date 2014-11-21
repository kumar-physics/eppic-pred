'''
Created on Oct 8, 2014

@author: baskaran_k
'''
from Bio.PDB import MMCIFParser
from getSurfaceResidues import getSurfaceResidues
from Bio.PDB import NeighborSearch
from random import random
class getDistanceMatrix(object):
    
    def parseMMCIF(self,pdb,chain,cifrepo):
        self.pdb=pdb
        parser = MMCIFParser()
        structure = parser.get_structure(self.pdb, "%s/%s.cif.gz"%(cifrepo,self.pdb))
        firstModel = structure.get_list()[0]
        firstChain = firstModel[chain]
        return firstChain
        
    def surfaceDistances(self,pdb,chain,interface,side,host,user,passwd,dbname,cifrepo):
        g=getSurfaceResidues()
        s=g.getSurfaceEntropies(pdb, interface, side, host, user, passwd, dbname)
        surfaceResidues=s[0]
        residueList=self.parseMMCIF(pdb, chain, cifrepo)
        surfaceR=[residueList[i]['CA'] for i in surfaceResidues]
        for i in surfaceResidues:
            try:
                residueList[i]['CA']
            except KeyError:
                try:
                    residueList[i]['CB']
                except KeyError:
                    surfaceResidues.remove(i)
        distances=[]
        for i in surfaceResidues:
            distances.append([])
            for j in surfaceResidues:
                try:
                    d=residueList[i]['CB']-residueList[j]['CB']
                except KeyError:
                    d=residueList[i]['CA']-residueList[j]['CA']
                distances[-1].append(d)
        ns=NeighborSearch(surfaceR)
        k=1
        for i in surfaceR:
            print "set_color c%d, [%f,%f,%f]"%(k,random(),random(),random())
            print "create s%d, resi %s"%(k,"+".join(["%d"%(r.get_id()[1]) for r in ns.search(i.coord, 5.0, 'R')]))
            print "show surface, s%d"%(k)
            print "color c%d, s%d"%(k,k)
            k+=1
        return [surfaceResidues,distances]
            
if __name__=="__main__":
    p=getDistanceMatrix()
    #p.parseMMCIF('2gs2', 'A', '/home/baskaran_k/cifrepo')
    p.surfaceDistances('2gs2', 'A', 1, 1, 'mpc1153', 'root', 'edb+1153', 'eppic_2_1_0_2014_05', '/home/baskaran_k/cifrepo')
    #from sys import argv
    #p=getDistanceMatrix()
    #p.surfaceDistances(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9])