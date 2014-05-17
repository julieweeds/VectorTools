__author__ = 'juliewe'

import ConfigParser,sys,os



class ConllReader:

    def __init__(self,parameters):
        self.parameters=parameters
        self.inputfile=os.path.join(self.parameters.get('A','datadir'),self.parameters.get('A','input'))
        self.EOF=False

    def openfile(self,inputfile=''):
        if inputfile!='':
            self.inputfile=inputfile
        self.instream=open(self.inputfile,'r')

    def closefile(self):
        self.instream.close()

    def readSentence(self):

        if self.EOF==True:
            raise EOFError
        else:
            lines=[]
            keepReading=True
            while keepReading==True:
                thisLine=self.instream.readline()
                if thisLine=='\n':
                    keepReading=False
                elif thisLine=='':
                    #end of file reached
                    self.EOF=True
                    keepReading=False
                else:
                    lines.append(thisLine)
            self.currentsentence=lines
            return lines

    def test(self):

        self.openfile()
        print self.readSentence()
        self.closefile()
        print "Completed Test 1"

        self.openfile()
        read=0
        try:
            while True:
                self.readSentence()
                read+=1
                print "Read "+str(read)+" sentences"
        except(EOFError):
            print "End of file reached: "+str(read)+ " sentences"
if __name__=='__main__':

    configfile=sys.argv[1]
    parameters=ConfigParser.RawConfigParser()
    parameters.read(configfile)
    myConllReader=ConllReader(parameters)
    myConllReader.test()