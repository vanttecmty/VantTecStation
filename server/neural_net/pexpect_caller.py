import pexpect
from pexpect import popen_spawn
from Distances import receive

def call():
    '''Realiza llamadas a codigo de red neuronal en C y pasa datos a codigo path.py'''
    child = popen_spawn.PopenSpawn('./a.out')
    child.expect('Hello .*')
    print(child.after.decode("utf-8"), end='')
    child.expect('.*')
    print(child.after.decode("utf-8"), end='')
    print(receive([1, 2, 3, 4, 5]))

call()