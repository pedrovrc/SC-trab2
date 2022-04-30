import miller_rabin as MR
import eratosthenes_sieve as primes
import random
import hashlib

RANGE = 1000
SIZE_1 = 256
SIZE_2 = 512

def strXOR(str1, str2):
    str_final = ''
    for i in range(len(str1)):
        str_final += str(ord(str1[i]) ^ ord(str2[i]))  # bitwise XOR em cada caracter
    return str_final

# def xor(num1, num2):
#     # print(len(num1))
#     # print(len(num2))
#     # assert len(num1) == len(num2)
#     # return [a^b for a, b in zip(num1, num2)]

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

def oaep(msg, nonce):
    msg_bin =  ''.join(format(ord(i), '08b') for i in msg)
    padded_msg = msg_bin + padZeroes(SIZE_1 - len(msg_bin))
    hash_nonce = bin(int(hashlib.sha3_256(bin(nonce).encode('utf-8')).hexdigest(), 16))[2:]
    hash_nonce = padZeroes(SIZE_1 - len(hash_nonce)) + hash_nonce
    part1 = strXOR(padded_msg, hash_nonce)
    hash_part1 = bin(int(hashlib.sha3_512(bin(int(part1, 2)).encode('utf-8')).hexdigest(), 16))[2:]
    hash_part1 = padZeroes(SIZE_2 - len(hash_part1)) + hash_part1
    part2 = strXOR(bits2Str(bin(nonce)[2:], 'bin'), hash_part1)
    return part1 + part2

def encrypt(message, key):
    nonce = random.getrandbits(SIZE_2)
    padded = oaep(message, nonce)
    return pow(int(padded), key[0], key[1])

def decrypt(message, key):
    RSA_back = pow(message, key[0], key[1])
    RSA_back_bin = bin(RSA_back)[2:]
    RSA_back = padZeroes(SIZE_1 + SIZE_2 - len(RSA_back_bin)) + RSA_back_bin
    part1 = RSA_back[:SIZE_1]
    part2 = RSA_back[SIZE_1:]
    hashback_part1 = bin(int(hashlib.sha3_512(bin(int(part1,2)).encode('utf-8')).hexdigest(), 16))[2:]
    hashback_part1 = padZeroes(SIZE_2 - len(hashback_part1)) + hashback_part1
    nonce = strXOR(part2, hashback_part1)
    hashback_nonce = bin(int(hashlib.sha3_256(bin(int(nonce,2)).encode('utf-8')).hexdigest(), 16))[2:]
    hashback_nonce = padZeroes(SIZE_1 - len(hashback_nonce)) + hashback_nonce
    message_bits = strXOR(part1, hashback_nonce)
    return bits2Str(message_bits[:SIZE_1], 'char')

pk, sk = generateKeys()

print("Insira a mensagem:")
message = input()
print("Tamanho da mensagem inserida:", len(message))

encrypted_message = encrypt(message, pk)
print("Mensagem criptografada: ")
print(encrypted_message)

decrypted_message = decrypt(encrypted_message, sk)
print("Mensagem recuperada: ")
print(decrypted_message)
print("Tamanho da mensagem recuperada:", len(decrypted_message))

