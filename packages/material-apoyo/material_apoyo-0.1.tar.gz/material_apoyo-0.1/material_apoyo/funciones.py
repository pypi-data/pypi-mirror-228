import random

def revisar_alarma(hora, minuto):
    seed = str(hora) + str(minuto)
    random.seed(int(seed))

    return random.choice([True, False, False, False])