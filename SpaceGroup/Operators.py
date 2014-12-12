'''
Created on Dec 11, 2014

@author: kumaran
'''

from re import findall
from fractions import Fraction
from numpy import array
from numpy import trace
from numpy import linalg
from numpy import matrix
class Operator:
    vector={'X':[1.0,0.0,0.0,0.0],'+X':[1.0,0.0,0.0,0.0],'-X':[-1.0,0.0,0.0,0.0],\
            'Y':[0.0,1.0,0.0,0.0],'+Y':[0.0,1.0,0.0,0.0],'-Y':[0.0,-1.0,0.0,0.0],\
            'Z':[0.0,0.0,1.0,0.0],'+Z':[0.0,0.0,1.0,0.0],'-Z':[0.0,0.0,-1.0,0.0]}
    def parseOperator(self,opr):
        self.opr=opr
        #Do not split the regular expression syntax, its not working when I use \ to split lines. Probably it considers that also part of the expression
        e=findall(r'([+-]*\d[/\d]*)([+-]\w)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)([+-]\w)([+-]\d[/\d]*)|([+-]*\d[/\d]*)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)([+-]\d[/\d]*)|([+-]*\d[/\d]*)([+-]\w)|([+-]*\w)([+-]\d[/\d]*)|([+-]*\w)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)|([+-]*\w),([+-]*\d[/\d]*)([+-]\w)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)([+-]\w)([+-]\d[/\d]*)|([+-]*\d[/\d]*)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)([+-]\d[/\d]*)|([+-]*\d[/\d]*)([+-]\w)|([+-]*\w)([+-]\d[/\d]*)|([+-]*\w)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)|([+-]*\w),([+-]*\d[/\d]*)([+-]\w)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)([+-]\w)([+-]\d[/\d]*)|([+-]*\d[/\d]*)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)([+-]\d[/\d]*)|([+-]*\d[/\d]*)([+-]\w)|([+-]*\w)([+-]\d[/\d]*)|([+-]*\w)([+-]\w)([+-]\w)|([+-]*\w)([+-]\w)|([+-]*\w)',self.opr)
        self.OperatorList=[filter(None,list(i)) for i in e]
        return self.OperatorList
    def operator2vecotor(self,singleopr):
        vec=array([0.0,0.0,0.0,0.0])
        for e in singleopr:
            if e in self.vector.keys():
                vec=vec+self.vector[e]
            else:
                vec=vec+array([0.0,0.0,0.0,float(Fraction(e))])
        return vec
    def operator2matrix(self,opr):
        self.parseOperator(opr)
        self.opmatrix=array([self.operator2vecotor(self.OperatorList[0]),\
                             self.operator2vecotor(self.OperatorList[1]),\
                             self.operator2vecotor(self.OperatorList[2]),\
                             array([0.0,0.0,0.0,1.0])])
        return self.opmatrix
    
    
    def omega(self,opmatrix):
        k=self.axisType(opmatrix)
        op=opmatrix.transpose()[:3].transpose()[:3]
        t=opmatrix.transpose()[3:].transpose()[:3]
        nullvec=array([0.0,0.0,0.0])
        Y=array([nullvec,nullvec,nullvec])
        for i in range(k):
            Y+=linalg.matrix_power(op, i)
        Y1=Y/k
        t1=t/k
        a=matrix.dot(t1.transpose(),Y1)
        return t1
        
    def axisType(self,opmatrix):
        d=linalg.det(opmatrix)
        t=trace(opmatrix)-1#trace of only operator not including translation
        if d>0:
            if t==3:
                ax=1
            elif t==-1:
                ax=2
            elif t==0:
                ax=3
            elif t==1:
                ax=4
            elif t==2:
                ax=6
            else:
                ax=0
        elif d<0:
            if t==-3:
                ax=-1
            elif t==1:
                ax=-2
            elif t==0:
                ax=-3
            elif t==-1:
                ax=-4
            elif t==-2:
                ax=-6
            else:
                ax=0
        else:
            ax=100
        return ax
            
                
                
        


if __name__=="__main__":
    p=Operator()
    f=open('/home/kumaran/symop.lib','r').read().split("\n")
    for l in f:
        n=len(l.split(" "))
        if n==2:
            op=l.split(" ")[1]
            #print op
            m=p.operator2matrix(op)
            print op,p.omega(m),p.axisType(m)
# testing
#     p.op2matrix('X+Y+Z-1/3')
#     p.op2matrix('-X+Y+Z-1/3')
#     p.op2matrix('X+Y+Z-1')
#     p.op2matrix('-X+Y+Z-3')
#     p.op2matrix('1/3-X+Y+Z')
#     p.op2matrix('-1/3-X+Y+Z')
#     p.op2matrix('1-X+Y+Z')
#     p.op2matrix('3-X+Y+Z')
#     p.op2matrix('X+Y-1/3')
#     p.op2matrix('-X+Z-1/3')
#     p.op2matrix('X+Z-1')
#     p.op2matrix('-X+Z-3')
#     p.op2matrix('1/3-X+Z')
#     p.op2matrix('-1/3-X+Z')
#     p.op2matrix('1-X+Z')
#     p.op2matrix('3-X+Z')
#     p.op2matrix('X-1/3')
#     p.op2matrix('-X-1/3')
#     p.op2matrix('X-1')
#     p.op2matrix('-X-3')
#     p.op2matrix('1/3-X')
#     p.op2matrix('-1/3-X')
#     p.op2matrix('1-X')
#     p.op2matrix('3-X')
#     p.op2matrix('X+Y+Z')
#     p.op2matrix('-X+Y+Z')
#     p.op2matrix('X+Y')
#     p.op2matrix('-Y+Z')
#     p.op2matrix('X')
#     p.op2matrix('-Z')