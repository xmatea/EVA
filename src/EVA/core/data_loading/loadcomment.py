
# shows RunNum is integer and the output is int and a string (python typing)
def loadcomment(RunNum: int, file_path: str) -> tuple[list[str], int]:
    '''
    This routine load the comments from comment.dat
    needs input the run number (integer)
    returns success flag and the string
    '''

    try:
        fd = open(file_path + '/comment.dat', 'r')
        #commenttext = open(globals.workingdirectory + '/comment.dat', 'r').readlines()
        commenttext = fd.readlines()

        search_str = 'Run ' + str(RunNum)
        flag = 1
        index = 0
        for line in commenttext:
            index += 1
            if search_str in line:
                flag = 0
                break
        if flag == 1:
            print('Run Info', search_str, ' Not found')
            rtn_str = [" ", " ", " ", " "]
        else:
            print('Run Info', search_str, 'Found in Line', index - 1)

            starttime_str = commenttext[index]
            endtime_str = commenttext[index + 1]
            events_str = commenttext[index + 2]
            comment_str = commenttext[index + 4]
            rtn_str = [starttime_str, endtime_str, events_str, comment_str]
            fd.close()
    except IOError:
        rtn_str = [" ", " ", " ", " "]
        flag = 1

    return rtn_str, flag

