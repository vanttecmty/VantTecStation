import pexpect
from pexpect import popen_spawn
import sys

def main():
    child = popen_spawn.PopenSpawn('./a.exe')
    #child.logfile = sys.stdout
    child.expect('Enter name: \n')
    child.sendline('Luke')
    child.expect('Tu nombre es Luke\n')
    child.expect('Enter name: \n')
    child.sendline('Mike')
    child.expect('Tu nombre es Mike\n')
    child.expect('Enter name: \n')
    child.sendline('Jonathan')
    child.expect('Tu nombre es Jonathan\n')
    child.expect('Enter name: \n')
    child.sendline('Exit')

main()