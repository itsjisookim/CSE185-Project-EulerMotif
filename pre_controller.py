import sys 
import os
import argparse
import csv
from Sort_Peaks import *
from better_candies import *
from pathlib import Path

# Author: John Gervasoni

class Formatter(argparse.HelpFormatter):
    # use defined argument order to display usage
    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = 'usage: '

        # if usage is specified, use that
        if usage is not None:
            usage = usage % dict(prog=self._prog)

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = '%(prog)s' % dict(prog=self._prog)
        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)
            # build full usage string
            action_usage = self._format_actions_usage(actions, groups) # NEW
            usage = ' '.join([s for s in [prog, action_usage] if s])
            # omit the long line wrapping code
        # prefix with 'usage:'
        return '%s%s\n\n' % (prefix, usage)

# Values go in order: Genome.Chromosome.Peakfile.StartingLocation
# Order of CSV: Motif - Count - Genome - Chromosome - Peakfile - StartingLocation
def toCSV(Everything):

    with open('Results.csv','w') as csvFile:
        
        for key,value in Everything.items():
            AfterFirstLine = False
            count = str(len(value))
            string = key + '\t' + count + '\t'
            for line in value:
                if AfterFirstLine:
                    string = '\t\t'
                line = line.replace('.','\t')
                string = string + line + '\n'
                csvFile.write(string)


def Controller(c=None):
    
    peak_dir = Path('Peak/')
    peak_files = peak_dir.glob('*.txt')
    peak_dict = {}

    Everything = {}
    for peak in peak_files:
        peak_filename = os.path.basename(peak)
        peak_filename = peak_filename.partition('.')[0]
        print("For " + peak_filename)
        peak_dict = SortPeaks(peak,c)

        source_dir = Path('Fasta/')
        files = source_dir.glob('*.fa')

        dic = {}
        # peak_dict should only have the chromosome we are interested in
        for fasta in files:
            print("Inside fasta")
            temp_Dict = Candies(fasta, peak_filename,  peak_dict)
            Everything.update(temp_Dict)    
        print() 
    toCSV(Everything)

    return Everything


if __name__=='__main__':

    #file1 = sys.argv[1]

    parser = argparse.ArgumentParser(formatter_class=Formatter)
    '''
    parser.add_argument('PeakFile',
                        type=argparse.FileType('r'),
                        help='input file of Peaks'
                        )
    '''
    '''  
    parser.add_argument('-s','--Sort_Peaks',
                        action='store_true',
                        help='Outputs Sorted Peak file',
                        dest='s'
                        )
    '''
    parser.add_argument('-chr','--chromosome',
                        type=str,
                        help='only return motifs of specific chromosome',
                        dest='c'
                        )
   
    args = parser.parse_args()
    GM = Controller(args.c)
