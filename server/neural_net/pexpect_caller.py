import pexpect
from pexpect import popen_spawn
import sys

def main():
    child = popen_spawn.PopenSpawn('./a.out')
    child.expect('Hello .*')
    print(child.after.decode("utf-8"), end='')

main()