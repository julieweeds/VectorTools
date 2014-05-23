__author__ = 'juliewe'

import re
import math


class Totals:
    entrycount=0
    domainPATT = re.compile('^T:')

    def __init__(self):
        Totals.entrycount+=1
        self.domaincolumn={} #dict to store column totals for window features
        self.domainrow={} #dict to store row totals for window features
        self.dependencycolumn={} #dict to store columns totals for dependency features
        self.dependencyrow={} #dict to store row totals for dependency features
        self.domaincolumnwidth={} #store widths as well as total frequencies
        self.domainrowwidth={}
        self.dependencycolumnwidth={}
        self.dependencyrowwidth={}
        self.dependencytotal=0
        self.domaintotal=0
        self.linecount=0
        self.filereads=0


    def readfile(self,filename):
        self.filename=filename
        outname=filename+"_mi"
        self.outstream = open(outname,"w")
        while(self.filereads<2):
            f = open(filename,'r')
            for line in f:
                self.linecount +=1
                self.process(line.rstrip())
                if((self.linecount % 1000)==0):print "Read line: "+str(self.linecount)
            f.close()
            self.filereads+=1;
            if self.filereads==1:
                self.output() #not necessary but may make it possible to recover crash halfway
        self.outstream.close()

    def process(self,line):

        wordlist = line.split('\t')
        row=wordlist[0]
        printout=row
        index=1
        while(index<len(wordlist)):
            column=wordlist[index]
            freq=int(wordlist[index+1])
            mioutput=self.update(row,column,freq)
            if self.filereads>0:
                printout=printout+'\t'+column+'\t'+str(mioutput)
            index = index+2
        if self.filereads>0:
            printout=printout+"\n"
            self.outstream.write(printout)



    def calcdommi(self,row,column,freq):
        gt = self.domaintotal
        if column in self.domaincolumn:
            coltotal=int(self.domaincolumn[column])
        else:
            print "Error - no domain column total for ", column
            exit(1)
        if row in self.domainrow:
            rowtotal=int(self.domainrow[row])
        else:
            print "Error - no domain row total for ", row
            exit(1)
        #print freq, rowtotal, coltotal, gt
        mi = (freq * gt * 1.0)/(rowtotal * coltotal)
        #print mi
        mi = math.log(mi)
        #print mi
        return mi

    def calcdepmi(self,row,column,freq):
        gt = self.dependencytotal
        if column in self.dependencycolumn:
            coltotal=int(self.dependencycolumn[column])
        else:
            print "Error - no dependency column total for ", column
            exit(1)
        if row in self.dependencyrow:
            rowtotal=int(self.dependencyrow[row])
        else:
            print "Error - no dependency row total for ", row
            exit(1)
        #print freq, rowtotal, coltotal, gt
        mi = (freq * gt * 1.0)/(rowtotal * coltotal)
        #print mi
        mi = math.log(mi)
        #print mi
        return mi

    def update(self,row,column,freq):
        mioutput=0
        matchobj=Totals.domainPATT.match(column)
        if matchobj: #domain/window feature
            if self.filereads>0:    #calc mis on second read of file
                mioutput = self.calcdommi(row,column,freq)
            else:   #calc totals on first read of file
                if column in self.domaincolumn:
                    current = int(self.domaincolumn[column])
                    width = int(self.domaincolumnwidth[column])
                else:
                    current = 0
                    width=0
                self.domaincolumn[column]=current+freq
                self.domaincolumnwidth[column]=width+1
                if row in self.domainrow:
                    current = int(self.domainrow[row])
                    width = int(self.domainrowwidth[row])
                else:
                    current=0
                    width=0
                self.domainrow[row]=current+freq
                self.domaintotal+=freq
                self.domainrowwidth[row]=width+1

        else: #dependency feature
            if self.filereads>0:    #calc mis
                mioutput = self.calcdepmi(row,column,freq)
            else:   #calc totals
                if column in self.dependencycolumn:
                    current = int(self.dependencycolumn[column])
                    width = int(self.dependencycolumnwidth[column])
                else:
                    current = 0
                    width =0
                self.dependencycolumn[column]=current+freq
                self.dependencycolumnwidth[column]=width+1
                if row in self.dependencyrow:
                    current = int(self.dependencyrow[row])
                    width = int(self.dependencyrowwidth[row])
                else:
                    current=0
                    width =0
                self.dependencyrow[row]=current+freq
                self.dependencytotal+=freq
                self.dependencyrowwidth[row]=width+1

        if mioutput < 0:
            mioutput = 0
        return mioutput

    def output(self):
        outname = self.filename+"_depcol"
        outputf = open(outname,'w')
        outputf.write("##Dependency column totals for "+self.filename+"\n")
        outputf.write("#Grandtotal:\t"+str(self.dependencytotal)+"\n")
        for key,value in self.dependencycolumn.iteritems():
            outputf.write(key+"\t"+str(value)+"\t"+str(self.dependencycolumnwidth[key])+"\n")
        outputf.close()

        outname = self.filename+"_domcol"
        outputf = open(outname,'w')
        outputf.write("##Domain column totals for "+self.filename+"\n")
        outputf.write("#Grandtotal:\t"+str(self.domaintotal)+"\n")
        for key,value in self.domaincolumn.iteritems():
            outputf.write(key+"\t"+str(value)+"\t"+str(self.domaincolumnwidth[key])+"\n")
        outputf.close()

        outname = self.filename+"_deprow"
        outputf = open(outname,'w')
        outputf.write("##Dependency row totals for "+self.filename+"\n")
        outputf.write("#Grandtotal:\t"+str(self.dependencytotal)+"\n")
        for key,value in self.dependencyrow.iteritems():
            outputf.write(key+"\t"+str(value)+"\t"+str(self.dependencyrowwidth[key])+"\n")
        outputf.close()

        outname = self.filename+"_domrow"
        outputf = open(outname,'w')
        outputf.write("##Domain row totals for "+self.filename+"\n")
        outputf.write("#Grandtotal:\t"+str(self.domaintotal)+"\n")
        for key,value in self.domainrow.iteritems():
            outputf.write(key+"\t"+str(value)+"\t"+str(self.domainrowwidth[key])+"\n")
        outputf.close()