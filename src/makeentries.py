__author__ = 'juliewe'

import ConfigParser,sys,os


class vectorReader:

    def __init__(self,parameters):
        #parameters is a ConfigParser
        self.datafile=os.path.join(parameters.get('A','datadir'),parameters.get('A','input'))
        self.separator=parameters.get('A','separator')
        self.outputfile=self.datafile+'.entries.strings'

    def process(self):

        print "Reading",self.datafile
        print "Writing",self.outputfile

        with open(self.datafile) as instream:
            with open(self.outputfile,'w') as outstream:
                for line in instream:
                    fields=line.rstrip().split(self.separator)
                    self.lineprocess(fields,outstream)

    def lineprocess(self,fields,outstream):
        print len(fields),fields
        outstream.write(fields)

class entryMaker(vectorReader):

    def lineprocess(self,fields,outstream):

        entry=fields[0]
        sum=0
        for i in range(2,len(fields),2):
            sum+=float(fields[i])
        print entry,sum
        outstream.write(entry+'\t'+str(sum)+'\n')

if __name__=='__main__':

    #configfile=os.path.join('conf',sys.argv[1])
    configfile=sys.argv[1]
    #print configfile
    parameters=ConfigParser.RawConfigParser()
    parameters.read(configfile)
    #print parameters.get('A','datadir')
    myVP=entryMaker(parameters)
    myVP.process()
