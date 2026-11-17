from sys import stdin, stdout


def readln():
    return stdin.readline().rstrip()


comandos = []
comando = ""
while comando != "FIM":
    comando = readln()
    comandos.append(comando.split())


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


if __name__ == '__main__':
    menu(comandos)

