import miller_rabin as MR
import eratosthenes_sieve as primes
import random
import hashlib

# VARIAVEIS AUXILIARES ------------------------------------------------------------------------------
#   Variaveis que sao mais convenientes de serem utilizadas como globais.

RANGE = 2000                    # Tamanho maximo dos primos gerados na geracao de chaves
SIZE_1 = 256                    # Representa 256 bits, usado para padding
SIZE_2 = 512                    # Representa 512 bits, usado para padding
MODE = 'Erastothenes Sieve'     # Modo de geracao de primos escolhido.
                                # Valores aceitos:
                                    # Erastothenes Sieve
                                    # Miller-Rabin

# FUNCOES AUXILIARES ------------------------------------------------------------------------------
#   Funcoes que executam tarefas que sao requisitadas com frequencia dentro das funcoes principais.

#   Transforma uma string com caracteres '0' e '1' para um tipo bytes.
def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

#   Retorna uma string contendo uma quantidade 'num' de caracteres '0'.
def padZeroes(num):
    str = ''
    for i in range(0, num):
        str += '0'
    return str

#   Realiza XOR por cada caracter de uma string. Nos casos de uso aqui presentes,
# as strings contem somente os caracteres '0' e '1'. Realiza padding para strings
# com tamanhos diferentes.
#   Retorna uma string com caracteres '0' e '1' com o resultado da operacao.
def strXOR(str1, str2):
    if len(str1) > len(str2):
        str2 = padZeroes(len(str1) - len(str2)) + str2
    elif len(str2) > len(str1):
        str1 = padZeroes(len(str2) - len(str1)) + str1
    str_final = ''
    for i in range(len(str1)):
        str_final += str(ord(str1[i]) ^ ord(str2[i]))
    return str_final

#   Verifica coprimalidade de dois inteiros. Dois numeros sao coprimos quando o
# maior divisor comum entre eles e 1.
def areCoprime(num1, num2):
    for i in range(2, num1+1):
        if num1 % i == 0 and num2 % i == 0:
            return False
    return True

#   Recebe uma string de bits e um argumento que determina o retorno.
#   Retorno:
#       arg = 'char':   Retorna uma string com a interpretacao ascii
#                       de cada byte da string original.
#       arg = 'bin':    Retorna uma string com os caracteres '0' e '1'
#                       assim como a string original.
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

#   Retorna uma string de caracteres '0' e '1' do digest de um objeto hash.
def bitsFromHash(hash_obj):
    list = [bin(int(x,16))[2:] for x in hash_obj.hexdigest()]
    str = ''
    for i in range(0, len(list)):
        if len(list[i]) < 4:
            list[i] = padZeroes(4 - len(list[i])) + list[i]
        str += list[i]
    return str


# FUNCOES PRINCIPAIS ------------------------------------------------------------------------------
#   Funcoes que sao essenciais para a logica e o funcionamento do algoritmo RSA com OAEP e SHA3.

#   Gera primos dado um tamanho maximo definido globalmente para gerar chaves para o
# algoritmo RSA. Retorna ambas as chaves geradas.
#   Ha a possibilidade de utilizar tanto o teste de primalidade de Miller-Rabin quanto
# o Crivo de Erastotenes para gerar os primos.
def generateKeys():
    if MODE == 'Miller-Rabin':
        # UTILIZANDO MILLER-RABIN --------------------------------
        # Escolher 2 primos p e q
        P = MR.getPrimeCandidate(RANGE)
        while(not(MR.isPrime(P))):
            P = MR.getPrimeCandidate(RANGE)

        while(True):
            Q = MR.getPrimeCandidate(RANGE)
            if MR.isPrime(Q) and Q != P:
                break
    elif MODE == 'Erastothenes Sieve':
        # UTILIZANDO CRIVO DE ERASTOTENES ------------------------
        # Escolher 2 primos p e q
        prime_list = primes.generateList(RANGE)
        P = prime_list[random.randrange(int(len(prime_list)/2), len(prime_list))]
        Q = prime_list[random.randrange(int(len(prime_list)/2), len(prime_list))]
        while Q == P:
            Q = prime_list[random.randrange(0, len(prime_list))]
    else: print("ERRO! generateKeys")

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

#   Realiza padding de acordo com o padrao OAEP.
def oaep(msg, nonce):
    # Padding inicial da mensagem para 256 bits
    msg_bin =  ''.join(format(ord(i), '08b') for i in msg)
    padded_msg = msg_bin + padZeroes(SIZE_1 - len(msg_bin))

    # Calculo do hash do Nonce, retorno em hexadecimal
    hash_nonce = int(hashlib.sha3_256(bitstring_to_bytes(nonce)).hexdigest(), 16)
    # Conversao para string de bits
    hash_nonce = format(hash_nonce, '0>256b')
    # Executa o XOR da mensagem com o hash do nonce
    part1 = strXOR(padded_msg, hash_nonce)

    # Calculo do hash da parte 1, retorno em hexadecimal
    hash_part1 = int(hashlib.sha3_512(bitstring_to_bytes(part1)).hexdigest(), 16)
    # Conversao para string de bits
    hash_part1 = format(hash_part1, '0>512b')
    # Executa o XOR do nonce com o hash da parte 1
    part2 = strXOR(nonce, hash_part1)

    # Retorno da concatenacao de parte 1 e parte 2
    return part1 + part2

#   Gera nonce, utiliza OAEP e retorna encriptacao RSA.
def encrypt(message, key):
    nonce = bin(random.getrandbits(SIZE_2))[2:]
    padded = oaep(message, nonce)
    return pow(int(padded, 2), key[0], key[1])

#   Realiza o processo inverso do padrao OAEP.
def reverse_oaep(message):
    # Separacao das partes da mensagem recebida
    part1 = message[:SIZE_1]
    part2 = message[SIZE_1:]

    # Calculo do hash da parte 1, retorno em hexadecimal
    hashback_part1 = int(hashlib.sha3_512(bitstring_to_bytes(part1)).hexdigest(), 16)
    # Conversao para string de bits
    hashback_part1 = format(hashback_part1, '0>512b')
    # Nonce obtido pelo XOR da parte 2 com o hash da parte 1
    nonce = strXOR(part2, hashback_part1)

    # Calculo do hash do nonce, retorno em hexadecimal
    hashback_nonce = int(hashlib.sha3_256(bitstring_to_bytes(nonce)).hexdigest(), 16)
    # Conversao para string de bits
    hashback_nonce = format(hashback_nonce, '0>256b')
    # Mensagem obtida pelo XOR da parte 1 com o hash do nonce
    message_bits = strXOR(part1, hashback_nonce)

    # Retorna string de caracteres da mensagem
    return bits2Str(message_bits[:SIZE_1], 'char')

#   Obtem a mensagem do RSA e reverte o processo OAEP.
def decrypt(message, key):
    RSA_back = pow(message, key[0], key[1])

    RSA_back_bin = bin(RSA_back)[2:]
    RSA_back = padZeroes(SIZE_1 + SIZE_2 - len(RSA_back_bin)) + RSA_back_bin
    return reverse_oaep(RSA_back)

#   Retorna a mensagem obtida pelo RSA e o Nonce encontrado.
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
