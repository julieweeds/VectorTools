__author__ = 'juliewe'

import sys

def remove_end_tabs(filename):

    with open(filename) as instream:
        with open(filename+'.new','w') as outstream:

            for line in instream:
                fields=line.rstrip().split('\t')
                outstream.write(fields[0])
                for field in fields[1:]:
                    outstream.write('\t'+field)
                outstream.write('\n')
                


if __name__=='__main__':

    filename = sys.argv[2]
    option = sys.argv[1]

    if option == 'remove_end_tabs':
        remove_end_tabs(filename)
