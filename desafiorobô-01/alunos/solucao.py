"""Edite somente este arquivo. Distância em metros; velocidade em m/s."""


def decidir_velocidade(distancia):
    """Recebe a distância entre a frente do robô e a parede.

    Retorne um número de 0.0 a 0.5. Zero significa parar.
    Meta: parar entre 0.27 e 0.33 m e permanecer parado por 2 s.
    Use a distância recebida; não use contagem de tempo ou posição fixa.
    """
    # TODO: substitua pela estratégia do grupo.
    
    if distancia > 0.40:
        return 0.4
    else:
        return 0.0
