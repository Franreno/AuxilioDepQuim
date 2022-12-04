from commands import Funcionalidades


def getInput(startString: str = '>> '):
    return input(startString)


def getAllCommands():
    return Funcionalidades.instances


def commandNames() -> list:
    return list(map(lambda x: x.name, Funcionalidades.instances))


def compareFuncsLengths(og: list, comp: list) -> bool:
    return len(comp) >= len(og)


def compareIfListsAreEqualByOgSize(og: list, comp: list) -> bool:
    """ Compare if two lists are equal with original size

    Args:
        og (list): original list of words
        comp (list): comparable list of words

    Returns:
        bool: true if comp == og, with og size
    """
    return comp[:len(og)] == og


def matchAndRun(funcToSearch: str, *args) -> bool:
    if(funcToSearch.lower() == 'clear'):
        clearScreen()
    if(funcToSearch.lower() == 'exit'):
        exit()


    func: Funcionalidades
    # Searches for `funcToSearch` in all of instances of `Funcionalidades`
    for func in Funcionalidades.instances:

        # List of words inside the `func` name
        funcWords: list = func.name.split()

        funcToSearchWords: list = funcToSearch.split()

        if compareFuncsLengths(funcWords, funcToSearchWords) and compareIfListsAreEqualByOgSize(funcWords, funcToSearchWords):
            func.run(*args, funcToSearch[len(func.name):])
            return True

    return False

def clearScreen():
    from os import system, name
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')