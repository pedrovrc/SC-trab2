import math

LIMIT = 2000

# numeros com 1024 bits de tamanho
# ou seja, numeros maiores ou iguais a 2^1023,
# aproximadamente 9 * 10^307, 308 digitos

def isEven(number):
    if number % 2 == 0:
        return True
    else:
        return False

def isPrime(number):
    # Miller-Rabin
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
            
# main
print(isPrime(int(input())))