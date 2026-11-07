# Desafio 01 — Estacionamento de precisão

## Missão

Vocês programarão um robô que se aproxima de uma parede e estaciona sem encostar. A cada leitura do sensor, o programa deve decidir com que velocidade avançar. O robô já está alinhado; não é necessário fazer curvas.

**Sucesso:** distância frontal entre **0.27 e 0.33 m**, velocidade medida de no máximo **0.01 m/s**, comando zero e permanência nessas condições por **2 segundos de simulação**, sem colisão durante a tentativa. O limite é **45 segundos de simulação**. O cronômetro da tentativa começa na primeira leitura recebida pelo executor.

O objetivo principal é escrever uma estratégia compreensível, testar hipóteses e explicar as escolhas. A instalação será conferida antes da avaliação.

## Organização

Grupos de 3 ou 4 integrantes. Alternem quem edita o código, quem executa e registra os ensaios e quem revisa o raciocínio. Todos devem conseguir explicar a solução.

Pré-requisitos: variáveis, operações aritméticas, `if`/`elif`/`else`, funções, parâmetros e `return`. O executor já contém a repetição que chama a função continuamente. Não é necessário escrever código de comunicação com o Gazebo.

## O que editar

Somente `alunos/solucao.py`, na função:

```python
def decidir_velocidade(distancia):
    return 0.0
```

- `distancia` é um número em **metros**, medido da frente do robô até a parede.
- Retorne uma velocidade entre **0.0 e 0.5 m/s**.
- `0.0` significa parar. Valores maiores significam avançar mais depressa.
- Não há marcha a ré neste desafio. Se passar da faixa, reinicie e corrija a estratégia.
- A função é chamada a cada nova leitura, aproximadamente 20 vezes por segundo de simulação.
- A função deve retornar rapidamente. Não coloque `input()`, `sleep()` ou um laço infinito nela.

Exemplo de interpretação das unidades: 0.80 m são 80 cm; 0.30 m são 30 cm; 0.03 m são 3 cm. A velocidade pedida é em metros por segundo, não uma porcentagem da potência do motor.

## Regras

1. A decisão deve usar a distância recebida. Não use espera por tempo fixo, contagem de chamadas ou coordenadas conhecidas da parede.
2. Não altere o mundo, os sensores, a infraestrutura ou os limites de velocidade para realizar a avaliação.
3. Não envie comandos por outro programa enquanto o executor estiver ativo.
4. Toda tentativa começa com o mundo recarregado pelo procedimento do guia.
5. Registre pelo menos cinco ensaios e explique pelo menos duas mudanças feitas na estratégia.
6. Declare materiais consultados e ferramentas usadas, conforme a política da disciplina.

## Etapas sugeridas

**Etapa 1 — Entender.** Execute o programa inicial e explique por que ele fica parado. Observe a leitura do sensor e localize as unidades.

**Etapa 2 — Primeira estratégia.** Façam o robô avançar enquanto estiver longe e parar perto da meta. Escolham uma velocidade inicial conservadora.

**Etapa 3 — Melhorar.** Investiguem se vale a pena reduzir a velocidade perto da parede. A frenagem não é instantânea; o robô pode continuar se movendo depois de receber zero.

**Etapa 4 — Testar.** Repitam os ensaios com nomes diferentes de saída e comparem o tempo simulado e a distância final. Identifiquem o que mudou e o efeito observado.

**Etapa 5 — Explicar.** Preparem uma demonstração de até 5 minutos e a ficha do grupo preenchida.

## Níveis de realização

- **Essencial:** cumprir a missão no cenário de treino.
- **Robusto:** cumprir também em três cenários com distâncias iniciais diferentes, mantendo o robô alinhado e o sensor sem ruído.
- **Eficiente:** reduzir o tempo sem perder precisão ou robustez.

Não serão introduzidos giros, obstáculos laterais, falhas de sensor ou ruído surpresa nesta avaliação. Extensões desse tipo são atividades separadas.

## Entrega

- Arquivo `alunos/solucao.py`, com nomes de todos os integrantes em comentário.
- Ficha do grupo preenchida, com tabela de pelo menos cinco ensaios.
- CSV e JSON correspondentes aos ensaios relatados.
- Explicação breve das decisões e de uma limitação conhecida.
- Demonstração e explicação individual de uma parte da estratégia.

## Avaliação — 10 pontos

| Critério | Pontos | Evidência |
| --- | --- | --- |
| Cumprimento da missão | 5.0 | Duas tentativas no cenário de treino; cada sucesso vale 2.5. |
| Robustez | 2.0 | Uma tentativa em cada uma de três variações: 0, 1, 2 ou 3 sucessos valem 0, 0.7, 1.3 ou 2.0. |
| Clareza, experimentação e explicação | 2.0 | Código compreensível, registros e justificativas: 1.0; explicação individual: 1.0. |
| Eficiência | 1.0 | Entre tentativas bem-sucedidas de treino: média até 15 s vale 1.0; acima de 15 até 25 s vale 0.5; acima de 25 s vale 0. Sem sucesso: 0. |

Os limites de eficiência devem ser confirmados pelo professor no piloto e publicados antes da atividade. Problemas de instalação ou interrupções comprovadas do simulador serão tratados como incidentes e terão a tentativa refeita.
