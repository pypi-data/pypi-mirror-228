from msvcrt import getwch
from os import read
from runpy import run_path
from sys import argv 
from multiprocessing import Process
from colorama import Fore as CLR

OK = True
RUNNING = None
INPUT = None
FILE = None

def Reload():
    global RUNNING
    RUNNING.terminate()
    try:
                RUNNING = Process(target=run_path,args=(FILE,))
                RUNNING.start()
    except Exception as e:
        print(e)
        exit()

def help():
    print("""{}
########################################
#        {}WELCOME TO PY_RELOADER{}        #
#                                      #
#  {}-ENTER A FILE AND RUN{}               #
#  {}-FOR RE-RUN ONLY PRESS R{}            #
#  {}-FOR EXIT PRESS Q  {}                 #
#                                      #
##############{}  BUT  WHY  {}##############
#      {}Beacuse very easy and fast{}      #
#       {}Debugging and developing{}       #
#                                      #
########################################{}
""".format(CLR.CYAN,CLR.YELLOW,CLR.CYAN,CLR.BLUE,CLR.CYAN,CLR.BLUE,CLR.CYAN,CLR.BLUE,CLR.CYAN,CLR.GREEN,CLR.CYAN,CLR.GREEN,CLR.CYAN,CLR.GREEN,CLR.CYAN,CLR.RESET))

         

def finish():
     global RUNNING,OK
     RUNNING.terminate()
     OK = False

options = {
    "q" : finish,
    "r" :  Reload,
}


if __name__ == "__main__":
    argv = argv[1:]
    print("{}PY_RELOADER BY CODE_BREAKER{}".format(CLR.CYAN,CLR.YELLOW))
    if argv.__sizeof__() > 1 or argv.__sizeof__() < 1:
         print("please enter AN ARGUMENT")
    for arg in argv:
        if arg == "help" or arg == "-h":
            help()
            exit()
        else:
            RUNNING = Process(target=run_path,args=(arg,))
            RUNNING.start()
            print(CLR.RED)
        
            FILE = arg
            while OK:
                INPUT = getwch().lower()
                try:
                    options[INPUT]()
                except:
                     pass
    print("{}THANKS FOR USING{}".format(CLR.CYAN,CLR.RESET))
    