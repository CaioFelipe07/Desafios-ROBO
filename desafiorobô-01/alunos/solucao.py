"""Edite somente este arquivo. Distância em metros; velocidade em m/s."""


def decidir_velocidade(distancia):
    """Recebe a distância entre a frente do robô e a parede.

    Retorne um número de 0.0 a 0.5. Zero significa parar.
    Meta: parar entre 0.27 e 0.33 m e permanecer parado por 2 s.
    Use a distância recebida; não use contagem de tempo ou posição fixa.
    """
    # A referência fica no limite superior da faixa aceita. O pequeno avanço
    # residual durante a frenagem leva o robô para dentro da faixa.
    distancia_de_parada = 0.33

    if distancia <= distancia_de_parada:
        return 0.0

    # Para parar em uma distância s com desaceleração a, vale v² = 2*a*s.
    # Usamos a = 0,2 m/s² para
    # começar a frear cedo.  Longe da parede, a velocidade continua no máximo
    # permitido e o percurso é feito rapidamente.
    velocidade = (0.4 * (distancia - distancia_de_parada)) ** 0.5
    return min(0.5, velocidade)
