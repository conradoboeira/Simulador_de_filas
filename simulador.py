import json
from queue import PriorityQueue
import sys

A = 2 ** 64
C = 7
M = 10000
SEED = 7

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
    self.tempo = {"total" : 0.0}
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

def chegada(tempo_atual, agenda, fila, random_nums):

    # Contabiliza tempo
    if(fila.ocupacao in fila.tempo):
        fila.tempo[fila.ocupacao] += tempo_atual - fila.tempo["total"]
    else:
        fila.tempo[fila.ocupacao] = tempo_atual - fila.tempo["total"]

    fila.tempo["total"] = tempo_atual

    # se fila < capacidade
    #     fila ++
    #     se fila <= servidores
    #         agenda saida (tempo + rnd)

    if(fila.ocupacao < fila.capacidade):
        fila.ocupacao +=1
        if fila.ocupacao <= fila.servidores:
            proximo_tempo =  tempo_atual + conversor_base(next(random_nums), fila.tempo_min_servidor, fila.tempo_max_servidor)
            agenda.put((proximo_tempo, "saida", fila.nome))
    else:
        fila.perda+=1

    # agenda chegada( t +rnd)
    proximo_tempo =  tempo_atual + conversor_base(next(random_nums),fila.tempo_min_chegada,fila.tempo_max_chegada)
    agenda.put((proximo_tempo, "chegada", fila.nome))

def saida(tempo_atual, agenda, fila, random_nums):

    # Contabiliza tempo
    if(fila.ocupacao in fila.tempo):
        fila.tempo[fila.ocupacao] += tempo_atual - fila.tempo["total"]
    else:
        fila.tempo[fila.ocupacao] = tempo_atual - fila.tempo["total"]

    fila.tempo["total"] = tempo_atual

    # Fila --
    # Se fila  > =1
    #  agenda SAIDA(T+rnd(3..6))

    fila.ocupacao -= 1

    if fila.ocupacao >= fila.servidores:
        proximo_tempo =  tempo_atual + conversor_base(next(random_nums), fila.tempo_min_servidor, fila.tempo_max_servidor)
        agenda.put((proximo_tempo, "saida", fila.nome))


def main(file_name):
    random_nums = random_gen(SEED)
    filas = []
    agenda = PriorityQueue() # (tempo, oque, onde) = (2.52, saida, fila1)

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

    # Agenda o primeiro evento
    agenda.put((data["Tempo Inicio"], "chegada", data["Fila de Entrada"]))

    print("SIMULANDO")
    while True:
        evento = agenda.get()
        if(evento[1] == "chegada"):
            chegada(evento[0], agenda, filas[0], random_nums)
        elif(evento[1] == "saida"):
            saida(evento[0], agenda, filas[0], random_nums)
        if (filas[0].tempo["total"] >= data["Tempo de Execucao"]):
            break

    # Parse output
    for fila in filas:
        print("Fila " + fila.nome)
        print("Comportamento: G/G/{}/{}".format(fila.servidores, fila.capacidade))
        print("Tempo de chegada: {}..{}".format(fila.tempo_min_chegada, fila.tempo_max_chegada))
        print("Tempo de serviço: {}..{}".format(fila.tempo_min_servidor, fila.tempo_max_servidor))
        print('Estado      Tempo      Probabilidade')

        total = fila.tempo["total"]
        max_ocupacao = find_max_ocupacao(fila.tempo)
        for i in range(max_ocupacao + 1):
            print("{}  {}  {:.2f}%".format(i, fila.tempo[i],(fila.tempo[i]/float(total))*100))


        print("Número de clientes perdidos: " + str(fila.perda))





if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print('Uso python3 simulador.py <file>')
    main(sys.argv[1])
