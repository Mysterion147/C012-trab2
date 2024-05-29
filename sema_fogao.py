import threading
import time
import random

class Restaurante:
    def __init__(self):
        self.fogao_disponivel = threading.Semaphore(1)  # Inicialmente, o fogão está disponível
        self.chefs = ["Chef 1", "Chef 2", "Chef 3"]  # Lista de chefs

    def usar_fogao(self, chef):
        print(f"{chef} está esperando para usar o fogão.")
        self.fogao_disponivel.acquire()  # Chef tenta adquirir o fogão
        print(f"{chef} está utilizando o fogão.")
        tempo_uso = random.randint(1, 5)  # Tempo aleatório de uso do fogão (1 a 5 segundos)
        time.sleep(tempo_uso)
        print(f"{chef} terminou de usar o fogão após {tempo_uso} segundos.")
        self.fogao_disponivel.release()  # Chef libera o fogão

def chef_cozinhando(restaurante, chef):
    while True:
        restaurante.usar_fogao(chef)
        time.sleep(random.uniform(1, 3))  # Tempo aleatório entre usar o fogão novamente

if __name__ == "__main__":
    restaurante = Restaurante()
    chefs_threads = []

    # Inicializa as threads para os chefs
    for chef in restaurante.chefs:
        chef_thread = threading.Thread(target=chef_cozinhando, args=(restaurante, chef))
        chef_thread.start()
        chefs_threads.append(chef_thread)

    # Espera todas as threads terminarem
    for chef_thread in chefs_threads:
        chef_thread.join()
