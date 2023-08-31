# Bio Seq Toolkit
# Last updated: 8/30/23
#
# This module contains DNA/RNA sequencing tools. 
#
# Classes included in this file:
#   - sequenceBuilder
#   - structs
#   - aa_seq
#
# https://www.stephendoescomp.bio
# Stephen Cheney © 2023

import collections
from structs import *
from sequenceBuilder import *
from aa_seq import *

class bio_seq():
    def __init__(self, seq = "ACTG", seq_type = 'DNA', label = 'No Label'):
        self.seq = seq.upper()
        self.seq_type = seq_type
        self.label = label
        self.is_valid = self.validateSeq()
        assert self.is_valid, f"Input {seq_type} sequence is invalid: {self.seq}"


    def validateSeq(self):
        """
        Return True if input sequence is a valid DNA sequence, return False otherwise
        \n<- bio_seq obj
        \n-> bool
        """
        if self.seq_type == 'DNA':
            return set(nucleotides).issuperset(self.seq)
        if self.seq_type == 'RNA':
            return set(rnaNucleotides).issuperset(self.seq)
        else:
            return False


    def printSeq(self, direc):
        """
        Return an annotated DNA sequence in given direction
        \nNotes: direc - 'f' for (5' -> 3'), 'r' for (3' -> 5')
        \n<- bio_seq obj, direc: chr
        \n-> str
        """
        if direc == 'f':
            return '5\' ' + self.seq + ' 3\''
        if direc == 'r':
            return '3\' ' + self.seq + ' 5\''
        

    def nucFrequencyDict(self):
        """
        Return a frequency dict of nucleotide bases in a given sequence
        \n<- bio_seq obj
        \n-> dict
        """
        dna_dict = dict(collections.Counter(self.seq))
        dna_dict.setdefault('A', 0)
        dna_dict.setdefault('T', 0)
        dna_dict.setdefault('G', 0)
        dna_dict.setdefault('C', 0)
        return dna_dict

    def percentGC(self):
        """
        Return GC percentage of a DNA sequence in % form
        \n<- bio_seq obj
        \n-> float
        """
        bases = len(self.seq)
        return float(self.nucFrequencyDict()['G']/bases * 100) + float(self.nucFrequencyDict()['C']/bases * 100)


    def transcribe(self):
        """
        Return the RNA transcription of a given DNA sequence
        \n<- bio_seq obj
        \n-> bio_seq obj RNA
        """
        assert self.seq_type == 'DNA', f"Input seq type is {self.seq_type}, not DNA"
        temp_seq = self.seq
        out_seq = temp_seq.replace('T', 'U')
        return bio_seq(out_seq, 'RNA')


    def dnaCompliment(self):
        """
        Return the matched sequence of a given DNA sequence
        \n<- bio_seq obj
        \n-> bio_seq obj DNA
        """
        assert self.seq_type == 'DNA', f"Input seq type is {self.seq_type}, not DNA"
        translationTable = str.maketrans('ATCG', 'TAGC')
        temp_seq = self.seq
        out_seq = temp_seq.translate(translationTable)
        return bio_seq(out_seq, 'DNA')


    def rnaCompliment(self):
        """
        Return the matched sequence of a given RNA sequence
        \n<- bio_seq obj
        \n-> bio_seq obj RNA
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        translationTable = str.maketrans('AUCG', 'UAGC')
        temp_seq = self.seq
        out_seq = temp_seq.translate(translationTable)
        return bio_seq(out_seq, 'RNA')


    def dna_reverseCompliment(self):
        """
        Return the reverse compliment of a given DNA sequence
        \nNotes: Returns 5' -> 3'
        \n<- bio_seq obj
        \n-> bio_seq obj DNA
        """
        assert self.seq_type == 'DNA', f"Input seq type is {self.seq_type}, not DNA"
        temp_seq = bio_seq(self.seq[::-1], 'DNA')
        return temp_seq.dnaCompliment()



    def rna_reverseCompliment(self):
        """
        Return the reverse compliment of a given RNA sequence
        \nNotes: Returns 5' -> 3'
        \n<- bio_seq obj
        \n-> bio_seq obj RNA
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        temp_seq = bio_seq(self.seq[::-1], 'RNA')
        return temp_seq.rnaCompliment()


    def getBasePairs(self):
        """
        Return the complimentary base pairs of a given DNA sequence
        \n<- bio_seq obj
        \n-> str
        """
        return self.printSeq('f') + '\n   ' + '|'*len(self.seq) + '\n' + self.dnaCompliment().printSeq('r')


    def hammingDist(self, seq2):
        """
        Returns Hamming Distance of 2 given sequences
        \n<- bio_seq obj,\n\tseq2: bio_seq obj
        \n-> int
        """
        seq1Len = len(self.seq)
        seq2Len = len(seq2.seq)
        
        tempseq1 = self.seq
        tempseq2 = seq2.seq

        if seq1Len < seq2Len:
            tempseq1 = self.seq + ('X' * (seq2Len - seq1Len))
        if seq2Len < seq1Len:
            tempseq2 = seq2.seq + ('X' * (seq1Len - seq2Len))
        
        h_dist = 0
        for i in range(len(tempseq1)):
            if tempseq1[i] != tempseq2[i]:
                h_dist += 1
        return h_dist


    def seqCompare(self, seq2):    
        """
        Returns a visual comparison of 2 input sequences
        \n<- seq1: bio_seq obj,\n\tseq2: bio_seq obj
        \n-> str
        """
        seqLen = min(len(self.seq), len(seq2.seq))
        compStr = ''
        for i in range(seqLen):
            if self.seq[i] == seq2.seq[i]:
                compStr += '|'
            else:
                compStr += ' '
        return self.seq + '\n' + compStr + '\n' + seq2.seq


    def translate(self, init_pos = 0):
        """
        Return the list of codons of a given RNA sequence and starting position in sequence
        \n<- bio_seq obj, init_pos: int
        \n-> chr[]
        """
        return [codons[self.seq[pos:pos + 3]] for pos in range(init_pos, len(self.seq) - 2, 3)]


    def seqSummary(self):
        """
        Return summary details of a given DNA sequence.
        \n Notes: seq_name [Optional] is a given name of a sequence for ease of use
        \n Format:
        \n\t Nucleotide Frequency
        \n\t GC Content
        \n\t Forward Strand
        \n\t Compliment
        \n\t Reverse Compliment
        \n\t RNA Transcription
        \n<- bio_seq obj
        \n-> None
        """
        summary = ''
        summary += f'==== Sequence: {self.label} ====\n'
        summary += f'Nucleotide Freq: {self.nucFrequencyDict()}\n'
        summary += f'GC Content: {self.percentGC()}\n'
        summary += f'Base Pairs: \n{self.getBasePairs()}\n'
        summary += f'Reverse Compliment:\n'
        summary += self.dna_reverseCompliment().printSeq('f')
        summary += f'\nTranscribed:\n{self.transcribe().printSeq("f")}'

        return summary
    

    def get_reading_frames(self, start_pos = 0, end_pos = 0):
        """
        Given an RNA seq, return a list of translated codon reading frames
        \n<- bio_seq obj RNA
        \n-> [str[]]
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        frames = []
        temp_seq = bio_seq(self.seq[start_pos:end_pos], 'RNA', self.label+ f': Pos {start_pos} : {end_pos}')
        for i in range(0,3):
            frames.append(temp_seq.translate(i))
        for i in range(0,3):
            frames.append(temp_seq.rna_reverseCompliment().translate(i))
        return frames


    def getAllORFProteins(self, start_pos = 0, end_pos = 0, ordered = False):
        """
        Given an RNA sequence, starting position, and ending position, return all possible polypeptides within the ORFs
        \n<- bio_seq obj start_pos: int, end_pos: int, ordered: bool
        \n-> str[]
        """
        assert self.seq_type == 'RNA', f"Input seq type is {self.seq_type}, not RNA"
        if end_pos > start_pos:
            frames = self.get_reading_frames(start_pos, end_pos)
        else:
            frames = self.get_reading_frames(start_pos, end_pos)
        
        output = []
        for frame in frames:
            proteins = getProteinsFromRF(frame)
            for protein in proteins:
                output.append(protein)
        

        if ordered:
            return sorted(output, key = len, reverse = True)
        return output


# ====== Function Comment Template ======

    """
    Purpose of Function
    \nNotes: [notes]
    \n\t[more notes]    
    \n<- input: type
    \n-> type
    """