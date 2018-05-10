import pexpect
from pexpect import popen_spawn
import sys

def main():
    child = popen_spawn.PopenSpawn('./a.exe')
    # child.logfile = sys.stdout
    child.expect('.*')
    child.sendline('Luke')
    child.expect('.*')
    child.sendline('Mike')
    child.expect('.*')
    child.sendline('Jonathan')
    child.expect('.*')
    child.sendline('Exit')

main()