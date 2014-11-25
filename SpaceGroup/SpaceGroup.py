'''
Created on Nov 21, 2014

@author: baskaran_k
'''


from MySQLdb import Connect
from string import atoi,atof,lower
from re import findall

class SpaceGroup:
    host=''
    user=''
    passwd=''
    dbname='eppic_2014_10'
    datapath='/media/baskaran_k/data/singlechain'
    def getSpaceGroupData(self):
        dbConnection=Connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname)
        cur=dbConnection.cursor()
        cur.execute("select p.pdbCode,p.spaceGroup,count(*) c from PdbInfo as p inner join \
        ChainCluster as c on p.uid=c.pdbInfo_uid inner join Interface as i on \
        i.pdbCode=p.pdbCode where p.numChainClusters=1 and length(c.memberChains)=1 and p.expMethod='X-RAY DIFFRACTION' group by p.pdbCode;")
        self.SpaceGroupData= [i+(self.parseScoresFile(i[0]),) for i in list(cur.fetchall()) if i[0] in self.singleChainList]
        
        
    def getUniqueSpaceGroup(self):
        s=[i[1] for i in self.SpaceGroupData]
        self.UniqueSpaceGroups=list(set(s))
        
    def getMinContactSpaceGroup(self):
        self.MinContacts1=[]
        self.MinContacts2=[]
        for s in self.UniqueSpaceGroups:
            mc1=min([i[2] for i in self.SpaceGroupData if i[1]==s])
            self.MinContacts1.append([s,mc1])
            mc2=min([i[3] for i in self.SpaceGroupData if i[1]==s])
            self.MinContacts2.append([s,mc2])
            
    def getContactFreq(self):
        self.ContactFreq1=[]
        self.ContactFreq2=[]
        for s in self.UniqueSpaceGroups:
            ss=[i[2] for i in self.SpaceGroupData if i[1]==s]
            unique_ss=list(set(ss))
            frq=[]
            for i in unique_ss:
                j=[ss.count(i),i]
                frq.append(j)
            self.ContactFreq1.append([s,sorted(frq)])
            ss=[i[3] for i in self.SpaceGroupData if i[1]==s]
            unique_ss=list(set(ss))
            frq=[]
            for i in unique_ss:
                j=[ss.count(i),i]
                frq.append(j)
            self.ContactFreq2.append([s,sorted(frq)])
            
    def getFilterlist(self):
        self.singleChainList=[lower(i) for i in open('/home/baskaran_k/singleChainPdbList.dat','r').read().split("\n")[:-1]]
    def parseScoresFile(self,pdbName):
        try:
            fname='%s/%s.scores'%(self.datapath,pdbName)
            dat=open(fname,'r').read()
            d=findall(r'\s+(\d+)\s+(\d+)\s+\S+\s+(\S+)\s+(\S+)\s+\d+\s+\d+\s+\d+\s+\S+\s+\n',dat)
            self.interfaceCount=len(d)
        except IOError:
            self.interfaceCount=-1
        return self.interfaceCount
        

            
if __name__=="__main__":
    p=SpaceGroup()
    p.getFilterlist()
    p.getSpaceGroupData()
    p.getUniqueSpaceGroup()
    p.getMinContactSpaceGroup()
    p.getContactFreq()
    n=len(p.ContactFreq1)
    for i in range(n):
        if p.MinContacts1[i][0]==p.ContactFreq1[i][0]:
            print "%s\t%d\t%d\t%d\t%d"%(p.ContactFreq1[i][0],p.MinContacts1[i][1],p.ContactFreq1[i][1][-1][1],p.MinContacts2[i][1],p.ContactFreq2[i][1][-1][1])
