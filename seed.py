import os
import linuxcnc
import redis
import time

def clear_screen():
    os.system('clear')

'''
CONFIG
'''
menuLogo = '''
      _______________________________________   
     /   _____/\_   _____/\_   _____/\______ \  
     \_____  \  |    __)_  |    __)_  |    |  \ 
     /        \ |        \ |        \ |    `   \
    /_______  //_______  //_______  //_______  /
            \/         \/         \/         \/
'''
c = linuxcnc.command()
s = linuxcnc.stat()
client = redis.Redis(host="10.0.0.1", port=6379)
# test = redis.from_url(redis://[[username]:[password]]@localhost:6379/0)
p = client.pubsub()
p.subscribe("cnc")


class Listener:
    def __init__(self):
        clear_screen()
        print menuLogo
        print "listening..."
        for item in p.listen():
            item = item['data']
            # mark = item[0]
            #data = item[1:]
            if item == "h0":
                c.home(0)
                print "Homing Axis "
            elif item == "h1":
                c.home(1)
                print "Homing Axis "
            if item == "h2":
                c.home(2)
                print "Homing Axis "
            elif item == "abort":
                c.abort()
                print "aborting"
            elif item == "":
                pass
            else:
                self.__init__()

'''
LINUXCNC FUNCTIONS
'''
def ok_for_mdi():
    try:
        s.poll()
        return not s.estop and s.enabled and s.homed and (s.interp_state == linuxcnc.INTERP_IDLE)
    except:
        error()
        print "MDI check failed"

def error():
    error = e.poll()
    if error:
        kind, text = error
        if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
            typus = "error"
        else:
            typus = "info"
        print typus, text

def homed(axes):
    try:
        s.poll()
        h = s.homed
        for i in range(0, axes):
            ax = "Axes " + str(i)
            if h[i] == 0:
                print ax + " not homed"
                return 0
            else:
                print ax + " homed"
        return 1
    except:
        error()
        print "homed failed"

def axis(axes):
    try:
        for i in range(axes):
            a = s.axis[i]
            name = str(i) + '_axis'
            client.hmset(name, a)
            print a
    except:
        error()
        print "axis failed"


if __name__ == "__main__":
    try:
        Listener()
    except KeyboardInterrupt:
        print("Exiting...\n")
        time.sleep(0.25)
