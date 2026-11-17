import time
import random



class Utente:
    def __init__(self, key, vacina, data):
        self.value = key
        self.left = None
        self.right = None
        self.vacina = Vacina(vacina, data)
        self.height = 1

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
        self.height = 1

    def inorder(self, inf):
        if self.left is not None:
            inf = self.left.inorder(inf)
        if self.vacina is not None:
            inf += " " + self.vacina + " " + self.data
        if self.right is not None:
            inf = self.right.inorder(inf)

        return inf


class AVLTree:
    def acrescenta_Utente(self, root, key, vacina, data):
        if not root:
            print("NOVO UTENTE CRIADO")
            return Utente(key, vacina, data)
        elif key == root.value:
            root.vacina = self.acrescenta_Vacina(root.vacina, vacina,data)
        elif key < root.value:
            root.left = self.acrescenta_Utente(root.left, key, vacina, data)
            root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        else:
            root.right = self.acrescenta_Utente(root.right, key, vacina, data)
            root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        fE = self.getBalance(root)

        if fE > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if fE < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    def acrescenta_Vacina(self, root, vacina, data):
        if not root:
            print("NOVA VACINA INSERIDA")
            return Vacina(vacina, data)
        elif vacina == str(root.vacina):
            print("VACINA ATUALIZADA")
            root.data = data
        elif vacina < str(root.vacina):
            root.left = self.acrescenta_Vacina(root.left, vacina, data)
            root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        else:
            root.right = self.acrescenta_Vacina(root.right, vacina, data)
            root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        fE = self.getBalance(root)

        if fE > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if fE < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    def getBalance(self, root):
        if not root:
            return 0
        else:
            return self.getHeight(root.left) - self.getHeight(root.right)

    def rightRotate(self, z):
        y = z.left
        T2 = y.right
        y.right = z
        z.left = T2

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root:
            return 0
        else:
            return root.height


def menu(comandos):
    root = None
    avl_tree = AVLTree()
    for i in range(len(comandos)):
        if comandos[i][0] == 'ACRESCENTA':
            root = avl_tree.acrescenta_Utente(root, int(comandos[i][1]), comandos[i][2], comandos[i][3])

        if comandos[i][0] == 'CONSULTA':
            consulta(root, int(comandos[i][1]))

        if comandos[i][0] == 'LISTAGEM':
            listagem(root)

        if comandos[i][0] == 'APAGA':
            root = None
            print("LISTAGEM DE NOMES APAGADA")


def listagem(root):
    if root is not None:
        num_list = root.inorder([])
        for i in range(len(num_list)):
            inf = num_list[i].vacina.inorder(str(num_list[i].value))
            print(inf)
    print("FIM")


def consulta(root, key):
    utente = search(root, key)

    if utente is not None:
        inf = str(utente.vacina.inorder(str(utente.value)))
        print(inf)
        print("FIM")
        return

    print("NAO ENCONTRADO")


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
    avl_tree = AVLTree()
    t1 = time.time()
    for i in range(int(n * iter)):
        root = avl_tree.acrescenta_Utente(root, random.randint(1, 20000), random.choice(vacinas), str(random.randint(1, 10000000)))

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