from multiprocessing.pool import ThreadPool
from threading import Thread, Lock
from time import sleep
import random
from queue import Queue

import matplotlib.pyplot as plt

tempos_espera = []
tempo_espera = 0
ordem_preparo = []

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
            return True  # Retorna que havia ingredientes disponíveis
        else:
            return False  # Retorna que não havia ingredientes disponíveis


# Função que simula o processo de preparação dos ingredientes na cozinha
def cozinha():
    print("Cozinha: Iniciando processos de preparação de ingredientes.")
    sleep(1)  # Simula o tempo de preparação
    print("Cozinha: Ingredientes preparados e prontos para uso.")


# Função que representa um pedido feito ao restaurante
def pedido(numero_pedido, tempo_preparo, queue):
    print(f"Pedido {numero_pedido}: Iniciando pedido.")
    queue.put((numero_pedido, tempo_preparo))


def processar_pedidos(queue):
    global tempo_espera

    while True:
        pedido_info = queue.get()
        if pedido_info is None:
            break
        numero_pedido, tempo_preparo = pedido_info
        # Verifica se há ingredientes suficientes para o pedido
        if verificar_ingredientes('carne', 1) and \
                verificar_ingredientes('queijo', 1) and \
                verificar_ingredientes('tomate', 1):
            print(f"Pedido {numero_pedido}: Ingredientes disponíveis.")
            print(f"Pedido {numero_pedido}: Preparando pedido...")
            sleep(tempo_preparo)  # Simula o tempo de preparo
            print(f"Pedido {numero_pedido}: Pedido pronto em {tempo_preparo} segundos")
            print(f"Pedido {numero_pedido}: Pedido entregue!")

            ordem_preparo.append(numero_pedido)
            tempos_espera.append(tempo_espera)
            tempo_espera = tempo_preparo
        else:
            print(f"Pedido {numero_pedido}: Ingredientes insuficientes. Pedido cancelado.")
        queue.task_done()


# Função principal do programa
def main():
    num_pedidos = 5  # Número de pedidos a serem gerenciados

    # Fila para manter os pedidos em ordem
    pedidos_queue = Queue()

    # Iniciando a thread da cozinha
    cozinha_thread = Thread(target=cozinha)
    cozinha_thread.start()
    cozinha_thread.join()

    # Criando um pool de threads para processar os pedidos
    pool = ThreadPool()

    # Adicionando as tarefas dos pedidos ao pool
    tempos_preparo = [1, 5, 4, 5, 3]
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

    print("\nAvaliação do Algoritmo...")
    print("Ordem de preparo:", ordem_preparo)
    print("Tempos de espera:", tempos_espera)
    print(f"Tempos médio de espera: {sum(tempos_espera) / len(tempos_espera)} segundos.")

    # Criando o gráfico de Gantt
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Tempo')
    gnt.set_ylabel('Pedidos')
    gnt.set_title('Gráfico de Gantt - Tempos de Espera')

    # Definindo as barras do gráfico
    gnt.set_xlim(0, sum(tempos_preparo))
    gnt.grid(True)

    print(ordem_preparo)
    y_ticks = range(1, len(ordem_preparo) + 1)
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels([f'Pedido {i}' for i in ordem_preparo])

    soma_tempo_espera = 0
    for i in range(len(ordem_preparo)):
        soma_tempo_espera = soma_tempo_espera + tempos_espera[ordem_preparo[i] - 1]
        gnt.broken_barh([(soma_tempo_espera, tempos_preparo[ordem_preparo[i] - 1])], (i, 0.1), facecolors='blue')

    # Exibindo o gráfico
    plt.savefig("fifo_gantt.png")


# Verifica se o script está sendo executado diretamente como o programa principal
if __name__ == "__main__":
    main()
