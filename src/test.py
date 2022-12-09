import os 
print(os.getcwd())

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

find_all('consultas.sql', os.getcwd())