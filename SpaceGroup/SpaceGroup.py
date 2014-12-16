'''
Created on Nov 21, 2014

@author: baskaran_k
'''


from MySQLdb import Connect
from string import atoi,atof,lower
from re import findall
from Bio.PDB import MMCIF2Dict
from commands import getoutput
from os import system
from threading import Thread
#2d4j heavy water
#4p3r,4pth multiple models sol=100%
class SpaceGroup:
    host=''
    user=''
    passwd=''
    dbname='eppic_2014_10'
    datapath='/media/baskaran_k/data/singlechain'
    cifrepo='/home/baskaran_k/cifrepo'
    def getSpaceGroupData(self):
        dbConnection=Connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname)
        cur=dbConnection.cursor()
        cur.execute("select p.pdbCode,p.spaceGroup,count(*) c from PdbInfo as p inner join \
        ChainCluster as c on p.uid=c.pdbInfo_uid inner join Interface as i on \
        i.pdbCode=p.pdbCode where p.numChainClusters=1 and length(c.memberChains)=1 and p.expMethod='X-RAY DIFFRACTION' group by p.pdbCode;")
        self.SpaceGroupData= [i+(self.parseScoresFile(i[0]),) for i in list(cur.fetchall()) if i[0] in self.singleChainList and self.parseScoresFile(i[0])>0 ]
    def getSpaceGroup(self,pdb):
        dbConnection=Connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname)
        cur=dbConnection.cursor()
        cur.execute("select spaceGroup from PdbInfo where pdbCode='%s'"%(pdb))
        try:
            self.sg=list(cur.fetchall())[0][0]
        except IndexError:
            self.sg="NULL"
        return self.sg
        
    def getSolventContent(self,pdbName):
        try:
            mmcif=MMCIF2Dict.MMCIF2Dict("%s/%s.cif.gz"%(self.cifrepo,pdbName))
            try:
                sol=atof(mmcif['_exptl_crystal.density_percent_sol'])
            except TypeError:
                sol=-1.0
            except ValueError:
                sol=-1.0
            except KeyError:
                sol=-1.0
        except ValueError:
            sol=-1.0
            print pdbName,"parsing problem"
        return sol
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
        self.singleChainList=[lower(i) for i in open('/home/baskaran_k/singleChainPdbList2.dat','r').read().split("\n")[:-1]]
    def parseScoresFile(self,pdbName):
        try:
            fname='%s/%s.scores'%(self.datapath,pdbName)
            dat=open(fname,'r').read()
            d=findall(r'\s+(\d+)\s+(\d+)\s+\S+\s+(\S+)\s+(\S+)\s+\d+\s+\d+\s+\d+\s+\S+\s+\n',dat)
            self.interfaceCount=len(d)
        except IOError:
            self.interfaceCount=-1
        return self.interfaceCount
        
    def getSolventContPhenix(self,pdb):
        sol=findall(r'fraction\s+(\S+)\s+',getoutput("/afs/psi.ch/project/strucbiol/xsoft/phenix-1.9/64/phenix-1.9-1692/build/intel-linux-2.6-x86_64/bin/phenix.f000 /home/baskaran_k/pdbrepo/*%s*"%(pdb)))
        try:
            ss=sol[0]
        except IndexError:
            ss=-1.0
        return ss
    def getSolventContentPhenixWithoutWater(self,pdb):
        cmd1="cp /home/baskaran_k/pdbrepo/pdb%s.ent.gz* /home/baskaran_k/tmp/"%(pdb)
        system(cmd1)
        cmd2="gunzip /home/baskaran_k/tmp/pdb%s.ent.gz*"%(pdb)
        system(cmd2)
        cmd3="fgrep -v HOH /home/baskaran_k/tmp/pdb%s.ent > /home/baskaran_k/tmp/%s_withoutwater.pdb"%(pdb,pdb)
        system(cmd3)
        sol=findall(r'fraction\s+(\S+)\s+',getoutput("/afs/psi.ch/project/strucbiol/xsoft/phenix-1.9/64/phenix-1.9-1692/build/intel-linux-2.6-x86_64/bin/phenix.f000 /home/baskaran_k/tmp/%s_withoutwater.pdb"%(pdb)))
        try:
            ss=sol[0]
        except IndexError:
            ss=-1.0
        cmd4="rm /home/baskaran_k/tmp/*%s*"%(pdb)
        system(cmd4)
        return ss    
    
