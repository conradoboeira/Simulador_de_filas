# Simulador de Filas
# Autores: Conrado Boeira e Guilherme Maurer


import json
from queue import PriorityQueue
import sys
from prettytable import PrettyTable

# Variaveis para a geracao de numeros aleatorios
A = 2 ** 64
C = 7
M = 10000
SEED = 1

# Variaveis de controle das filas
filas = []
rede = {}
agenda = PriorityQueue() # (tempo, oque, onde) = (2.52, saida, fila1)


class Fila:
  def __init__(self, nome, capacidade, servidores,
            tempo_max_servidor, tempo_min_servidor,
            tempo_max_chegada = -1, tempo_min_chegada = -1, perda=0):
    self.nome = nome
    self.capacidade = capacidade
    self.servidores = servidores
    self.tempo_max_servidor = tempo_max_servidor
    self.tempo_min_servidor = tempo_min_servidor
    self.tempo_max_chegada = tempo_max_chegada
    self.tempo_min_chegada = tempo_min_chegada
    self.tempo = {"total" : 0.0, "total_acumulado" : 0.0}
    self.ocupacao = 0
    self.perda=perda

# Gerador de numeros aleatorios
def random_gen(seed):
    last_num = seed
    while( True ):
        next_num = (A*last_num + C) % M
        last_num = next_num
        yield next_num / float((M-1))

def conversor_base(num, min, max):
    return (max - min) * num + min

def find_max_ocupacao(tempo):
    max_ocupacao = 0
    for t in tempo:
        if(isinstance(t, int)):
            if(t > max_ocupacao):
                max_ocupacao = t
    return max_ocupacao

def contabiliza_tempo(tempo_atual):
    for fila in filas:
        if(fila.ocupacao in fila.tempo):
            fila.tempo[fila.ocupacao] += tempo_atual - fila.tempo["total"]
        else:
            fila.tempo[fila.ocupacao] = tempo_atual - fila.tempo["total"]

        fila.tempo["total"] = tempo_atual

def get_anterior(fila):
    for key in rede:
        if(rede[key] == fila): return key
    return None

def get_fila(nome):
    for fila in filas:
        if(fila.nome == nome): return fila
    return None

def chegada(tempo_atual, fila, random_nums):

    # Contabiliza tempo
    contabiliza_tempo(tempo_atual)

    anterior = get_anterior(fila.nome)
    if(anterior):
        fila_anterior = get_fila(anterior)
        fila_anterior.ocupacao -= 1
        if(fila_anterior.ocupacao >= fila_anterior.servidores):
            proximo_tempo =  tempo_atual + conversor_base(next(random_nums), fila_anterior.tempo_min_servidor, fila_anterior.tempo_max_servidor)
            tempo_atual = proximo_tempo
            agenda.put((proximo_tempo, "chegada", fila.nome))


    # se fila < capacidade
    #     fila ++
    #     se fila <= servidores
    #         agenda saida (tempo + rnd)

    if(fila.ocupacao < fila.capacidade):
        fila.ocupacao +=1
        if fila.ocupacao <= fila.servidores:
            proximo_tempo =  tempo_atual + conversor_base(next(random_nums), fila.tempo_min_servidor, fila.tempo_max_servidor)
            # Checa se ela tem uma conexao na saida com outra fila
            if(fila.nome in rede):
                agenda.put((proximo_tempo, "chegada", rede[fila.nome]))
            else:
                agenda.put((proximo_tempo, "saida", fila.nome))
    else:
        fila.perda+=1

    if(not anterior):
        # agenda chegada( t +rnd)
        proximo_tempo =  tempo_atual + conversor_base(next(random_nums),fila.tempo_min_chegada,fila.tempo_max_chegada)
        agenda.put((proximo_tempo, "chegada", fila.nome))

def saida(tempo_atual, fila, random_nums):

    # Contabiliza tempo
    contabiliza_tempo(tempo_atual)

    # Fila --
    # Se fila  > =1
    #  agenda SAIDA(T+rnd(3..6))

    fila.ocupacao -= 1

    if fila.ocupacao >= fila.servidores:
        proximo_tempo =  tempo_atual + conversor_base(next(random_nums), fila.tempo_min_servidor, fila.tempo_max_servidor)
        agenda.put((proximo_tempo, "saida", fila.nome))


