def load_srn_settings():
    with open('Screen_issues.txt') as f:
        lines = f.readlines()
        print('screen_issues')
        print(lines)
        settings_info=lines
    #return (int(lines))