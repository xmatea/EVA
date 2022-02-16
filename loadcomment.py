import globals


def loadcomment(RunNum):
    try:
        commenttext = open(globals.workingdirectory + '/comment.dat', 'r').readlines()
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
        else:
            print('Run Info', search_str, 'Found in Line', index - 1)

            starttime_str = commenttext[index]
            endtime_str = commenttext[index+1]
            events_str = commenttext[index+2]
            comment_str = commenttext[index+4]
            rtn_str = [starttime_str,endtime_str,events_str,comment_str]
    except IOError:
        rtn_str = [" "," "," "," "]
        flag = 0
    return flag,rtn_str
