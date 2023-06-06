

import argparse

parser = argparse.ArgumentParser(description = "Align 2 DNA sequences")
    
# Adding optional argument
parser.add_argument('file')

args = parser.parse_args()
inf = open(args.file,'r')
data = inf.readlines()
for d in data:
    print(len(d))
inf.close()