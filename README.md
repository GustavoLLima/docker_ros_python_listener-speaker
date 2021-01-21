# codigo_gustavo
## Descrição
Teste para criar um pacote ros2 com listener/speaker em Python.

Os testes foram feitos utilizando o ros2 na distribuição `foxy`.

## Instalação

###### Instalação com Docker
É necessário ter o Docker instalado. O Docker está disponível para Windows, Linux e iOS. Disponível em: https://www.docker.com/products/docker-desktop

Uma vez que o Docker esteja instalado, crie um diretório e dentro dele 2 arquivos, `Dockerfile` e `docker-compose.yml`.

Conteúdo do arquivo `docker-compose.yml`:
```
version: '3'

services:
  talker:
    build: ./
    command: ros2 run codigo_gustavo talker

  listener:
    build: ./
    environment:
      - "PYTHONUNBUFFERED=1"
    volumes:
      - ./teste:/teste
    command: ros2 run codigo_gustavo listener
    deploy:
      mode: replicated
      replicas: 2

volumes:
  teste:
```
Observação: este arquivo utiliza um volume `teste`, que trata de uma pasta sincronizada entre o pc que executa o Docker e o container criado. A pasta `/teste/` está no mesmo nível dos arquivos `Dockerfile` e `docker-compose.yml`, e a pasta equivalente no container estará em `/root/teste`. Além disso, está sendo utilizada duas réplicas do serviço `listener`. Todos os parâmetros dessa descrição são opcionais, e podem ser removidos do `docker-compose.yml` sem alterar o funcionamento principal.

Conteúdo do arquivo `Dockerfile`:
```
ARG FROM_IMAGE=ros:foxy
ARG OVERLAY_WS=/opt/ros/overlay_ws

# multi-stage for caching
FROM $FROM_IMAGE AS cacher

# clone overlay source
ARG OVERLAY_WS
WORKDIR $OVERLAY_WS/src
RUN echo "\
repositories: \n\
  ros2/codigo_gustavo: \n\
    type: git \n\
    url: https://github.com/GustavoLLima/codigo_gustavo.git \n\
    version: master \n\
" > ../overlay.repos
RUN vcs import ./ < ../overlay.repos

# copy manifests for caching
WORKDIR /opt
RUN mkdir -p /tmp/opt && \
    find ./ -name "package.xml" | \
      xargs cp --parents -t /tmp/opt && \
    find ./ -name "COLCON_IGNORE" | \
      xargs cp --parents -t /tmp/opt || true

# multi-stage for building
FROM $FROM_IMAGE AS builder

# install overlay dependencies
ARG OVERLAY_WS
WORKDIR $OVERLAY_WS
COPY --from=cacher /tmp/$OVERLAY_WS/src ./src
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    apt-get update && rosdep install -y \
      --from-paths \
        src \
      --rosdistro \
        foxy \
    && rm -rf /var/lib/apt/lists/*

# build overlay source
COPY --from=cacher $OVERLAY_WS/src ./src
ARG OVERLAY_MIXINS="release"
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    colcon build \
      --packages-select \
        codigo_gustavo \
      --mixin $OVERLAY_MIXINS

# source entrypoint setup
ENV OVERLAY_WS $OVERLAY_WS
RUN sed --in-place --expression \
      '$isource "$OVERLAY_WS/install/setup.bash"' \
      /ros_entrypoint.sh
```

Tendo criado os 2 arquivos no mesmo diretório, abra um terminal/prompt de comando, navegue até o diretório, e execute:
```
docker-compose up -d
```
###### Instalação como um pacote ros2 normal
Crie um diretório, baixe o arquivo principal e faça importação pelo `vcs`
```
mkdir -p ~/my_ws/src
cd ~/my_ws
wget https://raw.githubusercontent.com/GustavoLLima/codigo_gustavo/master/file_for_raw

vcs import src < file_for_raw
```

Indique o source (atenção, pode variar conforme a distribuição do ROS):
```
cd ~/my_ws
source /opt/ros/foxy/setup.bash (varia conforme a distro)
```
Instale as dependências e monte o pacote
```
rosdep install -i --from-path src --rosdistro foxy -y
colcon build --packages-select codigo_gustavo
```

Em outro terminal, execute o setup:
```
/bin/bash
cd ~/my_ws
source /opt/ros/foxy/setup.bash (varia conforme a distro)
. install/setup.bash
```

Por fim, teste o pacote através do talker:
```
ros2 run codigo_gustavo talker
```

Ou então, crie um novo terminal, execute novamente os passos do setup e, por fim, execute o listener:
```
ros2 run codigo_gustavo listener
```

## Referências
Código utilizado como base para a criação do listener/speaker em Python, em conjunto com a criação do pacote no ros2: https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Publisher-And-Subscriber/

Criação do ROS como um Docker Container: https://hub.docker.com/_/ros
