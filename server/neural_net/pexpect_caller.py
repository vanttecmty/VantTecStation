import pexpect
from pexpect import popen_spawn

def main():
    child = popen_spawn.PopenSpawn('a.exe')
    child.expect('Enter name: \n')
    child.sendline('Luke')
    child.expect('Tu nombre es Luke')
    child.expect('Enter name: ')
    child.sendline('Mike')
    child.expect('Tu nombre es Mike')
    child.expect('Enter name: ')
    child.sendline('Jonathan')
    child.expect('Tu nombre es Jonathan')
    child.expect('Enter name: ')
    child.sendline('Exit')

main()