from sys import stdin, stdout


def readln():
    return stdin.readline().rstrip()


comandos = []
comando = ""
while comando != "FIM":
    comando = readln()
    comandos.append(comando.split())

utentes = []


def main(comandos):
    global utentes
    for i in range(len(comandos)):
        if comandos[i][0] == 'ACRESCENTA':
            acrescenta(comandos[i][1], comandos[i][2], comandos[i][3])

        if comandos[i][0] == 'CONSULTA':
            consulta(comandos[i][1])

        if comandos[i][0] == 'LISTAGEM':
            listagem()

        if comandos[i][0] == 'APAGA':
            utentes = []
            print("LISTAGEM DE NOMES APAGADA")


def acrescenta(num_ut, vac, data):
    num_ut = int(num_ut)

    global utentes

    index = pesquisa_binaria(utentes, num_ut)

    if index is None:
        index = pesquisa_binaria_ordem(utentes, num_ut)
        utentes = utentes[:index] + [[num_ut, [[vac, data]]]] + utentes[index:]
        print("NOVO UTENTE CRIADO")
        return

    index_vac = pesquisa_binaria(utentes[index][1], vac)

    if index_vac is None:
        index_vac = pesquisa_binaria_ordem(utentes[index][1], vac)
        utentes[index][1] = utentes[index][1][:index_vac] + [[vac, data]] + utentes[index][1][index_vac:]
        print("NOVA VACINA INSERIDA")
        return

    # utentes.insert(index, valor) in place

    utentes[index][1][index_vac][1] = data
    print("VACINA ATUALIZADA")
    return


def consulta(num_ut):
    index = pesquisa_binaria(utentes, int(num_ut))

    if index is not None:
        inf = str(utentes[index][0])
        for i in range(len(utentes[index][1])):
            inf += " " + utentes[index][1][i][0] + " " + utentes[index][1][i][1]
        print(inf)
        print("FIM")
        return
    else:
        print("NAO ENCONTRADO")


def listagem():
    for i in range(len(utentes)):

        inf = str(utentes[i][0])
        for j in range(len(utentes[i][1])):
            inf += " " + utentes[i][1][j][0] + " " + utentes[i][1][j][1]
        print(inf)
    print("FIM")


def pesquisa_binaria(arr, sol):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = int((right + left) / 2)
        if sol == arr[mid][0]:
            return mid
        if sol < arr[mid][0]:
            right = mid - 1
        else:
            left = mid + 1
    return None


def pesquisa_binaria_ordem(arr, sol):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = int((right + left) / 2)
        if sol == arr[mid][0]:
            return mid
        if sol < arr[mid][0]:
            right = mid - 1
        else:
            left = mid + 1
    return right + 1


main(comandos)
