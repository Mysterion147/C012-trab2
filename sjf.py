from multiprocessing.pool import ThreadPool
from threading import Thread, Lock
from time import sleep
import random
from queue import PriorityQueue

# Variáveis globais de ingredientes
ingredientes = {'tomate': 5, 'queijo': 5, 'carne': 5}
ingredientes_lock = Lock()

def verificar_ingredientes(ingrediente, quantidade):
    # Função de verificação dos ingredientes
    global ingredientes
    
    with ingredientes_lock:
        # Verifica a quantidade de ingredientes disponíveis
        if ingredientes.get(ingrediente, 0) >= quantidade:
            # Caso tenha, decremente a quantidade usada do estoque
            ingredientes[ingrediente] -= quantidade
            return True # Retorna que havia ingredientes disponíveis
        else:
            return False # Retorna que não havia ingredientes disponíveis

# Função que simula o processo de preparação dos ingredientes na cozinha
def cozinha():
    print("Cozinha: Iniciando processos de preparação de ingredientes.")
    sleep(2) # Simula o tempo de preparação
    print("Cozinha: Ingredientes preparados e prontos para uso.")

# Função que representa um pedido feito ao restaurante
def pedido(numero_pedido, tempo_preparo, queue):
    print(f"Pedido {numero_pedido}: Iniciando pedido.")
    queue.put((tempo_preparo, numero_pedido))

def processar_pedidos(queue):
    while True:
        pedido_info = queue.get()
        if pedido_info is None:
            break
        tempo_preparo, numero_pedido = pedido_info
        # Verifica se há ingredientes suficientes para o pedido
        if verificar_ingredientes('carne', 1) and \
            verificar_ingredientes('queijo', 1) and \
            verificar_ingredientes('tomate', 1):
            print(f"Pedido {numero_pedido}: Ingredientes disponíveis.")
            print(f"Pedido {numero_pedido}: Preparando pedido...")
            sleep(tempo_preparo) # Simula o tempo de preparo
            print(f"Pedido {numero_pedido}: Pedido pronto em {tempo_preparo} segundos")
            print(f"Pedido {numero_pedido}: Pedido entregue!")
        else:
            print(f"Pedido {numero_pedido}: Ingredientes insuficientes. Pedido cancelado.")
        queue.task_done()

# Função principal do programa
def main():
    num_pedidos = 5  # Número de pedidos a serem gerenciados

    # Fila de prioridade para manter os pedidos ordenados pelo tempo de preparo
    pedidos_queue = PriorityQueue()

    # Iniciando a thread da cozinha
    cozinha_thread = Thread(target=cozinha)
    cozinha_thread.start()

    # Criando um pool de threads para processar os pedidos
    pool = ThreadPool()

    # Adicionando as tarefas dos pedidos ao pool
    tempos_preparo = [random.randint(1, 5) for _ in range(num_pedidos)]
    for i, tempo in enumerate(tempos_preparo, start=1):
        pool.apply_async(pedido, args=(i, tempo, pedidos_queue))

    # Fechando o pool e aguardando todas as tarefas terminarem
    pool.close()
    pool.join()

    # Iniciando a thread que processa os pedidos na ordem da fila
    processador_thread = Thread(target=processar_pedidos, args=(pedidos_queue,))
    processador_thread.start()

    # Aguardando a fila ser esvaziada
    pedidos_queue.join()

    # Finalizando a thread de processamento de pedidos
    pedidos_queue.put(None)
    processador_thread.join()

    print("Todos os pedidos em preparação, foram finalizados!")

# Verifica se o script está sendo executado diretamente como o programa principal
if __name__ == "__main__":
    main()