'''
Created on Sep 29, 2014

@author: baskaran_k
'''

from Bio.PDB import *

cifrepo="/home/baskaran_k/"

def readCIF(pdb):
    parser = MMCIFParser()
    print cifrepo,pdb
    structure = parser.get_structure(pdb, '%s/%s.cif'%(cifrepo,pdb))
    for atoms in structure.get_atoms():
        print atoms
if __name__ == '__main__':
    readCIF('1fat')