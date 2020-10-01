# Simulador de filas - Conrado Boeira e Guilherme Maurer

Neste trabalho foi desenvolvido um simulador de filas simples e em tandem. Para executar o programa é primeiro preciso criar um arquivo json de configuração para definir as especificações das filas. Este arquivo deve ser no formato:

```yaml
{
    "Tempo Inicio" : t0,
    "Fila de Entrada" : "f1",
    "Filas" : [
        {   
            "Nome" : "f1", 
            "Comportamento":"G/G/s/c",
            "Tempo de Chegada" : "c0/c1",
            "Tempo de Atendimento" : "a0/a1"
        },
        {   
            "Nome" : "f2", 
            "Comportamento":"G/G/s/c",
            "Tempo de Chegada" : "c0/c1",
            "Tempo de Atendimento" : "a0/a1"
        }
    ],
    "Rede" : ["f1/f2"]
    "Seeds" :[sed],
    "Tempo de Execucao" : t1
}
```

Onde t0 e t1 definem o tempo de inicio e total da simulação respectivamente, f1 e f2 definem os nomes da filas, s e c definem o número de servidores e a capacidade de uma fila, c0, c1, a0 e a1 definem respectivamente, o tempo mínimo e máximo de chegada e atendimento e sed define uma lista de Seeds a serem usadas pelo gerador de números aleatórios. Rede define a sequencia de filas em tandem. Junto com o código também foi também fornecido um arquivo de configuração já completo, com o nome "filas_tandem.json".json".

Antes de executar o código, é preciso instalar as depências necessárias usando o comando:

```bash
pip install -r requirements.txt
```

Uma vez que o arquivo de configuração foi criado, para executar o código use:

```bash
python simulador.py <arquivo de configuração>
```

Nota: o código foi desenvolvido e testado usando a linguagem Python 3.8.5
