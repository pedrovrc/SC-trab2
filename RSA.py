import miller_rabin as MR
import eratosthenes_sieve as primes
import random
import hashlib

RANGE = 20

def areCoprime(num1, num2):
    for i in range(2, num1+1):
        if num1 % i == 0 and num2 % i == 0:
            return False
    return True

def keyGeneration():
    # UTILIZANDO MILLER-RABIN --------------------------------
    # Escolher 2 primos p e q
    # P = MR.getPrimeCandidate(MR.KEY_LEN)
    # while(not(MR.isPrime(P))):
    #     P = MR.getPrimeCandidate(MR.KEY_LEN)

    # while(True):
    #     Q = MR.getPrimeCandidate(MR.KEY_LEN)
    #     if MR.isPrime(Q) and Q != P:
    #         break
    # --------------------------------------------------------

    # UTILIZANDO CRIVO DE ERASTOTENES ------------------------
    # Escolher 2 primos p e q
    prime_list = primes.generateList(RANGE)
    P = prime_list[random.randrange(0, len(prime_list))]
    Q = prime_list[random.randrange(0, len(prime_list))]
    while Q == P:
        Q = prime_list[random.randrange(0, len(prime_list))]
    print("Primos: ", P, Q)

    # Gerar N = p * q
    # Computar phi(N) = (p-1) * (q-1)
    N = P * Q
    phi_N = (P-1) * (Q-1)
    print("N, phi_N: ", N, phi_N)

    # Escolher E tal que: 1 < E < phi(N); E é coprimo com N e phi(N)
    E = phi_N - 1
    while(True):
        if E == 1:
            print("ERRO!")
            print("Chaves não puderam ser geradas.")
            break
        elif areCoprime(E, N) and areCoprime(E, phi_N):
            break
        else:
            E -= 1

    # Escolher D tal que: D*E(mod phi(N)) = 1
    D = 5*(E+1)
    while (D*E) % phi_N != 1:
        D += 1

    if D == E:
        print("ERRO 2!")
        print("Chaves não puderam ser geradas.")

    PK = (E, N)     # Chave publica = (E, N)
    SK = (D, N)     # Chave privada = (D, N)

    if E != 1 and D != E:
        print("Chave Pública: (E, N) =", PK)
        print("Chave Secreta: (D, N) =", SK)

    return PK, SK