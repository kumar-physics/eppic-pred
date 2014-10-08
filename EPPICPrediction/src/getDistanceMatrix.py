'''
Created on Oct 8, 2014

@author: baskaran_k
'''
from Bio.PDB import MMCIFParser
from getSurfaceResidues import getSurfaceResidues

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
        return [surfaceResidues,distances]
            
if __name__=="__main__":
    from sys import argv
    p=getDistanceMatrix()
    p.surfaceDistances(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9])