from collections import namedtuple
import globals


def loadgamma():
    loadgammascan(0,117)


def loadgammascan(minA,maxA):
    str1 = './Databases/gammas/levels/z'

    for i in range(minA,maxA):
        A = i+1
        if len(str(A)) == 1:
            decodegammas2(str1+'00'+str(A)+'.dat',A)
        if len(str(A)) == 2:
            decodegammas2(str1 + '0' + str(A) + '.dat',A)
        if len(str(A)) == 3:
            decodegammas2(str1 + str(A) + '.dat',A)

    #print('gammas',globals.Full_Gammas)


def decodegammas(filename, A):
    #not used keep for time being :)
    #print('A=',A)
    #print('filename',filename)
    f = open(filename,'r')

    record = namedtuple('Isotope',
                        'SYMB A Z Nol Nog Nmax Nc Sn Sp')
    columns1 = ((0,5),(6,10),(11,15),(16,20),(21,25),(26,30),(31,35),(36,47),(48,60))

    record2 = namedtuple('Level',
                        'N1 Elv s p T_half Ng J')
    columns2 = ((0,3),(5,14),(16,20),(21,23),(25,33),(34,38),(39,39))

    record3 = namedtuple('Gammas',
                          'Nf Eg Pg Pe ICC')
    columns3 = ((39,43),(45,55),(55,65),(66,76),(77,87))

    while f:
        string = f.readline()
        if string == "":
            break

        dataline = [string[c[0]:c[1]] for c in columns1]

        nucl =record._make([string[c[0]:c[1]] for c in columns1])

        if int(nucl.Nol) >= 1:

            for x in range(int(nucl.Nol)):
                string = f.readline()
                level =record2._make([string[c[0]:c[1]] for c in columns2])

                if int(level.Ng) >= 1:
                    for y in range(int(level.Ng)):
                        string = f.readline()
                        gammas = record3._make([string[c[0]:c[1]] for c in columns3])

                        temp1 = list(globals.Full_Gammas)
                        temp1.append((nucl.SYMB,gammas.Eg,gammas.Pg,level.T_half))
                        globals.Full_Gammas = tuple(temp1)

    f.close()

def decodegammas2(filename, A):
    f = open(filename,'r')
    record = namedtuple('Isotope',
                        'SYMB A Z Nol Nog Nmax Nc Sn Sp')
    columns1 = ((0,5),(6,10),(11,15),(16,20),(21,25),(26,30),(31,35),(36,47),(48,60))

    record2 = namedtuple('Level',
                        'N1 Elv s p T_half Ng J')
    columns2 = ((0,3),(5,14),(16,20),(21,23),(25,33),(34,38),(39,39))

    record3 = namedtuple('Gammas',
                          'Nf Eg Pg Pe ICC')
    columns3 = ((39,43),(45,55),(55,65),(66,76),(77,87))

    while f:
        string = f.readline()
        if string == "":
            break

        dataline = [string[c[0]:c[1]] for c in columns1]

        nucl =record._make([string[c[0]:c[1]] for c in columns1])

        if int(nucl.Nol) >= 1:

            for x in range(int(nucl.Nol)):
                string = f.readline()
                level =record2._make([string[c[0]:c[1]] for c in columns2])

                if int(level.Ng) >= 1:
                    for y in range(int(level.Ng)):
                        string = f.readline()
                        gammas = record3._make([string[c[0]:c[1]] for c in columns3])

                        globals.Full_Gammas[A].append((nucl.SYMB, gammas.Eg, gammas.Pg, level.T_half))

    f.close()
