# Implementacao do teste de primalidade de Miller-Rabin

import random

LIMIT = 2000

def isEven(number):
    if number % 2 == 0:
        return True
    else:
        return False

def isPrime(number):
    # Teste de primalidade de Miller-Rabin
    number_alt = number - 1
    power = 0
    while (isEven(number_alt)):
        power += 1
        number_alt = int(number_alt / 2)
    
    remainder = int((number - 1)/(pow(2, power)))
    base = 2

    check = int((pow(base, remainder)) % number)
    if check == 1:
        return False
    elif check == number - 1:
        return True
    else:
        for i in range(LIMIT):
            check = int((pow(check, 2)) % number)
            if check == 1:
                return False
            elif check == number - 1:
                return True

        return False

def set_bit(value, bit):
    return value | (1<<bit)

def getPrimeCandidate(length):
    # Gera numero aleatorio de tamanho desejado
    num = random.getrandbits(length)

    # Setar bits para garantir que o numero seja impar e grande o suficiente
    num = set_bit(num, 0)
    num = set_bit(num, length - 1)
    return num
