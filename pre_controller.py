import sys 
import os
import argparse
from Sort_Peaks import *

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

def Controller(Peakfile, s=False, c=None):
    
    peak_dict = SortPeaks(Peakfile, s, c)

    

    return peak_dict


if __name__=='__main__':

    file1 = sys.argv[1]

    parser = argparse.ArgumentParser(formatter_class=Formatter)

    parser.add_argument('PeakFile',
                        type=argparse.FileType('r'),
                        help='input file of Peaks'
                        )
    
    parser.add_argument('-s','--Sort_Peaks',
                        action='store_true',
                        help='Outputs Sorted Peak file',
                        dest='s'
                        )
    parser.add_argument('-chr','--chromosome',
                        type=str,
                        help='only return motifs of specific chromosome',
                        dest='c'
                        )
   
    args = parser.parse_args()
    print(args.s)
    GM = Controller(args.PeakFile, args.s, args.c)

