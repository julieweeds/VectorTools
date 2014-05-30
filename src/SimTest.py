__author__ = 'juliewe'
import ConfigParser, sys, os,datetime,time

class Vector:

    def __init__(self,name):
        self.name=name
        self.features={}
        self.total=0


    def addfeatures(self,fields):

        while(len(fields)>0):
            sc=float(fields.pop())
            feat=fields.pop()
            current=self.features.get(feat,0)
            if current>0:
                print "Warning: adding repeated values for "+feat+" : "+str(current)+" : "+str(sc)
            self.features[feat]=current+sc
            self.total+=sc

class simEngine:
    def __init__(self,configfile):
        self.parameters = ConfigParser.RawConfigParser()
        self.parameters.read(configfile)
        self.datadir=self.parameters.get('A','datadir')
        self.prefix=self.parameters.get('A','prefix')
        self.featuredict={}
        self.vectordict={}
        self.grandtotal=0


    def readfeaturefile(self):
        featurefile= os.path.join(self.datadir,self.prefix+self.parameters.get('A','featurefile'))
        print "Reading ",featurefile
        read=0
        with open(featurefile) as instream:
            for line in instream:
                parts=line.rstrip().split('\t')
                if len(parts)==2:
                    self.featuredict[parts[0]]=float(parts[1])
                    self.grandtotal+=parts[1]
                else:
                    print "Ignoring line "+line
                read+=1
                if read%10000==0:
                    print "Read "+str(read)+" lines"

        print "Grandtotal for features is "+str(self.grandtotal)
        return

    def readvectors(self):
        which = self.parameters.get('A','which')
        if which == 'n':
            self.readnvectors()
        else:
            print "Aborting: method not defined for which = "+which
            exit()

        return

    def readnvectors(self):

        vectorfile=os.path.join(self.datadir,self.prefix+self.parameters.get('A','eventfile'))
        n=int(self.parameters.get('A','n'))
        print "Reading ",vectorfile
        read=0
        with open(vectorfile) as instream:
            for line in instream:
                fields=line.rstrip().split('\t')
                self.vectordict[fields[0]]=Vector(fields[0])
                self.vectordict[fields[0]].addfeatures(fields[1:])
                read+=1
                if read>=n:break
            print "Read first "+str(n)+" vectors"


    def allpairssims(self):

        return

    def knn(self):

        return

    def run(self):

        self.readfeaturefile()
        self.readvectors()
        self.allpairssims()
        self.knn()


if __name__=='__main__':
    configfile=sys.argv[1]
    myEngine=simEngine(configfile)
    myEngine.run()
