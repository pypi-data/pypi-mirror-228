# Computational Biology Python Tools
# Last updated: 8/15/23
#
#
# Packages included in this file:
#   - dnaToolkit.py
#
# https://www.stephendoescomp.bio
# Stephen Cheney © 2023

from bio_seq import *
from aa_seq import *
from fasta_tk import *


class main:
   dna = bio_seq("ACGTTTA")
   dna2 = bio_seq("ACGGGTA")
   print(dna.seqSummary())
main()