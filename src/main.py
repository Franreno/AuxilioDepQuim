from utils import *


def main():
    clearScreen()
    while True:
        cmd = getInput()
        matchAndRun(cmd)


if __name__ == '__main__':
    main()
