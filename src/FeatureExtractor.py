__author__ = 'juliewe'

import ConfigParser, sys, datetime,time
from conllReader import ConllReader

class FeatureExtractor:

    def __init__(self,configfile):
        self.configfile=configfile
        self.parameters=ConfigParser.RawConfigParser()
        self.parameters.read(configfile)
        self.inputReader=ConllReader(self.parameters)
        self.inputReader.openfile()
        self.outfile=self.inputReader.inputfile+self.parameters.get('A','id')
        self.outstream=open(self.outfile,'w')


    def run(self):
        self.starttime=time.time()
        st=datetime.datetime.fromtimestamp(self.starttime).strftime('%Y-%m-%d %H:%M:%S')
        print "Feature Extraction Starting "+st
        print "Configuration in "+self.configfile
        processed=0
        keepReading=True
        try:
            while keepReading==True:
                self.currentsentence=self.inputReader.readSentence()
                self.extractSentence()
                processed+=1
                if self.parameters.get('A','mode')=='testing' and processed>0:
                    keepReading=False

        except(EOFError):
            print "End of file, processed "+str(processed)+" sentences"

    def extractSentence(self):
        if self.parameters.get('A','features')=='windows':
            self.extractWindowFeatures()

        else:
            print "Other types of features not currently supported"

    def extractWindowFeatures(self):

        self.tokens= [int(tok) for tok in self.parameters.get('A','tokens').split(',')]
        if self.parameters.get('A','labelled')=='on':
            labelled=True
        else:
            labelled=False
            fname='T:'
        self.indexSentence()
        #print self.index
        #features=[]
        for i,instance in enumerate(self.index):  #make list of related tokens based on position
            features=[]
            for j in range(int(self.parameters.get('A','before')),0,-1):
                if labelled:fname='T'+'-'+str(j)+':'
                if i-j>-1:
                    feature=self.makefeature(i-j,fname)
                    features.append(feature)
            for k in range(1,int(self.parameters.get('A','after'))+1):

                if labelled:fname='T'+'+'+str(k)+':'
                if i+k<len(self.index):
                    feature=self.makefeature(i+k,fname)
                    features.append(feature)
            if len(features)>0:
                line=self.index[i][1]
                for feature in features:
                    line+='\t'+feature
                line+='\n'
                self.outstream.write(line)

    def makefeature(self,i,fname):
        feature=fname+self.index[i][1]
        return feature


    def indexSentence(self):
        self.index=[]
        for instance in self.currentsentence:
            fields=instance.split('\t')
            thisindex=int(fields[0])
            parts=[]
            for i in self.tokens:
                parts.append(fields[i-1])
            token = parts[0]
            if len(parts)>1:
                for part in parts[1:]:
                    token+='/'+part
            self.index.append((thisindex,token))
            self.index.sort()

    def shutdown(self):
        self.inputReader.closefile()
        self.outstream.close()
        ts2=time.time()
        st=datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
        print "Feature Extraction Complete "+st
        timetaken=int(ts2-self.starttime)
        hours = timetaken/3600
        mins = (timetaken%3600)/60
        secs = (timetaken%3600)%3600
        print "Time taken: "+str(hours)+" hrs, "+str(mins)+" mins, "+str(secs)+" secs"

    def test(self):
        self.run()
        print "Test Complete"

if __name__=='__main__':

    myFeatureExtractor=FeatureExtractor(sys.argv[1])
    myFeatureExtractor.run()
    myFeatureExtractor.shutdown()
