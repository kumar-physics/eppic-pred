'''
Created on Dec 11, 2014

@author: kumaran
'''


from MySQLdb import Connect
from string import atoi,atof,lower
from re import findall

class Assembly:
    host=''
    user=''
    passwd=''
    dbname='eppic_2014_10'
    def connectMySql(self):
        dbConnection=Connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname)
        self.cur=dbConnection.cursor()
        
        
    def getAuthorAssembly(self,pdbCode):
        self.pdbCode=pdbCode
        self.cur.execute("select mmSize from Assembly where pdbCode='%s' and method='authors';"%(self.pdbCode))
        try:
            self.mmSize=list(self.cur.fetchall())[0][0]
        except IndexError:
            self.mmSize=-1        
        return self.mmSize
    
if __name__=="__main__":
    p=Assembly()
    p.connectMySql()
    f=open('/home/kumaran/spacegroup/done.list','r')
    for l in f:
        w=l.split("\n")[0].split("\t")
        ss=p.getAuthorAssembly(w[0])
        if ss==1:
            ssname="Monomer"
        elif ss==2:
            ssname="Dimer"
        elif ss==3:
            ssname="Trimer"
        elif ss==4:
            ssname="Tetramer"
        elif ss==5:
            ssname="Pentamer"
        elif ss==6:
            ssname="Hexamer"
        elif ss==7:
            ssname="Heptamer"
        elif ss==8:
            ssname="Octamer"
        elif ss==9:
            ssname="Nonamer"
        elif ss==10:
            ssname="Decamer"
        elif ss==-1:
            ssname="Undefined"
        else:
            ssname="%d-mer"%(ss)
        aa=w[1].count("2")
        if aa==0:
            two="without"
        else:
            two="with"
        print "%s\t%s\t%s"%(l.split("\n")[0],ssname,two)
        