# Simulador de filas - Conrado Boeira e Guilherme Maurer

Neste trabalho foi desenvolvido um simulador de filas simples. Para executar o programa é primeiro preciso criar um arquivo json de configuração para definir as especificações da fila. Este arquivo deve ser no formato:

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
        }
    ],
    "Seeds" :[sed],
    "Tempo de Execucao" : t1
}
```

Onde t0 e t1 definem o tempo de inicio e total da simulação respectivamente, f1 define o nome da fila, s e c definem o número de servidores e a capacidade da fila, c0, c1, a0 e a1 definem respectivamente, o tempo mínimo e máximo de chegada e atendimento e sed define uma lista de Seeds a serem usadas pelo gerador de números aleatórios. A chave "Filas" é definida como uma lista para facilitar a futura expansão desse projeto para um simulador de múltiplas filas. Junto com o código também foram fornecidos dois arquivos de configuração já completos, "fila1.json" e "fila2.json".

Uma vez que o arquivo de configuração foi criado, para executar o código use:

```bash
python3 simulador.py <arquivo de configuração>
```

