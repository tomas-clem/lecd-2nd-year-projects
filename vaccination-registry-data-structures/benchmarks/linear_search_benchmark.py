from sys import stdin, stdout
import time
import random


def readln():
    return stdin.readline().rstrip()


#comandos = []
#comando = "a"
#while comando != "FIM":
#    comando = readln()
#    comandos.append(comando.split())

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
    index = -1
    global utentes
    for i in range(len(utentes)):
        if num_ut == utentes[i][0]:
            index = i

    if index == -1:
        for j in range(len(utentes)):
            if utentes[j][0] > num_ut:
                utentes = utentes[:j] + [[num_ut, [[vac, data]]]] + utentes[j:]
                print("NOVO UTENTE CRIADO")
                return
        utentes.append([num_ut, [[vac, data]]])
        print("NOVO UTENTE CRIADO")
        return

    for j in range(len(utentes[index][1])):
        if vac in utentes[index][1][j][0]:
            utentes[index][1][j][1] = data
            print("VACINA ATUALIZADA")
            return
    for j in range(len(utentes[index][1])):
        if utentes[index][1][j][0] > vac:
            utentes[index][1] = utentes[index][1][:j] + [[vac, data]] + utentes[index][1][j:]
            print("NOVA VACINA INSERIDA")
            return
    utentes[index][1].append([vac, data])
    print("NOVA VACINA INSERIDA")


def consulta(num_ut):
    index = -1

    for i in range(len(utentes)):
        if num_ut == utentes[i][0]:
            index = i

    if index == -1:
        print("NAO ENCONTRADO")
        return

    inf = str(utentes[index][0])
    for i in range(len(utentes[index][1])):
        for j in range(2):
            inf += " " + utentes[index][1][i][j]

    print(inf)
    print("FIM")


def listagem():
    for i in range(len(utentes)):

        inf = str(utentes[i][0])
        for j in range(len(utentes[i][1])):
            inf += " " + utentes[i][1][j][0] + " " + utentes[i][1][j][1]
        print(inf)
    print("FIM")

vacinas = ["photograph","profession","functional","acceptable","plagiarize","overcharge","relinquish","democratic","vegetarian","commitment"]

#main(comandos)
def cenario_1(n, iter, pesq):
    t1 = time.time()
    for i in range(int(n * iter)):
        acrescenta(random.randint(1, 20000), random.choice(vacinas), str(random.randint(1, 10000000)))

    for i in range(int(n * pesq)):
        consulta(random.randint(1, 20000))
    return time.time()-t1
c1 = [cenario_1(20000,0.1,0.9),cenario_1(40000,0.1,0.9),cenario_1(60000,0.1,0.9),cenario_1(80000,0.1,0.9),cenario_1(100000,0.1,0.9)]
c2 = [cenario_1(20000,0.9,0.1),cenario_1(40000,0.9,0.1),cenario_1(60000,0.9,0.1),cenario_1(80000,0.9,0.1),cenario_1(100000,0.9,0.1)]

print(c1)
print(c2)


