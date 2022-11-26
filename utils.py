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
    print("Entrei")
    func: Funcionalidades
    # Searches for `funcToSearch` in all of instances of `Funcionalidades`
    for func in Funcionalidades.instances:

        print(f"Procudando... {func}")
        # List of words inside the `func` name
        funcWords: list = func.name.split()

        funcToSearchWords: list = funcToSearch.split()

        if compareFuncsLengths(funcWords, funcToSearchWords) and funcToSearchWords[:len(funcWords)] == funcWords:
            print("Vou rodar")
            func.run(*args, funcToSearch[len(func.name):])
            return True

    return False
