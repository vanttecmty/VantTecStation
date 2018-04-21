def main():
    while True:
        print('name => Q: what is your name?')
        name = input()
        if name == 'Exit':
            break
        print('name => A: your name is ' + name)

main()
