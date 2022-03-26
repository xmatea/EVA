from collections import namedtuple
import globals
import threading

def loadgamma():
    #loadgammascan(0,118)
    # Create two threads as follows
    print('in load gamma')

    t1=threading.Thread(target=loadgammascan, args=(0, 5,))
    t2=threading.Thread(target=loadgammascan, args=(6, 9,))
    t3=threading.Thread(target=loadgammascan, args=(10, 12,))
    t4=threading.Thread(target=loadgammascan, args=(13, 15,))
    t5=threading.Thread(target=loadgammascan, args=(16, 18,))
    t6=threading.Thread(target=loadgammascan, args=(19, 21,))
    t7=threading.Thread(target=loadgammascan, args=(22, 24,))
    t8=threading.Thread(target=loadgammascan, args=(25, 27,))
    t9=threading.Thread(target=loadgammascan, args=(28, 30,))
    t10=threading.Thread(target=loadgammascan, args=(31, 33,))
    t11=threading.Thread(target=loadgammascan, args=(34, 36,))
    t12=threading.Thread(target=loadgammascan, args=(37, 39,))
    t21=threading.Thread(target=loadgammascan, args=(40, 42,))
    t22=threading.Thread(target=loadgammascan, args=(43, 45,))
    t23=threading.Thread(target=loadgammascan, args=(46, 48,))
    t24=threading.Thread(target=loadgammascan, args=(49, 51,))
    t25=threading.Thread(target=loadgammascan, args=(52, 54,))
    t26=threading.Thread(target=loadgammascan, args=(55, 57,))
    t27=threading.Thread(target=loadgammascan, args=(58, 60,))
    t28=threading.Thread(target=loadgammascan, args=(61, 63,))
    t29=threading.Thread(target=loadgammascan, args=(64, 66,))
    t210=threading.Thread(target=loadgammascan, args=(67, 69,))
    t211=threading.Thread(target=loadgammascan, args=(70, 72,))
    t212=threading.Thread(target=loadgammascan, args=(73, 75,))
    t31=threading.Thread(target=loadgammascan, args=(76, 78,))
    t32=threading.Thread(target=loadgammascan, args=(79, 81,))
    t33=threading.Thread(target=loadgammascan, args=(82, 84,))
    t34=threading.Thread(target=loadgammascan, args=(85, 87,))
    t35=threading.Thread(target=loadgammascan, args=(88, 90,))
    t36=threading.Thread(target=loadgammascan, args=(91, 93,))
    t37=threading.Thread(target=loadgammascan, args=(94, 96,))
    t38=threading.Thread(target=loadgammascan, args=(97, 99,))
    t39=threading.Thread(target=loadgammascan, args=(100, 102,))
    t310=threading.Thread(target=loadgammascan, args=(103, 105,))
    t311=threading.Thread(target=loadgammascan, args=(106, 108,))
    t312=threading.Thread(target=loadgammascan, args=(109, 111,))
    t49=threading.Thread(target=loadgammascan, args=(112, 114,))
    t410=threading.Thread(target=loadgammascan, args=(115, 118,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t21.start()
    t22.start()
    t23.start()
    t24.start()
    t25.start()
    t26.start()
    t27.start()
    t28.start()
    t29.start()
    t210.start()
    t211.start()
    t212.start()
    t31.start()
    t32.start()
    t33.start()
    t34.start()
    t35.start()
    t36.start()
    t37.start()
    t38.start()
    t39.start()
    t310.start()
    t311.start()
    t312.start()
    t49.start()
    t410.start()
    print('setup done')
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()
    t12.join()
    t21.join()
    t22.join()
    t23.join()
    t24.join()
    t25.join()
    t26.join()
    t27.join()
    t28.join()
    t29.join()
    t210.join()
    t211.join()
    t212.join()
    t31.join()
    t32.join()
    t33.join()
    t34.join()
    t35.join()
    t36.join()
    t37.join()
    t38.join()
    t39.join()
    t310.join()
    t311.join()
    t312.join()
    t49.join()
    t410.join()


def loadgammascan(minA,maxA):
    #print('helo')
    str1 = './Databases/gammas/levels/z'

    for i in range(minA,maxA):
        A = i+1
        #print(A, len(str(A)))
        if len(str(A)) == 1:
            decodegammas(str1+'00'+str(A)+'.dat')
        if len(str(A)) == 2:
            decodegammas(str1 + '0' + str(A) + '.dat')
        if len(str(A)) == 3:
            decodegammas(str1 + str(A) + '.dat')

    #print('gammas',globals.Full_Gammas)


def decodegammas(filename):
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
                #print(string)
                level =record2._make([string[c[0]:c[1]] for c in columns2])
                #print(level)
                #print('NG',level.Ng)

                if int(level.Ng) >= 1:
                    for y in range(int(level.Ng)):
                        string = f.readline()
                        gammas = record3._make([string[c[0]:c[1]] for c in columns3])
                        #print(y, nucl.SYMB, level.N1,level.Ng, gammas.Nf, gammas)

                        temp1 = list(globals.Full_Gammas)
                        temp1.append((nucl.SYMB,gammas.Eg,gammas.Pg,level.T_half))
                        globals.Full_Gammas = tuple(temp1)

    #print(globals.Full_Gammas)

    f.close()
