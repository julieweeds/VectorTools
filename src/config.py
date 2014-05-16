__author__ = 'juliewe'

import ConfigParser,sys

def make_config():

    conf = ConfigParser.RawConfigParser()

    conf.add_section('A')
    conf.set('A','input','test.txt')
    conf.set('A','datadir','data/')
    conf.set('A','k',5)

    with open('conf/example.cfg','wb') as configfile:
        conf.write(configfile)

def read_config():

    conf = ConfigParser.RawConfigParser()

    conf.read('conf/example.cfg')

    input=conf.get('A','input')
    datadir=conf.get('A','datadir')
    k=conf.get('A','k')

    print datadir,input,k


if __name__=='__main__':

    for arg in sys.argv:
        if arg=='make':
            make_config()
        elif arg=='read':
            read_config()

