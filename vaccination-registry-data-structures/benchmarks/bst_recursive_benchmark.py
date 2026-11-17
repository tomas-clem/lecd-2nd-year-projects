import time
import random


class Utente:
    def __init__(self, key, vacina, data):
        self.value = key
        self.left = None
        self.right = None
        self.vacina = Vacina(vacina, data)

    def adicionar(self, value, vacina, data):
        if self.value < value:
            if self.right is None:
                self.right = Utente(value, vacina, data)
            else:
                self.right.adicionar(value, vacina, data)
        else:
            if self.left is None:
                self.left = Utente(value, vacina, data)
            else:
                self.left.adicionar(value, vacina, data)

    def inorder(self, inf):
        if self.left is not None:
            self.left.inorder(inf)
        if self.value is not None:
            inf.append(self)
        if self.right is not None:
            self.right.inorder(inf)

        return inf


class Vacina:
    def __init__(self, vacina, data):
        self.vacina = vacina
        self.data = data
        self.left = None
        self.right = None

    def adicionar(self, vacina, data):
        if self.vacina == vacina:
            self.data = data
            print("VACINA ATUALIZADA")
            return
        elif self.vacina < vacina:
            if self.right is None:
                print("NOVA VACINA INSERIDA")
                self.right = Vacina(vacina, data)
            else:
                self.right.adicionar(vacina, data)
        else:
            if self.left is None:
                print("NOVA VACINA INSERIDA")
                self.left = Vacina(vacina, data)
            else:
                self.left.adicionar(vacina, data)


    def inorder(self, inf):
        if self.left is not None:
            inf = self.left.inorder(inf)
        if self.vacina is not None:
            inf += " " + self.vacina + " " + self.data
        if self.right is not None:
            inf = self.right.inorder(inf)

        return inf


def menu(comandos):
    root = None
    for i in range(len(comandos)):
        if comandos[i][0] == 'ACRESCENTA':
            root = adicionar(root, int(comandos[i][1]), comandos[i][2], comandos[i][3])

        if comandos[i][0] == 'CONSULTA':
            consulta(root, int(comandos[i][1]))

        if comandos[i][0] == 'LISTAGEM':
            listagem(root)

        if comandos[i][0] == 'APAGA':
            root = None
            print("LISTAGEM DE NOMES APAGADA")


def adicionar(root, key, vacina, data):
    utente = search(root, key)

    if root is None:
        print("NOVO UTENTE CRIADO")
        return Utente(key, vacina, data)
    else:
        if utente is None:
            print("NOVO UTENTE CRIADO")
            root.adicionar(key, vacina, data)
        else:
            utente.vacina.adicionar(vacina, data)
        return root


def consulta(root, key):
    utente = search(root, key)

    if utente is not None:
        inf = str(utente.vacina.inorder(str(utente.value)))
        print(inf)
        print("FIM")
        return

    print("NAO ENCONTRADO")


def listagem(root):
    num_list = root.inorder([])
    for i in range(len(num_list)):
        inf = num_list[i].vacina.inorder(str(num_list[i].value))
        print(inf)
    print("FIM")


def search(root, key):
    if root is not None:
        if root.value == key:
            return root
        elif root.value < key:
            return search(root.right, key)
        else:
            return search(root.left, key)
    else:
        return None



# -------------- Test and Objectives Part -------------- #

vacinas = ["photograph", "profession", "functional", "acceptable", "plagiarize", "overcharge", "relinquish",
           "democratic", "vegetarian", "commitment"]


def cenario_1(n, iter, pesq):
    root = None
    t1 = time.time()
    for i in range(int(n * iter)):
        root = adicionar(root, random.randint(1, 20000), random.choice(vacinas), str(random.randint(1, 10000000)))

    for i in range(int(n * pesq)):
        consulta(root, random.randint(1, 20000))
    return time.time() - t1


c1 = sum([cenario_1(20000, 0.1, 0.9) for i in range(100)]) / 100
c2 = sum([cenario_1(40000, 0.1, 0.9) for i in range(100)]) / 100
c3 = sum([cenario_1(60000, 0.1, 0.9) for i in range(100)]) / 100

c4 = sum([cenario_1(80000, 0.1, 0.9) for i in range(100)]) / 100

c5 = sum([cenario_1(100000, 0.1, 0.9) for i in range(100)]) / 100


c6 = sum([cenario_1(20000, 0.9, 0.1) for i in range(100)]) / 100

c7 = sum([cenario_1(40000, 0.9, 0.1) for i in range(100)]) / 100

c8 = sum([cenario_1(60000, 0.9, 0.1) for i in range(100)]) / 100

c9 = sum([cenario_1(80000, 0.9, 0.1) for i in range(100)]) / 100

c10 = sum([cenario_1(100000, 0.9, 0.1) for i in range(100)]) / 100

print("c1 >>> ", c1)
print("c2 >>> ", c2)
print("c3 >>> ", c3)
print("c4 >>> ", c4)
print("c5 >>> ", c5)
print("c1 >>> ", c6)
print("c2 >>> ", c7)
print("c3 >>> ", c8)
print("c4 >>> ", c9)
print("c5 >>> ", c10)
