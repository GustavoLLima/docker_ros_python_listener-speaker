# codigo_gustavo
Teste para criar um pacote ros2 com listener/speaker em Python.

Os testes foram feitos utilizando o ros2 na distribuição `foxy`.

Para funcionar, é necessários criar 2 arquivos, `Dockerfile` e `docker-compose.yml`.

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

Tendo criado os 2 arquivos no mesmo diretório, basta rodar:
```
docker-compose up -d
```

## Referências
Código utilizado como base para a criação do listener/speaker em Python, em conjunto com a criação do pacote no ros2: https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Publisher-And-Subscriber/

Criação do ROS como um Docker Container: https://hub.docker.com/_/ros
