"""Infraestrutura do professor: sensor, comando e relatório de uma tentativa."""
import argparse
import csv
import importlib.util
import json
import math
from pathlib import Path
import signal
import threading
import time

from gz.transport13 import Node
from gz.msgs10.laserscan_pb2 import LaserScan
from gz.msgs10.twist_pb2 import Twist
from gz.msgs10.contacts_pb2 import Contacts
from gz.msgs10.odometry_pb2 import Odometry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solucao', default='alunos/solucao.py')
    parser.add_argument('--saida', default='resultados/tentativa')
    parser.add_argument('--limite', type=float, default=45.0,
                        help='Limite em segundos de simulação')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('solucao_grupo', args.solucao)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    decidir = modulo.decidir_velocidade
    node = Node()
    pub = node.advertise('/desafio/cmd_vel', Twist)
    lock = threading.Lock()
    dados = dict(t=None, d=None, recebido=0.0, colisao=False,
                 v=None, odom_recebida=0.0, seq=0)
    interromper = threading.Event()
    signal.signal(signal.SIGINT, lambda *_: interromper.set())
    signal.signal(signal.SIGTERM, lambda *_: interromper.set())

    def scan(msg):
        valores = [r for r in msg.ranges if math.isfinite(r) and r >= msg.range_min]
        with lock:
            dados.update(t=msg.header.stamp.sec + msg.header.stamp.nsec * 1e-9,
                         d=min(valores) if valores else None,
                         recebido=time.monotonic(), seq=dados['seq'] + 1)

    def contato(msg):
        if len(msg.contact):
            with lock:
                dados['colisao'] = True

    def odometria(msg):
        with lock:
            dados['v'] = abs(msg.twist.linear.x)
            dados['odom_recebida'] = time.monotonic()

    for tipo, topico, callback in [
        (LaserScan, '/desafio/scan', scan),
        (Contacts, '/desafio/contato', contato),
        (Odometry, '/desafio/odom', odometria),
    ]:
        if not node.subscribe(tipo, topico, callback):
            raise RuntimeError('Não foi possível assinar ' + topico)

    def mover(v):
        msg = Twist()
        msg.linear.x = v
        pub.publish(msg)

    base = Path(args.saida)
    base.parent.mkdir(parents=True, exist_ok=True)
    inicio = None
    estavel = None
    ultimo_seq = -1
    status = 'interrompido'
    erro = None
    distancia_final = None
    decorrido = 0.0
    print('Aguardando sensor e odometria. O Gazebo deve estar em Play.', flush=True)
    espera = time.monotonic()
    try:
        with base.with_suffix('.csv').open('w', newline='') as arquivo:
            gravar = csv.writer(arquivo)
            gravar.writerow(['tempo_sim_s', 'distancia_m', 'comando_m_s', 'velocidade_odom_m_s'])
            while not interromper.is_set():
                with lock:
                    atual = dados.copy()
                agora = time.monotonic()
                if atual['colisao']:
                    status = 'colisao'
                    break
                if atual['t'] is None or atual['v'] is None:
                    mover(0.0)
                    if agora - espera > 30:
                        status = 'sem_sensor_ou_odometria'
                        break
                    time.sleep(0.02)
                    continue
                if (agora - atual['recebido'] > 3 or
                        agora - atual['odom_recebida'] > 3):
                    status = 'sensor_ou_simulacao_sem_atualizacao'
                    break
                if atual['seq'] == ultimo_seq:
                    time.sleep(0.01)
                    continue
                ultimo_seq = atual['seq']
                t, d = atual['t'], atual['d']
                if inicio is None:
                    inicio = t
                if t < inicio or t - inicio < decorrido - 0.2:
                    status = 'simulacao_reiniciada'
                    break
                decorrido = t - inicio
                distancia_final = d
                if d is None:
                    status = 'leitura_invalida'
                    break
                if decorrido >= args.limite:
                    status = 'tempo_esgotado'
                    break
                v = decidir(d)
                if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 0.5:
                    raise ValueError('A função deve retornar um número finito entre 0 e 0.5.')
                mover(float(v))
                gravar.writerow([round(decorrido, 4), d, v, atual['v']])
                if 0.27 <= d <= 0.33 and atual['v'] <= 0.01 and v == 0:
                    if estavel is None:
                        estavel = t
                    if t - estavel >= 2:
                        status = 'sucesso'
                        break
                else:
                    estavel = None
    except Exception as exc:
        status = 'erro_na_execucao'
        erro = str(exc)
    finally:
        # Repetir o comando ajuda a entregá-lo antes de encerrar o transporte.
        for _ in range(10):
            mover(0.0)
            time.sleep(0.03)
        with lock:
            colisao = dados['colisao']
        if colisao:
            status = 'colisao'
        relatorio = dict(status=status, tempo_sim_s=round(decorrido, 4),
                         distancia_final_m=distancia_final, colisao=colisao,
                         solucao=args.solucao, erro=erro)
        base.with_suffix('.json').write_text(
            json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(relatorio, ensure_ascii=False, indent=2), flush=True)
    return 0 if status == 'sucesso' else 1


if __name__ == '__main__':
    raise SystemExit(main())
