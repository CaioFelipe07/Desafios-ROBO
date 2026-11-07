FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg lsb-release \
    && curl -fsSL https://packages.osrfoundation.org/gazebo.gpg -o /usr/share/keyrings/gazebo.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/gazebo.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable noble main" > /etc/apt/sources.list.d/gazebo.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    gz-harmonic python3-gz-transport13 python3-gz-msgs10 \
    xvfb x11vnc novnc websockify fluxbox xterm x11-utils \
    libgl1-mesa-dri libglx-mesa0 mesa-utils fonts-dejavu-core dbus-x11 \
    && rm -rf /var/lib/apt/lists/*
ENV DISPLAY=:1 LIBGL_ALWAYS_SOFTWARE=1 QT_X11_NO_MITSHM=1
ENV GZ_PARTITION=estacionamento01
WORKDIR /atividade
COPY infra/desktop.sh /usr/local/bin/desktop.sh
EXPOSE 6080
CMD ["bash", "/usr/local/bin/desktop.sh"]
