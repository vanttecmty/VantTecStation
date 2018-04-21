'''Modulo de pruebas de subprocesos para llamar a la red neuronal'''
from subprocess import Popen, PIPE, STDOUT
import sys

def main():
    child = Popen(
        ['C:\\Users\\Julio\\Documents\\a.exe'],
        stdin=PIPE,
        stdout=PIPE,
        bufsize=1,
        universal_newlines=True)

    commandlist = ['Luke', 'Mike', 'Jonathan', 'Exit']
    for command in commandlist:
        print('From PIPE: Q:', child.stdout.readline())
        print(command, file=child.stdin)
        #### child.stdin.flush()
        if command != 'Exit':
            print('From PIPE: A:', child.stdout.readline())
    child.stdin.close()  # no more input
    assert not child.stdout.read()  # should be empty
    child.stdout.close()
    child.wait()

main()
