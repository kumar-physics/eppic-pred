'''
Created on Oct 8, 2014

@author: baskaran_k
'''
from MySQLdb import Connect
from string import atoi

class getSurfaceResidues(object):
    
    def getSurfaceEntropies(self,pdb,interface,side,host,user,passwd,dbname):
        self.pdb=pdb
        self.interface=interface
        self.side=side
        dbConnection=Connect(host=host,user=user,passwd=passwd,db=dbname)
        cur=dbConnection.cursor()
        cur.execute("select r.pdbResidueNumber,r.region,r.entropyScore \
        from Residue as r inner join Interface as i on i.uid=r.interfaceItem_uid \
        where i.pdbCode='%s' and i.interfaceId=%d and r.side=%d and r.region>=0;"%(self.pdb,self.interface,self.side))
        self.entropyScore= list(cur.fetchall())
        if len(self.entropyScore)==0:
            raise ValueError('PDB entry not found in the database')
        self.surfaceResidues=[atoi(res[0]) for res in self.entropyScore]
        self.surfaceEntropies=[res[2] for res in self.entropyScore]
        return [self.surfaceResidues,self.surfaceEntropies]
    def get70CoreEntropies(self,pdb,interface,side,host,user,passwd,dbname):
        self.pdb=pdb
        self.interface=interface
        self.side=side
        dbConnection=Connect(host=host,user=user,passwd=passwd,db=dbname)
        cur=dbConnection.cursor()
        cur.execute("select r.pdbResidueNumber,r.region,r.entropyScore \
        from Residue as r inner join Interface as i on i.uid=r.interfaceItem_uid \
        where i.pdbCode='%s' and i.interfaceId=%d and r.side=%d and r.region>0;"%(self.pdb,self.interface,self.side))
        self.coreEntropyScore= list(cur.fetchall())
        if len(self.coreEntropyScore)==0:
            raise ValueError('PDB entry not found in the database')
        self.coreResidues=[atoi(res[0]) for res in self.coreEntropyScore]
        self.coreEntropies=[res[2] for res in self.coreEntropyScore]
        return [self.coreResidues,self.coreEntropies]
    def get95CoreEntropies(self,pdb,interface,side,host,user,passwd,dbname):
        self.pdb=pdb
        self.interface=interface
        self.side=side
        dbConnection=Connect(host=host,user=user,passwd=passwd,db=dbname)
        cur=dbConnection.cursor()
        cur.execute("select r.pdbResidueNumber,r.region,r.entropyScore \
        from Residue as r inner join Interface as i on i.uid=r.interfaceItem_uid \
        where i.pdbCode='%s' and i.interfaceId=%d and r.side=%d and r.region>1;"%(self.pdb,self.interface,self.side))
        self.coreEntropyScore= list(cur.fetchall())
        if len(self.coreEntropyScore)==0:
            raise ValueError('PDB entry not found in the database')
        self.coreResidues=[atoi(res[0]) for res in self.coreEntropyScore]
        self.coreEntropies=[res[2] for res in self.coreEntropyScore]
        return [self.coreResidues,self.coreEntropies]  
if __name__=="__main__":
    from sys import argv
    p=getSurfaceResidues()
    p.getSurfaceEntropies(argv[1],argv[2],argv[3], argv[4], argv[5], argv[6], argv[7])