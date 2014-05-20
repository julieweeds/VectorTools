__author__ = 'juliewe'

if __name__=='__main__':

    filename='/Volumes/LocalScratchHD/juliewe/Documents/workspace/Compounds/data/WNCompounds/teststuff/oneline'
    instream = open(filename)
    lines=[]
    for line in instream:
        lines.append(line.rstrip())

    fields=lines[0].split('\t')
    print len(fields)
    entry =fields[0]
    print entry
    sum=0
    for i in range(1,len(fields),2):
        try:
            feat = fields[i]
            score = float(fields[i+1])
            sum+=score
        except(IndexError):
            print i, feat

    print sum