class myThread(Thread):
    host=''
    user=''
    passwd=''
    dbname='eppic_2014_10'
    datapath='/media/baskaran_k/data/singlechain'
    cifrepo='/home/baskaran_k/cifrepo'
    def __init__(self,threadID,name,sdata,foname):
        Thread.__init__(self)
        self.threadId=threadID
        self.name=name
        self.sdata=sdata
        self.foname=foname
    def runold(self):
        print "Starting "+ self.name
        fo=open(self.foname,'w')
        for ddd in self.sdata:
            self.datout="%s\t%s\t%d\t%d\t%.2f\t%.2f\t%.2f"%(ddd[0],ddd[1],ddd[2],ddd[3],atof(self.getSolventContent(ddd[0])),100.0*atof(self.getSolventContPhenix(ddd[0])),100.0*atof(p.getSolventContentPhenixWithoutWater(ddd[0])))
            fo.write("%s\n"%(self.datout))
        fo.close()
        print "Finished"+self.name
        
    def getSpaceGroup(self,pdb):
        dbConnection=Connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname)
        cur=dbConnection.cursor()
        cur.execute("select spaceGroup from PdbInfo where pdbCode='%s'"%(pdb))
        try:
            self.sg=list(cur.fetchall())[0][0]
        except IndexError:
            self.sg="NULL"
        return self.sg    
    def run(self):
        print "Starting "+ self.name
        fo=open(self.foname,'w')
        for ddd in self.sdata:
            self.datout="%s\t%s\t%.2f"%(ddd,self.getSpaceGroup(ddd),100.0*atof(self.getSolventContentPhenixWithoutWater(ddd)))
            print self.datout
            fo.write("%s\n"%(self.datout))
        fo.close()
        print "Finished"+self.name
    def getSolventContent(self,pdbName):
        try:
            mmcif=MMCIF2Dict.MMCIF2Dict("%s/%s.cif.gz"%(self.cifrepo,pdbName))
            try:
                sol=atof(mmcif['_exptl_crystal.density_percent_sol'])
            except TypeError:
                sol=-1.0
            except ValueError:
                sol=-1.0
            except KeyError:
                sol=-1.0
        except ValueError:
            sol=-1.0
            print pdbName,"parsing problem"
        return sol
    
        
        
    def getSolventContPhenix(self,pdb):
        sol=findall(r'fraction\s+(\S+)\s+',getoutput("/afs/psi.ch/project/strucbiol/xsoft/phenix-1.9/64/phenix-1.9-1692/build/intel-linux-2.6-x86_64/bin/phenix.f000 /home/baskaran_k/pdbrepo/*%s*"%(pdb)))
        try:
            ss=sol[0]
        except IndexError:
            ss=-1.0
        return ss
    def getSolventContentPhenixWithoutWater(self,pdb):
        cmd1="cp /home/baskaran_k/pdbrepo/pdb%s.ent.gz* /home/baskaran_k/tmp/"%(pdb)
        system(cmd1)
        cmd2="gunzip /home/baskaran_k/tmp/pdb%s.ent.gz*"%(pdb)
        system(cmd2)
        cmd3="fgrep -v HOH /home/baskaran_k/tmp/pdb%s.ent > /home/baskaran_k/tmp/%s_withoutwater.pdb"%(pdb,pdb)
        system(cmd3)
        sol=findall(r'fraction\s+(\S+)\s+',getoutput("/afs/psi.ch/project/strucbiol/xsoft/phenix-1.9/64/phenix-1.9-1692/build/intel-linux-2.6-x86_64/bin/phenix.f000 /home/baskaran_k/tmp/%s_withoutwater.pdb"%(pdb)))
        try:
            ss=sol[0]
        except IndexError:
            ss=-1.0
        cmd4="rm /home/baskaran_k/tmp/*%s*"%(pdb)
        system(cmd4)
        return ss       
    
    
if __name__=="__main__":
    p=SpaceGroup()
#    print p.getSolventContPhenix('1ynu'), p.getSolventContentPhenixWithoutWater('1ynu')
    #p.getSolventContent('2gs2')
    pdblist=open('/home/baskaran_k/memb/mm2.list','r').read().split("\n")[:-1]
    
   
    
#     p.getFilterlist()
#     p.getSpaceGroupData()
    n=len(pdblist)
    nt=8
    sets=range(0,n,n/nt)
    sets[-1]=n
    th=[]
    for i in range(1,len(sets)):
        threadName="Thread%d"%(i)
        setd=pdblist[sets[i-1]:sets[i]]
        foname="/home/baskaran_k/memb/spaceGroupdat_%d.dist"%(i)
        th.append(myThread(i,threadName,setd,foname))
        th[-1].start()
         
# 

    
    
    
 #   for ddd in p.SpaceGroupData:
#          #if ddd[3]>0 and ddd[1]=='P 2 2 2': # or (ddd[1]=='C 2 2 21' and ddd[3]<3) or (ddd[1]=='P 1 21 1' and ddd[3]<3)):
#         print "%s\t%s\t%d\t%d\t%.2f\t%.2f\t%.2f"%(ddd[0],ddd[1],ddd[2],ddd[3],atof(p.getSolventContent(ddd[0])),100.0*atof(p.getSolventContPhenix(ddd[0])),100.0*atof(p.getSolventContentPhenixWithoutWater(ddd[0])))
#     p.getUniqueSpaceGroup()
#     p.getMinContactSpaceGroup()
#     p.getContactFreq()
#     n=len(p.ContactFreq1)
#     for i in range(n):
#         if p.MinContacts1[i][0]==p.ContactFreq1[i][0]:
#             print "%s\t%d\t%d\t%d\t%d"%(p.ContactFreq1[i][0],p.MinContacts1[i][1],p.ContactFreq1[i][1][-1][1],p.MinContacts2[i][1],p.ContactFreq2[i][1][-1][1])
