import os

import globals


def loadcomment(RunNum):
    try:
        fd = open(globals.workingdirectory + '/comment.dat', 'r')
        #commenttext = open(globals.workingdirectory + '/comment.dat', 'r').readlines()
        commenttext = fd.readlines()

        search_str = 'Run ' + str(RunNum)
        flag = 0
        index = 0
        for line in commenttext:
            index += 1
            if search_str in line:
                flag = 1
                break
        if flag == 0:
            print('Run Info', search_str, ' Not found')
            rtn_str = [" ", " ", " ", " "]
        else:
            print('Run Info', search_str, 'Found in Line', index - 1)

            globals.starttime_str = commenttext[index]
            globals.endtime_str = commenttext[index+1]
            globals.events_str = commenttext[index+2]
            globals.comment_str = commenttext[index+4]
            rtn_str = [globals.starttime_str, globals.endtime_str, globals.events_str, globals.comment_str]
            fd.close()
    except IOError:
        rtn_str = [" ", " ", " ", " "]
        flag = 0



    return flag,rtn_str
