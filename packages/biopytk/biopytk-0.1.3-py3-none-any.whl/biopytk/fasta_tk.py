# FASTA Toolkit
# Last updated: 8/30/23
#
# This module contains FASTA file analysis tools. 
#
# Classes included in this file:
#   - sequenceBuilder
#   - structs
#   - bio_seq
#
# https://www.stephendoescomp.bio
# Stephen Cheney © 2023

from structs import *
from sequenceBuilder import *
from bio_seq import *

def percentGC_fasta(seq):
    """
    Return GC percentage of a DNA sequence in % form
    \n<- bio_seq obj
    \n-> float
    """
    temp_seq = bio_seq(seq)
    bases = len(seq)
    return float(temp_seq.nucFrequencyDict()['G']/bases * 100) + float(temp_seq.nucFrequencyDict()['C']/bases * 100)


def gcContentFromFASTA(fasta_File):
    """
    Given a FASTA file, return a dict of sequence names and their respective GC content
    \n<- fasta_File: FASTA formatted file 
    \n-> dict
    """
    seqDict = seqsFromFASTA(fasta_File)
    gcDict = {k:percentGC_fasta(v) for k,v in seqDict.items()}
    return gcDict


def getMaxGCFromFASTA(fasta_File):
    """
    Given a FASTA file, return the sequence with the largest GC content
    \n<- fasta_File: FASTA formatted file 
    \n-> dict
    """    
    gcDict = gcContentFromFASTA(fasta_File)
    maxKey = max(gcDict, key=gcDict.get)
    return {maxKey:gcDict[maxKey]}
