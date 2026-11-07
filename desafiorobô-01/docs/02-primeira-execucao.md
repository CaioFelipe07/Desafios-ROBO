# 2. Primeira execução e operação

## Antes de começar

Conclua a instalação. Deixe abertos dois terminais na pasta do pacote e, no caminho Docker, a tela do navegador. Comandos `docker compose exec` são digitados no terminal do **seu computador**, não na barra de endereço do navegador nem no console do Python.

## Passo 1 — Abrir o cenário

No terminal A:

```sh
docker compose exec sim bash scripts/iniciar.sh
```

O terminal fica ocupado: isso é esperado. Na tela do navegador aparecerá o Gazebo com um robô azul, uma parede vermelha e uma marca verde no chão. Aguarde a cena carregar.

O script usa `-r`, portanto a simulação começa rodando. Na interface, o controle Play/Pause pode interromper e retomar o tempo. A missão só avança com o tempo de simulação rodando. O sensor fica na frente do robô, voltado para a parede.

Se a câmera não mostrar a cena, procure o modelo `robo` na árvore de entidades, selecione e use o recurso de mover a câmera para a seleção, disponível no menu de contexto. A navegação da câmera também pode ser feita com o mouse. Consulte o [guia oficial da interface](https://gazebosim.org/docs/harmonic/gui/).

## Passo 2 — Conferir se o sensor funciona

No terminal B:

```sh
docker compose exec sim gz topic -l
docker compose exec sim gz topic -e -t /desafio/scan
```

O primeiro comando deve incluir `/desafio/scan`, `/desafio/odom` e `/desafio/cmd_vel`. O segundo imprime mensagens continuamente; procure `ranges`, com valores próximos de **2.65 m** no cenário inicial. Use **Ctrl+C** para parar apenas essa visualização. O tópico de contato pode ficar silencioso enquanto não existe contato.

Os scripts configuram `GZ_PARTITION=estacionamento01`; no Docker isso já está no ambiente. No Ubuntu direto, antes dos comandos de diagnóstico `gz topic`, execute `export GZ_PARTITION=estacionamento01` nesse terminal.

## Passo 3 — Executar o código inicial

No terminal B:

```sh
docker compose exec sim bash scripts/executar.sh
```

O robô fica parado. O arquivo inicial retorna zero para qualquer distância. Use Ctrl+C depois de conferir; o programa envia uma parada e grava os resultados. O limite normal é 45 segundos **de simulação**, contados a partir da primeira leitura recebida pelo executor.

Não deixe esse executor rodando ao iniciar outro. Somente um programa pode comandar o robô por vez.

## Passo 4 — Demonstração do professor

Disponível apenas no pacote completo. Encerre o executor anterior e inicie uma tentativa nova pelo procedimento de reinício abaixo. No terminal B:

```sh
docker compose exec sim bash scripts/executar.sh --solucao professor/referencia.py --saida resultados/demo
```

Espera-se que o robô avance, reduza a velocidade e pare na faixa. A saída deve terminar com `"status": "sucesso"`. Essa é uma **expectativa a validar na máquina**, não uma execução previamente comprovada neste material.

A marca verde indica onde a frente do robô deve ficar; não é a posição do centro dele. A distância é medida da frente à parede. A meta é um intervalo de 0.27 a 0.33 m.

## Passo 5 — Editar e repetir

Abra `alunos/solucao.py` em um editor, altere somente `decidir_velocidade`, salve e reinicie a tentativa. Não é necessário reiniciar o Docker por edição. O Python relê o arquivo ao iniciar o executor.

Registre cada ensaio com um nome diferente:

```sh
docker compose exec sim bash scripts/executar.sh --saida resultados/grupo01-teste01
```

Arquivos existentes com o mesmo nome serão substituídos. Os resultados ficam na pasta local `resultados`, em CSV (leituras e comandos) e JSON (resumo). O CSV pode ser aberto em um editor ou importado em uma planilha.

## Como reiniciar corretamente

1. No terminal B, pressione Ctrl+C se o executor ainda estiver rodando e espere o resumo final.
2. No terminal A, pressione Ctrl+C para fechar o Gazebo e espere o comando terminar.
3. Inicie novamente `docker compose exec sim bash scripts/iniciar.sh` no terminal A.
4. Aguarde o cenário aparecer; confira que o robô voltou à posição inicial.
5. Execute novamente a estratégia no terminal B.

Esse procedimento recarrega o mundo, a velocidade e os relógios. Evita as ambiguidades de diferentes botões Reset da interface. Não use Reset durante uma tentativa avaliada.

## Parada imediata

Ctrl+C no executor deve enviar velocidade zero. Se o programa travar ou a sessão cair, abra outro terminal e use:

```sh
docker compose exec sim bash scripts/parar.sh
```

Se necessário, use Pause na interface ou feche o Gazebo no terminal A. Comandos de velocidade podem persistir se um processo for encerrado abruptamente; o comando de parada não substitui encerrar um controlador ainda ativo que continue publicando movimento.

## Erros frequentes

| Sintoma | Verificação e ação |
| --- | --- |
| `docker: compose is not a docker command` | Instale ou reinstale Docker Desktop; o comando Docker isolado não basta. |
| `Cannot connect to the Docker daemon` | Abra Docker Desktop e espere o mecanismo iniciar. |
| `no configuration file provided` | Abra o terminal na pasta que contém `compose.yaml`. |
| Navegador não conecta | Execute `docker compose ps` e `docker compose logs --tail 80 sim`; confira a porta 6080. |
| `port is already allocated` | Há outro serviço usando 6080. Encerre a instância anterior ou altere somente o primeiro 6080 em `compose.yaml` e use a nova porta no navegador. |
| Área de trabalho vazia | Inicie `scripts/iniciar.sh`; a área de trabalho sozinha não inicia a simulação. |
| Tela preta ou erro Ogre/OpenGL | Confira `docker compose exec sim glxinfo -B`. A renderização por software deve estar disponível. Não desative o sistema Sensors para esconder o erro: o sensor deixaria de funcionar. Tente Ubuntu nativo se o perfil gráfico não funcionar. |
| Robô parado com código inicial | É o comportamento esperado de `return 0.0`. |
| Robô parado com referência | Verifique Play, mensagens `/desafio/scan`, importações Python e se há dois controladores ativos. |
| `ModuleNotFoundError: gz` | No Docker use os comandos fornecidos. No Ubuntu use `/usr/bin/python3`, com os pacotes do instalador; não use ambiente Conda ou virtualenv sem configurar os bindings. |
| `sem_sensor_ou_odometria` | Verifique a simulação, os tópicos, o carregamento dos plugins e o estado Play. |
| `sensor_ou_simulacao_sem_atualizacao` | Houve pausa, perda de mensagens ou máquina muito lenta por mais de 3 s reais. Reinicie; não conte como erro algorítmico sem investigar. |
| Erro de sintaxe no aluno | Confira dois-pontos, indentação e se o retorno é um número. |
| Muito lento ou sem janela no Mac ARM | Atualize o pacote e reconstrua com `docker compose up -d --build`. A versão corrigida usa ARM nativo. Confira `docker compose exec sim uname -m`: deve ser `aarch64` em Apple Silicon. |

Para depurar a construção: `docker compose build --progress plain`. Copie a primeira mensagem de erro relevante, o sistema operacional e o tipo de processador ao pedir ajuda.
