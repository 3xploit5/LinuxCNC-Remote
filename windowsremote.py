# !/usr/bin/python
# python 2.7
import os
import redis
import time
import socket


'''
COMMON FUNCTION
'''


def clear_screen():
    os.system('cls')


def timer():
    return time.asctime(time.localtime(time.time()))


'''
CONFIG
'''
menuLogo = '''
    _________   _______  _________   __________                       __          
    \_   ___ \  \      \ \_   ___ \  \______   \ ____   _____   _____/  |_  ____  
    /    \  \/  /   |   \/    \  \/   |       _// __ \ /     \ /  _ \   __\/ __ \ 
    \     \____/    |    \     \____  |    |   \  ___/|  Y Y  (  <_> )  | \  ___/ 
     \______  /\____|__  /\______  /  |____|_  /\___  >__|_|  /\____/|__|  \___  >
            \/         \/        \/          \/     \/      \/                 \/ 
     '''
prompt = "CNCR3M0T3 ~# "
client = redis.Redis(host="127.0.0.1", port=6379)


'''
MENU CLASSES
'''


class WindowsRemote:
    def __init__(self):
        clear_screen()
        print(menuLogo + '''
        {3}--3 Axes
        {4}--4 Axes
        {5}--5 Axes
        ''')
        choice = input(prompt)
        clear_screen()
        Commander(int(choice))
        if choice == "\r" or choice == "\n" or choice == "" or choice == " " or int(choice) > 5:
            self.__init__()
        else:
            try:
                print(os.system(choice))
            except:
                pass
        self.action_completed()

    def action_completed(self):
        input("Task executed, click return to go back")
        self.__init__()


class Commander:
    def __init__(self, axes):
        clear_screen()
        self.axes = axes
        print(menuLogo + '''
            SELECT A COMMAND
            {1}--machine state
            {2}--home
            {3}--unhome
            {4}--brake
            
            {r}--return/abort
        ''')
        choice = input(prompt)
        if choice == "1":
            self.switch_state()
        elif choice == "2":
            self.home_axis(self.axes)
        elif choice == "3":
            self.un_home_axis(self.axes)
        elif choice == "4":
            self.brake()
        elif choice == "r":
            client.publish("cnc", "abort")
            Commander(self.axes)
        else:
            self.__init__(self.axes)
        self.action_completed()

    def switch_state(self):
        clear_screen()
        print(menuLogo + '''
            input: estop, estopr, ston, stof, 
            ''')
        choice = input(prompt)
        client.publish("cnc", choice)
        self.action_completed()

    def home_axis(self, axes):
        self.axes = axes
        clear_screen()
        print(menuLogo + '''
            input axis
        ''')
        choice = int(input(prompt))
        if choice < self.axes:
            client.publish("cnc", "h" + str(choice))
        elif choice == "r":
            Commander(self.axes)
        else:
            self.__init__(self.axes)
        self.action_completed()

    def un_home_axis(self, axes):
        self.axes = axes
        clear_screen()
        print(menuLogo + '''
            input axis
        ''')
        choice = int(input(prompt))
        clear_screen()
        if choice < self.axes:
            client.publish("cnc", "uh" + str(choice))
        elif choice == "r":
            Commander(self.axes)
        else:
            self.__init__(self.axes)
        self.action_completed()

    def brake(self):
        client.publish("cnc", "brake")
        self.action_completed()

    def action_completed(self):
        input("Action sent, click return to go back")
        Commander(self.axes)

#######


if __name__ == "__main__":
    try:
        WindowsRemote()
    except KeyboardInterrupt:
        print("Exiting...\n")
        time.sleep(0.25)



