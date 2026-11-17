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

    index = pesquisa_binaria(utentes, 0, len(utentes) - 1, num_ut)

    if index is None:
        index = pesquisa_binaria2(utentes, 0, len(utentes) - 1, num_ut)
        utentes = utentes[:index] + [[num_ut, [[vac, data]]]] + utentes[index:]
        print("NOVO UTENTE CRIADO")
        return

    index_vac = pesquisa_binaria(utentes[index][1], 0, len(utentes[index][1]) - 1, vac)

    if index_vac is None:
        index_vac = pesquisa_binaria2(utentes[index][1], 0, len(utentes[index][1]) - 1, vac)
        utentes[index][1] = utentes[index][1][:index_vac] + [[vac, data]] + utentes[index][1][index_vac:]
        print("NOVA VACINA INSERIDA")
        return

    utentes[index][1][index_vac][1] = data
    print("VACINA ATUALIZADA")
    return


def consulta(num_ut):
    index = pesquisa_binaria(utentes, 0, len(utentes) - 1, int(num_ut))

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


def pesquisa_binaria(arr, left, right, sol):
    if right < left:
        return None

    mid = (left + right) // 2

    if arr[mid][0] == sol:
        return mid

    elif arr[mid][0] > sol:
        return pesquisa_binaria(arr, left, mid - 1, sol)

    else:
        return pesquisa_binaria(arr, mid + 1, right, sol)


def pesquisa_binaria2(arr, left, right, sol):
    if right < left:
        return right+1

    else:
        mid = (left + right) // 2

        if arr[mid][0] == sol:
            return mid

        elif arr[mid][0] > sol:
            return pesquisa_binaria2(arr, left, mid - 1, sol)

        else:
            return pesquisa_binaria2(arr, mid + 1, right, sol)


main(comandos)

