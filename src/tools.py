__author__ = 'juliewe'

import sys
from featuretotals import Totals

def remove_end_tabs(filename):

    with open(filename) as instream:
        with open(filename+'.new','w') as outstream:

            for line in instream:
                fields=line.rstrip().split('\t')
                outstream.write(fields[0])
                for field in fields[1:]:
                    outstream.write('\t'+field)
                outstream.write('\n')


def make_ppmi(filename):
    #convert vector file from frequencies into PPMI
    mytotals=Totals()
    mytotals.readfile(filename)

if __name__=='__main__':

    filename = sys.argv[2]
    option = sys.argv[1]

    if option == 'remove_end_tabs':
        remove_end_tabs(filename)

    elif option == 'make_ppmi':
        make_ppmi(filename)
