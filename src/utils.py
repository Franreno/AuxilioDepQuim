from commands import Funcionalidades

def compareFuncsLengths(og: list, comp: list) -> bool:
    """Compara se as duas listas possuem o tamanho de acordo com o teste

    Args:
        og (list): original list of words
        comp (list): comparable list of words

    Returns:
        bool: true if len(comp) >= len(og)
    """
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


def matchAndRun(funcToSearch: str, *args) -> str:
    """Pesquisa a funcao dentre as funcionalidades e roda a correta

    Args:
        funcToSearch (str): Funcao a ser rodada

    Returns:
        str: resultado da funcao
    """
    func: Funcionalidades
    # Searches for `funcToSearch` in all of instances of `Funcionalidades`
    
    for func in Funcionalidades.instances:
        # List of words inside the `func` name
        funcWords: list = func.name.split()
        funcToSearchWords: list = funcToSearch.split()
        if compareFuncsLengths(funcWords, funcToSearchWords) and compareIfListsAreEqualByOgSize(funcWords, funcToSearchWords):
            return func.run(*args, funcToSearch[len(func.name):])
