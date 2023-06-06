#BIMM 182 : Assignment 2 Q2
#Jisoo Kim
#A15638045

import argparse
from matplotlib import pyplot as plt
import numpy as np

def find_median(array):
    size = len(array)
    middle = int(size / 2)
    if size % 2 == 0:
        return (array[middle - 1] + array[middle]) / 2.0
    else:
        return array[middle]

def GenerateHist(inputfile):
    ID = inputfile.split('.')[0]
    inf = open(inputfile)
    data= inf.readlines()
    
    align_lengths = []
    for d in data:
        if 'Length' in d:
            align_lengths.append(int(d.split()[-1]))
    inf.close()

    print(find_median(align_lengths))

    aligned  = np.array(align_lengths)
    plt.hist(aligned, bins=20)
    plt.xlabel('Length')
    plt.ylabel('Frequency')
    plt.title('Alignment Legnth of %s parameters'%ID)
    plt.savefig('%s_hist.png'%ID)


def PromptMessage():
    # Initialize parser
    parser = argparse.ArgumentParser(description = "Generate Histogram of given alignment length data")
    # Adding optional argument
    parser.add_argument('file', help='File containing alignment lengths')
    
    # Read arguments from command line
    args = parser.parse_args()

    GenerateHist(args.file)
    

#### Execution
PromptMessage()