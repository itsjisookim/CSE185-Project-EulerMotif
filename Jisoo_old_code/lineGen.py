#BIMM 182 : Assignment 2 Q2
#Jisoo Kim
#A15638045

import argparse
from matplotlib import pyplot as plt


def GenerateLine(inputfiles):
    IDs = []
    mean_vals = []
    for file in inputfiles:
        ID = file.split('.')[1]
        print(ID)
        mismatch = '-' + (ID.split('_')[0])
        if len(ID.split('_')) > 2:
            ind = '-' + '.'.join(ID.split('_')[1:])
        else :
            ind = '-' + ID.split('_')[1]
        IDs.append(float(ind))
        inf = open(file)
        data= inf.readlines()
        
        align_lengths = []
        for d in data:
            if 'Length' in d:
                align_lengths.append(int(d.split()[-1]))
        inf.close()

        mean = sum(align_lengths)/len(align_lengths)
        mean_vals.append(mean)
    print(IDs)
    print(mean_vals)
    plt.plot(IDs,mean_vals, marker='.', linestyle='solid',  mfc='none', markersize=24, markerfacecolor='white')
    plt.xlabel('Indel score')
    plt.ylabel('Mean Alignment Length')
    plt.title('Alignment Legnth of varying Indel Scores with mismatch score of %s'%mismatch)
    plt.savefig('Indel_line_%s.png'%(mismatch.strip('-')))


def PromptMessage():
    # Initialize parser
    parser = argparse.ArgumentParser(description = "Generate Histogram of given alignment length data")
    # Adding optional argument
    parser.add_argument('file', nargs= '+', help='File containing alignment lengths')
    
    # Read arguments from command line
    args = parser.parse_args()
    print(args)
    GenerateLine(args.file)
    

#### Execution
PromptMessage()