import json
from queue import PriorityQueue

A = 4
C = 4
M = 9
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

def random_gen(seed):
    last_num = seed
    while( True ):
        next_num = (A*last_num + C) % M
        last_num = next_num
        yield next_num / float((M-1))

def conversor_base(num, min, max):
    return (max - min) * num + min

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


def main():
    random_nums = random_gen(SEED)
    filas = []
    agenda = PriorityQueue() # (tempo, oque, onde) = (2.52, saida, fila1)   
    
    with open('entrada.json', 'r') as json_file:
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
            
    agenda.put((data["Tempo Inicio"], "chegada", data["Fila de Entrada"]))

    for i in range(100):
        evento = agenda.get()
        if(evento[1] == "chegada"): 
            chegada(evento[0], agenda, filas[0], random_nums)
        #elif(evento[1] == "saida"): saida()

if __name__ == "__main__":
    main()    