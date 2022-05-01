import miller_rabin as MR
import eratosthenes_sieve as primes
import random
import hashlib

RANGE = 2000
SIZE_1 = 256
SIZE_2 = 512

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def strXOR(str1, str2):
    if len(str1) > len(str2):
        str2 = padZeroes(len(str1) - len(str2)) + str2
    elif len(str2) > len(str1):
        str1 = padZeroes(len(str2) - len(str1)) + str1
    str_final = ''
    for i in range(len(str1)):
        str_final += str(ord(str1[i]) ^ ord(str2[i]))  # bitwise XOR em cada caracter
    return str_final

def areCoprime(num1, num2):
    for i in range(2, num1+1):
        if num1 % i == 0 and num2 % i == 0:
            return False
    return True

def padZeroes(num):
    str = ''
    for i in range(0, num):
        str += '0'
    return str

def bits2Str(bits, arg):
    string = ''
    for i in range(0, len(bits), 8):
        temp = bits[i : i+8]
        if arg == 'char':
            temp_decimal = int(temp, 2)
            string += chr(temp_decimal)
        elif arg == 'bin':
            string += str(temp)
        else:
            print("ERRO! bits2Str")
    return string

def bitsFromHash(hash_obj):
    list = [bin(int(x,16))[2:] for x in hash_obj.hexdigest()]
    str = ''
    for i in range(0, len(list)):
        if len(list[i]) < 4:
            list[i] = padZeroes(4 - len(list[i])) + list[i]
        str += list[i]
    return str

def generateKeys():
    # UTILIZANDO MILLER-RABIN --------------------------------
    # Escolher 2 primos p e q
    # P = MR.getPrimeCandidate(RANGE)
    # while(not(MR.isPrime(P))):
    #     P = MR.getPrimeCandidate(RANGE)

    # while(True):
    #     Q = MR.getPrimeCandidate(RANGE)
    #     if MR.isPrime(Q) and Q != P:
    #         break
    # --------------------------------------------------------

    # UTILIZANDO CRIVO DE ERASTOTENES ------------------------
    # Escolher 2 primos p e q
    prime_list = primes.generateList(RANGE)
    P = prime_list[random.randrange(int(len(prime_list)/2), len(prime_list))]
    Q = prime_list[random.randrange(int(len(prime_list)/2), len(prime_list))]
    while Q == P:
        Q = prime_list[random.randrange(0, len(prime_list))]

    # Gerar N = p * q
    # Computar phi(N) = (p-1) * (q-1)
    N = P * Q
    phi_N = (P-1) * (Q-1)

    # Escolher E tal que: 1 < E < phi(N); E é coprimo com N e phi(N)
    E = phi_N - 1
    while(True):
        if areCoprime(E, N) and areCoprime(E, phi_N):
            break
        else:
            E -= 1

    # Escolher D tal que: D*E(mod phi(N)) = 1
    D = 5*(E+1)
    while (D*E) % phi_N != 1:
        D += 1

    PK = (E, N)     # Chave publica = (E, N)
    SK = (D, N)     # Chave privada = (D, N)
    return PK, SK

def oaep(msg, nonce):
    msg_bin =  ''.join(format(ord(i), '08b') for i in msg)
    padded_msg = msg_bin + padZeroes(SIZE_1 - len(msg_bin))

    hash_nonce = int(hashlib.sha3_256(bitstring_to_bytes(nonce)).hexdigest(), 16)
    hash_nonce = format(hash_nonce, '0>256b')
    part1 = strXOR(padded_msg, hash_nonce)

    hash_part1 = int(hashlib.sha3_512(bitstring_to_bytes(part1)).hexdigest(), 16)
    hash_part1 = format(hash_part1, '0>512b')
    part2 = strXOR(nonce, hash_part1)

    return part1 + part2

def encrypt(message, key):
    nonce = bin(random.getrandbits(SIZE_2))[2:]
    padded = oaep(message, nonce)
    return pow(int(padded, 2), key[0], key[1])

def reverse_oaep(part1, part2):
    hashback_part1 = int(hashlib.sha3_512(bitstring_to_bytes(part1)).hexdigest(), 16)
    hashback_part1 = format(hashback_part1, '0>512b')
    nonce = strXOR(part2, hashback_part1)

    hashback_nonce = int(hashlib.sha3_256(bitstring_to_bytes(nonce)).hexdigest(), 16)
    hashback_nonce = format(hashback_nonce, '0>256b')
    message_bits = strXOR(part1, hashback_nonce)
    return bits2Str(message_bits[:SIZE_1], 'char')

def decrypt(message, key):
    RSA_back = pow(message, key[0], key[1])

    RSA_back_bin = bin(RSA_back)[2:]
    RSA_back = padZeroes(SIZE_1 + SIZE_2 - len(RSA_back_bin)) + RSA_back_bin
    part1 = RSA_back[:SIZE_1]
    part2 = RSA_back[SIZE_1:]
    return reverse_oaep(part1, part2)

def decrypt_hash(message, key):
    RSA_back = pow(message, key[0], key[1])

    RSA_back_bin = bin(RSA_back)[2:]
    RSA_back = padZeroes(SIZE_1 + SIZE_2 - len(RSA_back_bin)) + RSA_back_bin
    part1 = RSA_back[:SIZE_1]
    part2 = RSA_back[SIZE_1:]

    hashback_part1 = int(hashlib.sha3_512(bitstring_to_bytes(part1)).hexdigest(), 16)
    hashback_part1 = format(hashback_part1, '0>512b')
    nonce = strXOR(part2, hashback_part1)
    return RSA_back, nonce
