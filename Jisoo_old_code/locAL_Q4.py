#BIMM 182 : Assignment 2 Q4
#Jisoo Kim
#A15638045

### Obejective
# Input:
#       1. Sequence file with 2 long DNA sequences
#       2. match score
#       3. mismatch score
#       4. indel score
# Output:
#       1. Score of the best local-alignment
#       2. Length of the best local-alignment
#       [optional] when -a, return alignment with Blast format

import argparse
from datetime import datetime
import tracemalloc

def readSeq(inputfile):
    sequences = {}
    inf = open(inputfile, 'r')
    data = inf.readlines()
    
    ID = ""
    for d in data:
        line = d.strip()
        if '>' in line:
            ID = line.strip('>')
        else:
            if len(line) != 0 :
                sequences[ID] = line
    inf.close()

    return sequences

def LocalAlignment(n1, n2, sequences, match, mismatch, IND):
    seq = sequences.values()

    s = [[0 for i in range(0, len(n2)+1)]
        for j in range(0, len(n1)+1)]

    opt_score = 0
    opt_loc = (0,0)
    for i in range(1, len(n1)+1):
        for j in range(1, len(n2)+1):
            score = 0
            if n1[i-1] == n2[j-1]:
                score = match
            else:
                score = mismatch

            s[i][j] = max(0, s[i-1][j] + IND, s[i][j-1] + IND, s[i-1][j-1] + score)
            if s[i][j] >= opt_score:
                opt_score = s[i][j]
                opt_loc = (i,j)

    print("start coordinate ")
    print(opt_loc)
    score = opt_score
    tracker = opt_loc
    aligned ={}
    IDs = [list(sequences.keys())[list(seq).index(n)] for n in seq]
    #print(IDs[1])
    for ID in sequences:
        aligned[ID] = ""
    
    #print(n2)
    while  score != 0:
        i = tracker[0]
        j = tracker[1]
        if s[i][j] == (s[i-1][j]+IND): #"down : insertion so need space n2"
            aligned[IDs[0]] = n1[i-1] + aligned[IDs[0]]
            aligned[IDs[1]] = '-' + aligned[IDs[1]]
            tracker = (i-1, j)
            score = s[i-1][j]
        elif s[i][j] == (s[i][j-1]+IND): #"right :deletion so need space in n1"
            aligned[IDs[0]] = '-' + aligned[IDs[0]]
            aligned[IDs[1]] = n2[j-1] + aligned[IDs[1]]
            tracker = (i, j-1)
            score = s[i][j-1]
        elif (s[i][j] == (s[i-1][j-1] + match)) or (s[i][j] == (s[i-1][j-1] + mismatch)): #"diagonal/match"
            aligned[IDs[0]] = n1[i-1] + aligned[IDs[0]]
            aligned[IDs[1]] = n2[j-1]+ aligned[IDs[1]]
            tracker = (i-1, j-1)
            score = s[i-1][j-1]
    print("end coordinate :")
    print(tracker)
    print("Alignment Score : %s"%opt_score)
    print("Alignment Length : %s"%len(aligned[IDs[0]]))
    return aligned, i-1, j-1

def PromptMessage():
    # Initialize parser
    parser = argparse.ArgumentParser(description = "Align 2 DNA sequences")
    
    # Adding optional argument
    parser.add_argument('file')
    parser.add_argument("-m", "--Match", help = "[required] Match score", type=int, required=True)
    parser.add_argument("-s", "--Mismatch", help = "[required] Mismatch score", type=int, required=True)
    parser.add_argument("-d", "--Indel", help = "[required] Indel score", type=float, required=True)
    parser.add_argument("-a", "--Alignment", help = "[optional] Print aligned sequences", action='store_true')
    
    # Read arguments from command line
    args = parser.parse_args()
    
    sequences = readSeq(args.file)
    seq = list(sequences.values())
    #print(sequences)
    for n in range(len(seq)-1):
        n1 = seq[n]
        n2 = seq[n+1]

        #if args.Output:
        #    print("Displaying Output as: % s" % args.Output)
        aligned, n1_idx, n2_idx = LocalAlignment(n1, n2, sequences, args.Match, args.Mismatch, args.Indel)

        # When -a was passed in the command line
        if (args.Alignment == True):
            print("Alignment : ")
            seq = aligned.keys()
            pos = 0
            while pos != len(aligned[seq[0]]):
                add = 0
                if pos+60 <= len(aligned[seq[0]]): 
                    add = 60
                else:
                    add = len(aligned[seq[0]])-pos
                            
                print("%s\t%s\t%s\t%s"%(seq[0], n1_idx, aligned[seq[0]][pos:pos+add], n1_idx+add-aligned[seq[0]][pos:pos+add].count('-')))
                connect = ''
                for i in range(pos, pos+add):
                    if (aligned[seq[0]][i] == '-') or (aligned[seq[1]][i] == '-'):
                        connect += ' '
                    else:
                        connect += '|'
                print("%s\t%s\t%s\t%s"%('', '', connect, ''))
                print("%s\t%s\t%s\t%s"%(seq[1], n2_idx, aligned[seq[1]][pos:pos+add], n2_idx+add-aligned[seq[1]][pos:pos+add].count('-')))
                
                n1_idx = n1_idx+add-aligned[seq[0]][pos:pos+add].count('-')-1
                n2_idx = n2_idx+add-aligned[seq[1]][pos:pos+add].count('-')-1
                pos = pos+add
        n+=2

#### Execution
start = datetime.now()
tracemalloc.start()
PromptMessage()
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
print(datetime.now()-start)