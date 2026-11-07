#!/usr/bin/env bash
set -euo pipefail
export GZ_PARTITION=estacionamento01
gz topic -t /desafio/cmd_vel -m gz.msgs.Twist -p 'linear: {x: 0}'
