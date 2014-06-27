__author__ = 'juliewe'
import ConfigParser, sys, os,datetime,time,math

class Vector:

    def __init__(self,name):
        self.name=name
        self.features={}
        self.total=0
        self.transformed=False
        self.pmifeats={}
        self.sims={}

    def addfeatures(self,fields):

        while(len(fields)>0):
            sc=float(fields.pop())
            feat=fields.pop()
            current=self.features.get(feat,0)
            if current>0:
                print "Warning: adding repeated values for "+feat+" : "+str(current)+" : "+str(sc)
            self.features[feat]=current+sc
            self.total+=sc

    def transform_ppmi(self,featuredict,grandtotal):
        self.pmifeats={}

        for feature in self.features.keys():
            myscore=self.features[feature]
            marg=featuredict.get(feature,0)
            num=myscore*grandtotal
            den=self.total*marg
            if den>0:
                ratio=num/den
            else:
                ratio = 1
            logvalue=math.log(ratio)
            if logvalue>0:
                self.pmifeats[feature]=logvalue
            self.transformed=True

    def calcsim(self,aVector,metric='cosine'):

        if metric=='lin':
            return self.calcLin(aVector)
        elif metric=='cosine':
            return self.cosine(aVector)
        else:
            print "Unknown similarity metric", metric
            exit(1)

    def calcLin(self,aVector):

        num=0
        den=0
        for feature in self.pmifeats.keys():
            myscore=self.pmifeats[feature]
            ascore= aVector.pmifeats.get(feature,0)
            if ascore>0:
                num+=ascore+myscore
            den+=myscore
        for feature in aVector.pmifeats.keys():
            den+=aVector.pmifeats[feature]
        if den>0:
            sim=num/den
        else:
            sim=0
        self.sims[aVector.name]=sim
        return sim

    def cosine(self,aVector):
        num=self.dotproduct(aVector)
        prod=self.dotproduct(self)*aVector.dotproduct(aVector)
        if prod>0:
            den=math.pow(prod,0.5)
        else:
            return 0
        if den >0:
            return num/den
        else:
            return 0

    def dotproduct(self,aVector):

        total=0.0
        for feature in self.features.keys():
            ascore=aVector.features.get(feature)
            total+=self.features[feature]*ascore
        return total

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
                    self.grandtotal+=float(parts[1])
                else:
                    print "Ignoring line "+line
                read+=1
                if read%100000==0:
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


    def transformall(self):

        print "Transforming values to PPMI..."
        for vector in self.vectordict.values():

            vector.transform_ppmi(self.featuredict,self.grandtotal)
        print "Finished transforming values to PPMI"

    def allpairssims(self):

        for avector in self.vectordict.values():
            for bvector in self.vectordict.values():
                sim=avector.calcsim(bvector,metric=self.parameters.get('A','metric'))
                print avector.name,bvector.name,str(sim)
        return

    def knn(self):

        return

    def run(self):

        self.readfeaturefile()
        self.readvectors()
        if self.parameters.get('A','input')=='raw' and self.parameters.get('A','metric')=='lin':
            self.transformall()
        self.allpairssims()
        self.knn()


if __name__=='__main__':
    configfile=sys.argv[1]
    myEngine=simEngine(configfile)
    myEngine.run()
