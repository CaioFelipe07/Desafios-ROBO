# 1. Instalação, do zero

## O que você vai usar

O **Gazebo** simula o robô, a parede, o movimento e o sensor. O **Python** executa a estratégia escrita pelos alunos. Um arquivo **SDF** descreve o cenário. Não é necessário instalar ROS para esta atividade.

Adotamos **Gazebo Harmonic** para fixar a combinação de versões: Sim 8, Transport 13 e mensagens 10. Existem versões posteriores; misturar as bibliotecas de versões diferentes pode impedir os programas de funcionar.

Como os grupos usarão computadores próprios, o caminho comum é **Docker + navegador**. O Docker executa um Ubuntu preparado; o navegador mostra a tela desse Ubuntu. Não se trata de uma versão web do Gazebo: a simulação continua rodando localmente no computador.

Como referência de planejamento, reserve 4 núcleos, 6 GB de memória para o Docker e aproximadamente 15 GB livres. São estimativas para este pacote, não requisitos oficiais universais. Em computadores com 8 GB de RAM total pode haver lentidão. O primeiro download exige internet; a imagem pode ocupar vários GB. Faça a instalação antes da aula.

## Opção A — Mac, Windows ou Linux com Docker

### A1. Instalar e abrir o Docker

- **Mac:** baixe o Docker Desktop para o processador correto, Apple Silicon (M1/M2/M3/M4 etc.) ou Intel. Arraste o aplicativo para Aplicativos e abra. Siga a [instalação oficial para Mac](https://docs.docker.com/desktop/setup/install/mac-install/).
- **Windows:** instale o Docker Desktop com o mecanismo WSL 2 e contêineres Linux. Se o instalador pedir atualização do WSL ou reinício, conclua essas etapas. Siga a [instalação oficial para Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Se necessário, execute `wsl --install` em PowerShell como administrador e reinicie antes de continuar.
- **Linux:** use [Docker Engine e o plugin Compose](https://docs.docker.com/engine/install/) ou Docker Desktop. O usuário precisa conseguir executar `docker info`.

Abra o aplicativo Docker Desktop e espere informar que o mecanismo está funcionando. Ele precisa continuar aberto durante a atividade. No Mac deste professor foi encontrado um comando Docker antigo, mas não o aplicativo Docker Desktop em Aplicativos; o Compose também estava indisponível. Instale ou reinstale o Docker Desktop antes de seguir.

### A2. Abrir um terminal na pasta correta

Extraia o ZIP antes de executar. Evite OneDrive/iCloud e pastas de rede se houver problemas de compartilhamento; prefira uma pasta local. Não execute diretamente de dentro do ZIP.

- **Windows:** abra a pasta no Explorador, clique na barra de endereço, digite `powershell` e pressione Enter.
- **Mac:** abra Terminal, digite `cd ` com um espaço, arraste a pasta extraída para a janela e pressione Enter.
- **Linux:** abra um terminal na pasta extraída pelo gerenciador de arquivos.

A pasta correta contém `compose.yaml`, `README.md` e a pasta `alunos`.

Confira:

```sh
docker info
docker compose version
```

Se `docker compose version` informar que compose não é um comando, instale ou reinstale o Docker Desktop. Se aparecer que não consegue conectar ao mecanismo, abra o Docker Desktop e aguarde. Não adianta repetir a construção antes de ele funcionar.

### A3. Preparar o ambiente

```sh
docker compose up -d --build
```

Este comando baixa o Ubuntu e instala o Gazebo **dentro do contêiner**. Na primeira vez demora mais. Aguarde voltar ao prompt sem mensagem de erro. Em dias posteriores, basta `docker compose up -d`.

Confira:

```sh
docker compose ps
docker compose exec sim gz sim --versions
docker compose exec sim /usr/bin/python3 -c "from gz.transport13 import Node; from gz.msgs10.laserscan_pb2 import LaserScan; print('Python e Gazebo disponíveis')"
```

O serviço `sim` deve estar em execução. A versão do Sim deve ser 8.x. O terceiro comando deve imprimir a mensagem final sem erro de importação.

### A4. Abrir a tela

Acesse [a tela local do ambiente](http://localhost:6080/vnc.html?autoconnect=true&resize=scale). Se necessário, clique em Connect. Inicialmente aparece uma área de trabalho simples; o Gazebo só abre no próximo guia.

O pacote usa a arquitetura nativa do computador: ARM64 em Macs Apple Silicon e AMD64 em computadores Intel/AMD. O repositório do Gazebo oferece os pacotes necessários para ambas as arquiteturas. A renderização é feita por software para evitar exigir repasse da placa gráfica. Isso precisa ser testado em cada perfil de máquina antes da aula; não há garantia de desempenho uniforme. A versão inicial forçava AMD64 e apresentou travamento da janela no Mac Apple Silicon; essa configuração foi corrigida.

O acesso da tela fica restrito ao próprio computador (`127.0.0.1`). A pasta extraída é compartilhada com o ambiente: edite `alunos/solucao.py` no seu editor habitual e salve; não é necessário reconstruir a imagem a cada edição.

## Opção B — Ubuntu 24.04 em computador Intel/AMD

É a alternativa com menos camadas e a primeira escolha para um laboratório Linux. A instalação direta deste pacote exige **Ubuntu 24.04 amd64**. Não execute o instalador no macOS, PowerShell, Ubuntu ARM ou outra distribuição.

No terminal, dentro da pasta do pacote:

```sh
bash scripts/instalar-ubuntu.sh
gz sim --versions
/usr/bin/python3 -c "from gz.transport13 import Node; print('Integração disponível')"
```

O instalador pedirá sua senha para instalar os pacotes. A senha não aparece enquanto você digita. Ele usa o repositório oficial do Gazebo; confira os comandos em `scripts/instalar-ubuntu.sh` se desejar.

Nesse caminho, substitua os comandos Docker do próximo guia por:

```sh
bash scripts/iniciar.sh
bash scripts/executar.sh
```

Cada comando deve ficar em seu próprio terminal. O Gazebo abre como aplicativo, sem navegador.

## Instalação nativa no Mac

A documentação do Harmonic fornece instalação por Homebrew com `brew tap osrf/simulation`, `brew trust osrf/simulation` e `brew install gz-harmonic`. Ela anuncia pacotes prontos para macOS Sequoia em Apple Silicon e descreve o servidor `gz sim -s`; em outras versões pode haver compilação longa. O Mac consultado usa macOS 26.6.2, fora dessa combinação anunciada. Por isso, **essa não é a rota principal deste pacote**. Os scripts de instalação e execução direta aqui são para Ubuntu; não presumem que os bindings Python do Homebrew estejam configurados.

## Se um computador não conseguir executar

Faça o piloto antes de atribuir nota. Primeiro tente Ubuntu nativo em uma máquina disponível. Se um grupo precisar usar um computador de colega, todos ainda devem participar da edição, dos experimentos e da explicação. Evite transformar problemas de instalação em critério de desempenho acadêmico.

No fim do trabalho com Docker:

```sh
docker compose down
```

Isso encerra o ambiente. Os arquivos de código e os resultados salvos na pasta permanecem no computador.
