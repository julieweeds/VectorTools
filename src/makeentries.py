__author__ = 'juliewe'

import ConfigParser,sys,os,csv


class vectorReader:

    def __init__(self,parameters):
        #parameters is a ConfigParser
        self.datafile=os.path.join(parameters.get('A','datadir'),parameters.get('A','input'))
        self.separator=parameters.get('A','separator')
        self.outputfile=self.datafile+'.entries.strings'
        if self.separator=='tab':
            self.separator='\t'
        print 'Delimiter: ',self.separator


    def process(self):

        print "Reading",self.datafile
        print "Writing",self.outputfile

        csvreader=csv.reader(open(self.datafile,'r'),delimiter=self.separator)
        with open(self.outputfile,'w') as outstream:
            for row in csvreader:
                #fields=line.rsplit().split(self.separator)
                #print row
                self.lineprocess(row,outstream)

    def lineprocess(self,fields,outstream):
        print len(fields),fields
        outstream.write(fields[0])
        for field in fields[1:]:
            outstream.write('\t'+field)
        outstream.write('\n')

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

    #myVP=vectorReader(parameters)
    myVP.process()