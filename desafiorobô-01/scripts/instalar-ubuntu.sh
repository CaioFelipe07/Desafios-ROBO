#!/usr/bin/env bash
set -euo pipefail
. /etc/os-release
if [[ "${ID:-}" != ubuntu || "${VERSION_ID:-}" != 24.04 || "$(dpkg --print-architecture)" != amd64 ]]; then
  echo 'Este instalador exige Ubuntu 24.04 amd64. Consulte docs/01-instalacao.md.' >&2
  exit 1
fi
sudo apt-get update
sudo apt-get install -y curl ca-certificates gnupg lsb-release
sudo curl -fsSL https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable noble main' | sudo tee /etc/apt/sources.list.d/gazebo-stable.list >/dev/null
sudo apt-get update
sudo apt-get install -y gz-harmonic python3-gz-transport13 python3-gz-msgs10
echo 'Instalação concluída. Leia docs/02-primeira-execucao.md.'
