'''
Created on Dec 3, 2014

@author: baskaran_k
'''


from MySQLdb import Connect
from string import atoi,atof,lower
from re import findall
from Bio.PDB import MMCIF2Dict
from commands import getoutput
from os import system
from threading import Thread


class SeqEntropy:
    host=''
    user=''
    passwd=''
    dbname='eppic_2014_10'
    datapath='/media/baskaran_k/data/singlechain'
    cifrepo='/home/baskaran_k/cifrepo'
    def getSurfaceResiudes(self,pdb):
        dbConnection=Connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname)
        cur=dbConnection.cursor()
        cur.execute("select r.residueNumber,r.pdbResidueNumber,r.residueType from Residue as \
        r inner join Interface as i on i.uid=r.interfaceItem_uid where i.pdbCode='%s' \
        and r.region>2 and r.side=1 and i.interfaceId=1"%(pdb))
        self.surface=list(cur.fetchall())
    def getAllignmentFile(self,pdb,chain):
        cmd="wget -O /home/baskaran_k/tmp/%s.aln http://eppic-web.org/ewui/ewui/fileDownload?type=fasta\&id=%s\&alignment=%s "%(pdb,pdb,chain)
        print cmd
        system(cmd)
        self.aln=open("/home/baskaran_k/tmp/%s.aln"%(pdb),'r').read()
    def parseAln(self):
        self.dat=[]
        for dd in self.aln.split("\n"):
            if len(dd)>0 and dd[0]==">":
                self.dat.append("%s:"%(dd))
            else:
                self.dat.append(dd)
        self.dat2="\n".join("".join(self.dat).split(">")[1:])
        self.dat3=findall("(\S+):(\S+)\n",self.dat2)
    def getMapping(self):
        self.map=[]
        j=1
        for i in range(len(self.dat3[0][1])):
            if self.dat3[0][1][i]!="-":
                self.map.append(j)
                j+=1
            else:
                self.map.append(-1)
            
    def getFeq(self):
        n=len(self.dat3[0][1])
        n2=len(self.dat3)
        self.frq=[]
        for i in range(n):
            if self.dat3[0][1][i]!="-":
                x=[]
                for j in range(n2):
                    x.append(self.dat3[j][1][i])
                ss=list(set(x))
                fq=[(float(x.count(k))/float(len(x)),k) for k in ss]
                self.frq.append([i,self.dat3[0][1][i],sorted(fq,reverse=1)]) 
                       
if __name__=="__main__":
    pdbName='2a5l'
    chain="A"
    p=SeqEntropy()
    p.getAllignmentFile(pdbName, chain)
    p.parseAln()
    n=len(p.dat3[0][1])
    p.getMapping()
    p.getSurfaceResiudes(pdbName)
    p.getFeq()
    sr=[p.map.index(atoi(i[1])) for i in p.surface]
    res=[k for k in p.frq if k[0] in sr]
   
    for k in res:
        print "".join([i[1] for i in k[2] if i[0]>0.1])
    
   
    
        
