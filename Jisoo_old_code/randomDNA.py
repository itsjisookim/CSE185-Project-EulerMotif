#BIMM 182 : Assignment 2 Q2
#Jisoo Kim
#A15638045

### Obejective
# Input:
#       Number      Number of Sequence (e.g. 500)
#       Length      Length of Sequence (e.g. 1000)
# Output:
#       p2seq.txt containing random sequences generagted with given parameters 

import argparse
from random import choice

def GenerateSeq(number, length):
    nuc_ct ={'A':0,'C':0, 'T':0,'G':0}
    for i in range(1,number+1):
        print(">Q2seq%s\n"%(i))
        rand_str = ''.join(choice("ATCG") for i in range(length))
        for n in nuc_ct:
            ct = rand_str.count(n)
            nuc_ct[n]+=ct
        print("%s\n"%rand_str)
        rand_str = ''.join(choice("ATCG") for i in range(length))
        for n in nuc_ct:
            ct = rand_str.count(n)
            nuc_ct[n]+=ct
        print("%s\n"%rand_str)
        print("\n")

    for n in nuc_ct:
        print("%s %.3f"%(n, float(nuc_ct[n])/(2*length*number)))


def PromptMessage():
    # Initialize parser
    parser = argparse.ArgumentParser(description = "Generate random DNA sequences with the given number and length of the sequences and they nucleotide composition summary")
    
    # Adding optional argument
    parser.add_argument('Number', help='Number of Sequence (e.g. 500)' ,type=int)
    parser.add_argument('Length', help='Length of Sequence (e.g. 1000)', type=int)
    
    # Read arguments from command line
    args = parser.parse_args()

    GenerateSeq(args.Number, args.Length)
    

#### Execution
PromptMessage()