'''
Created on Oct 29, 2014

@author: baskaran_k
'''


from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import threading

outpath='/home/baskaran_k/biounit'
class myThread(threading.Thread):
    def __init__(self,threadID,name,pdblist,s1,s2,assembly,foname):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pdblist=pdblist
        self.s1=s1
        self.s2=s2
        self.assembly=assembly
        self.foname=foname
    def run(self):
        for self.pdb in self.pdblist[self.s1:self.s2]:
            self.fo=open("%s/%s"%(outpath,self.foname),'w')
            #print self.name,self.pdb
            self.assembly.parseMMCIF(self.pdb)
            self.assembly.getAsymDetails()
            self.assembly.getAssemblyDetails()
            if isinstance(self.assembly.assemblyId, list) and self.assembly.protentryId[0]>1:
                self.assembly.getOligomers()
                if len(list(set(self.assembly.oligomerCount)))>1:
                    outdat="%s\t%s\t%s"%(self.pdb,"-".join(self.assembly.oligomerCount),"-".join(self.assembly.composition))
                    print self.name,outdat
                    self.fo.write("%s\n"%(outdat))
            self.fo.close()
        

class BioUnit:
    cifrepo='/home/baskaran_k/cifrepo'
    def parseMMCIF(self,pdbId):
        self.pdbId=pdbId
        self.mmcifFile="%s/%s.cif.gz"%(self.cifrepo,self.pdbId)
        self.mmcif=MMCIF2Dict(self.mmcifFile)

    def getAsymDetails(self):
        self.entryId=self.mmcif['_entity_poly.entity_id']
        self.polyType=self.mmcif['_entity_poly.type']
        self.asymId=self.mmcif['_struct_asym.id']
        self.entryIdmap=self.mmcif['_struct_asym.entity_id']
        self.strandId=self.mmcif['_entity_poly.pdbx_strand_id']
        if isinstance(self.entryId, list):
            self.protentryId=[self.entryId[i] for i in range(len(self.polyType)) if self.polyType[i]=='polypeptide(L)']
            if 'polypeptide(L)' not in self.polyType:
                self.protentryId=[-1]
        else:
            if self.polyType=='polypeptide(L)':
                self.protentryId=[self.entryId]
            else:
                self.protentryId=[-1]
                
    def getAssemblyDetails(self):
        self.assemblyId=self.mmcif['_pdbx_struct_assembly.id']
        self.oligomerCount=self.mmcif['_pdbx_struct_assembly.oligomeric_count']
        self.assemblygenId=self.mmcif['_pdbx_struct_assembly_gen.assembly_id']
        self.opExp=self.mmcif['_pdbx_struct_assembly_gen.oper_expression']
        self.assemblyAsymId=self.mmcif['_pdbx_struct_assembly_gen.asym_id_list']
    def getOligomers(self):
        self.chains=[self.asymId[i] for i in range(len(self.entryIdmap)) if self.entryIdmap[i] in self.protentryId]
        self.composition=[]
        c1=[]
        for i in range(len(self.assemblyAsymId)):
            oper=len(self.opExp[i].split(","))
            c="".join(["%s%d"%(k,oper*self.assemblyAsymId[i].split(",").count(k)) for k in self.chains if self.assemblyAsymId[i].split(",").count(k)>0])
            c1.append(c)
        for i in self.assemblyId:
            c2="".join([c1[k] for k in range(len(self.assemblygenId)) if self.assemblygenId[k]==i])
            self.composition.append(c2)
if __name__=="__main__":
    pdblist=open('/home/baskaran_k/pdb_all.list','r').read().split("\n")[:-1]
    nt=4
    sets=range(0,len(pdblist),len(pdblist)/nt)
    sets[-1]=len(pdblist)
    print sets
    th=[]
    for i in range(1,len(sets)):
        threadName="Thread%03d"%(i)
        foname="thread_%03d.out"%(i)
        th.append(myThread(i,threadName,pdblist,sets[i-1],sets[i],BioUnit(),foname))
        th[-1].start()
    #t1=myThread(1,'thread1',pdblist,10,100,BioUnit())
    #t2=myThread(2,'thread2',pdblist,100,200,BioUnit())
    #t1.start()
    #t2.start()
#     for pdb in pdblist:
#     #pdb='1a52'
#         #print pdb
#         p=BioUnit()
#         p.parseMMCIF(pdb)
#         p.getAsymDetails()
#         p.getAssemblyDetails()
#         if isinstance(p.assemblyId, list) and p.protentryId[0]>1:
#             p.getOligomers()
#             if len(list(set(p.oligomerCount)))>1:
#                 print pdb,p.oligomerCount,p.composition
#                 #print pdb,p.assemblygenId,p.composition,p.assemblyId,p.oligomerCount