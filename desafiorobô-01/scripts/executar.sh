#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export GZ_PARTITION=estacionamento01
exec /usr/bin/python3 infra/executar.py "$@"
