import threading
import time
import random
from queue import Queue

class Restaurante:
    
    def __init__(self):
        self.fogao_disponivel = threading.Semaphore(1)  # 1 = disponivel
        self.fila_chefs = Queue()  # fila de fifo
        self.chefs = ["Chef 1", "Chef 2", "Chef 3"] # lista de chefs
        random.shuffle(self.chefs) # embaralha os chefs na lista
        # adiciona todos chefs na lista
        for chef in self.chefs:
            self.enterq(chef)

    # funcao pra add os chefs na fila
    def enterq(self, chef):
        self.fila_chefs.put(chef)
        self.showq()

    # funcao pra printar a fila
    def showq(self):
        chefs_esperando = list(self.fila_chefs.queue)
        if chefs_esperando:
            print("Chefes esperando na fila:", ", ".join(chefs_esperando))
        else:
            print("Não há chefes esperando na fila.")

    # funcao pra usar o fogao
    def cook(self):
        chef = self.fila_chefs.get()  # prox chef
        print(f"{chef} está utilizando o fogão.")
        tempo_uso = random.randint(2, 8)
        time.sleep(tempo_uso)
        print(f"{chef} terminou de usar o fogão após {tempo_uso} segundos.")

    # funcao que vai coordenar o acesso
    def chefcooking(self, chef):
        with self.fogao_disponivel:
            self.cook()

if __name__ == "__main__":
    restaurante = Restaurante()
    chefs_threads = []

    # inicializacao de threads
    for chef in restaurante.chefs:
        chef_thread = threading.Thread(target=restaurante.chefcooking, args=(chef,))
        chef_thread.start()
        chefs_threads.append(chef_thread)

    # espera fim de todas threads
    for chef_thread in chefs_threads:
        chef_thread.join()
