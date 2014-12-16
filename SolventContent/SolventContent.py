'''
Created on Dec 9, 2014

@author: baskaran_k
'''


from threading import Thread
from re import  findall
from os import system
from commands import getoutput
from sys import argv
from string import atoi,atof
from MySQLdb import Connect

class myThread(Thread):
    host=''
    user=''
    passwd=''
    dbname='eppic_2014_10'
    def __init__(self,threadId,threadName,pdbList,outFile):
        Thread.__init__(self)
        self.threadId=threadId
        self.threadName=threadName
        self.pdbList=pdbList
        self.outFile=outFile
    def getSpaceGroup(self,pdb):
        dbConnection=Connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname)
        cur=dbConnection.cursor()
        cur.execute("select spaceGroup,resolution,rfreeValue,expMethod from PdbInfo where pdbCode='%s'"%(pdb))
        try:
            self.cur=list(cur.fetchall())
            self.sg=self.cur[0][0]
            self.resolution=self.cur[0][1]
            self.rfree=self.cur[0][2]
            self.exp=self.cur[0][3]
        except IndexError:
            self.sg="NULL"
            self.resolution=-1.0
            self.rfree=-1.0
            self.exp="NULL"
        return [self.sg,self.resolution,self.rfree,self.exp]
        
    def getSolventContent(self,pdbName):
        self.pdbName=pdbName
        copyFile="cp /home/baskaran_k/pdbrepo/pdb%s.ent.gz* /home/baskaran_k/tmp/"%(self.pdbName)
        system(copyFile)
        unzipFile="gunzip /home/baskaran_k/tmp/pdb%s.ent.gz*"%(self.pdbName)
        system(unzipFile)
        removeWater="fgrep -v HOH /home/baskaran_k/tmp/pdb%s.ent > /home/baskaran_k/tmp/%s_withoutwater.pdb"%(self.pdbName,self.pdbName)
        system(removeWater)
        sol=findall(r'fraction\s+(\S+)\s+',getoutput("/afs/psi.ch/project/strucbiol/xsoft/phenix-1.9/64/phenix-1.9-1692/build/intel-linux-2.6-x86_64/bin/phenix.f000 /home/baskaran_k/tmp/%s_withoutwater.pdb"%(self.pdbName)))
        try:
            self.solventContent=atof(sol[0])
        except IndexError:
            self.solventContent=-1.0
        except ValueError:
            self.solventContent=-1.0
        removeTmpfile="rm /home/baskaran_k/tmp/*%s*"%(self.pdbName)
        system(removeTmpfile)
        return self.solventContent
    def run(self):
        print "Starting "+ self.threadName
        fo=open(self.outFile,'w')
        for pdb in self.pdbList:
            sgdat=self.getSpaceGroup(pdb)
            outdat="%s\t%s\t%s\t%f\t%f\t%f\n"%(pdb,sgdat[0],sgdat[-1],sgdat[1],sgdat[2],self.getSolventContent(pdb))
            #print outdat
            fo.write(outdat)
        fo.close()
        print "Ending "+self.threadName
        

if __name__=="__main__":
    pdblist=argv[1]
    n=atoi(argv[2])
    plist=open(pdblist,'r').read().split("\n")[:-1]
    sets=range(0,len(plist),len(plist)/n)
    sets[-1]=len(plist)
    th=[]
    for i in range(1,len(sets)):
        pl=plist[sets[i-1]:sets[i]]
        tname="Thread %d"%(i)
        foname="/media/baskaran_k//data/solventcontent/Out_%d.dat"%(i)
        th.append(myThread(i,tname,pl,foname))
        th[-1].start()