def main(file_name):
    # Parse Input
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
        for fila in data["Filas"]:
            comportamento = fila["Comportamento"].split(r"/")
            if(len(comportamento) == 3):
                _,_,servidores = comportamento
                capacidade = -1
            else:
                _,_,servidores,capacidade = comportamento

            if( "Tempo de Chegada" in fila):
                min_chegada, max_chegada = fila["Tempo de Chegada"].split(r"/")
            else:
                min_chegada = -1
                max_chegada = -1
            min_atendimento, max_atendimento = fila["Tempo de Atendimento"].split(r"/")

            nova_fila = Fila(fila["Nome"], int(capacidade), int(servidores),
                        float(max_atendimento), float(min_atendimento),
                        float(max_chegada), float(min_chegada))
            filas.append(nova_fila)
        for conexao in data["Rede"]:
            fila1, fila2 = conexao.split(r"/")
            rede[fila1] = fila2

    # Agenda o primeiro evento
    global agenda
    agenda.put((data["Tempo Inicio"], "chegada", data["Fila de Entrada"]))

    print("SIMULANDO")
    for s in data["Seeds"]:
        global SEED
        SEED = int(s)
        random_nums = random_gen(SEED)
        print("Simulacao com seed {}".format(SEED))
        while True:
            evento = agenda.get()
            if(evento[1] == "chegada"):
                chegada(evento[0], get_fila(evento[2]), random_nums)
            elif(evento[1] == "saida"):
                saida(evento[0], get_fila(evento[2]), random_nums)
            if (filas[0].tempo["total"] >= data["Tempo de Execucao"]):
                break

        # Limpa as filas para a proxima execucao
        for fila in filas:
            fila.ocupacao = 0
            fila.tempo["total_acumulado"] += fila.tempo["total"]
            fila.tempo["total"] = 0
        agenda = PriorityQueue()
        agenda.put((data["Tempo Inicio"], "chegada", data["Fila de Entrada"]))


    # Parse output
    for fila in filas:
        print("\n-----------------------------------\n")
        print("Fila " + fila.nome)
        print("Comportamento: G/G/{}/{}".format(fila.servidores, fila.capacidade))
        if(fila.tempo_min_chegada != -1 and fila.tempo_max_chegada):
            print("Tempo de chegada: {}..{}".format(fila.tempo_min_chegada, fila.tempo_max_chegada))
        print("Tempo de servico: {}..{}".format(fila.tempo_min_servidor, fila.tempo_max_servidor))
        #print('\nEstado      Tempo      Probabilidade')

        total = fila.tempo["total_acumulado"]
        max_ocupacao = find_max_ocupacao(fila.tempo)
        tabela = PrettyTable()
        tabela.field_names = ["Estado","Tempo","Probabilidade"]
        probs = [] # lista de probabilidades, usado depois no calculo das metricas
        for i in range(max_ocupacao + 1):
            #print("{}  {}  {:.2f}%".format(i, fila.tempo[i],(fila.tempo[i]/float(total))*100))
            tabela.add_row([i,fila.tempo[i],(fila.tempo[i]/float(total))*100])
            probs.append(fila.tempo[i]/float(total))
        print()
        print(tabela)

        # Programacao Funcional
        pop_media = sum([i*probs[i] for i in range(len(probs))])
        mu = 60/((fila.tempo_min_servidor + fila.tempo_max_servidor)/2)
        mu_i = [min(i,fila.servidores)*mu for i in range(max_ocupacao+1)]
        vazao = sum([p*m for p,m in zip(probs,mu_i)])
        utilizacao = sum([(min(i,fila.servidores)/fila.servidores)*probs[i] for i in range(len(probs))])
        tempo_resp = pop_media/vazao

        print("\nEstatisticas")
        print("Numero de clientes perdidos: " + str(fila.perda))
        print("Populacao media: " + str(pop_media))
        print("Vazao: " + str(vazao))
        print("Utilizacao: " + str(utilizacao))
        print("Tempo de resposta: " + str(tempo_resp))



    print("\n-----------------------------------\n")
    print("Tempo total de execucao: {}".format(data["Tempo de Execucao"]))




if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print('Uso python3 simulador.py <file>')
    main(sys.argv[1])

