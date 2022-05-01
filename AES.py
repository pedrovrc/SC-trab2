import numpy as np
import random

# VARIAVEIS AUXILIARES ---------------------------------------------------------------------------------------------
#   Variaveis globais feitas para armazenar dados extensos que sao parte do algoritmo da cifra de bloco AES. Foram
# criadas globalmente para não colocar declaracoes grandes no meio do codigo.


RCONTABLE = [[chr(1), chr(0), chr(0), chr(0)], [chr(2), chr(0), chr(0), chr(0)],
             [chr(4), chr(0), chr(0), chr(0)], [chr(8), chr(0), chr(0), chr(0)],
             [chr(16), chr(0), chr(0), chr(0)], [chr(32), chr(0), chr(0), chr(0)],
             [chr(64), chr(0), chr(0), chr(0)], [chr(128), chr(0), chr(0), chr(0)],
             [chr(27), chr(0), chr(0), chr(0)], [chr(54), chr(0), chr(0), chr(0)]]
BYTESTABLE = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
              [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
              [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
              [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
              [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
              [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
              [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
              [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
              [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
              [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
              [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
              [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
              [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
              [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
              [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
              [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]
GALOISMATRIX = np.array([[2, 3, 1, 1],
                         [1, 2, 3, 1],
                         [1, 1, 2, 3],
                         [3, 1, 1, 2]], dtype=np.int8)

NONCE = random.getrandbits(128)

# DEFINICOES ---------------------------------------------------------------------------------------------
#   Definicoes de tamanhos comumente usados. Criados para promover maior clareza no codigo e retirar
# numeros soltos.



# FUNCOES AUXILIARES ---------------------------------------------------------------------------------------------
#   Funcoes criadas para maior clareza e modularizacao do codigo. Sao tarefas que precisam ser executadas varias
# vezes, com tarefas relativamente simples e encapsulaveis.


# tamanho da string = 16 caracteres = 128 bits
def string2List(string):
    list = []
    for i in range(0, 16):
        list.append(string[i])
    return list

def list2String(list):
    string = ""
    for i in range(0, len(list)):
        string = string + list[i]
    return string

def int2String(number):
    string = ''
    while(number != 0):
        string += chr(number % 256)
        number = int(number/256)
    string = string[::-1]
    return string

def printKeys(keys):
    for i in range(len(keys)):
        print("[", end = '')
        for j in range(len(keys[i])):
            print(hex(ord(keys[i][j])), ", ", end = '')
        print("]")
    return

# listas de tamanhos iguais somente
def listXOR(str1, str2):
    str_final = []
    for i in range(len(str1)):
        str_final.append(chr(ord(str1[i]) ^ ord(str2[i])))  # bitwise XOR em cada caracter
    return str_final

# amount > 0 -> rotacao para a direita
# amount < 0 -> rotacao para a esquerda
def listRotate(list, amount):
    if list != []:
        list = list[amount:] + list[:amount]
    return list


# FUNCOES PRINCIPAIS ---------------------------------------------------------------------------------------------
#   Funcoes integrais para a logica do algoritmo da cifra de bloco AES e para o modo de operacao CTR.


#   Funcao generateRoundKeys:
# Funcao responsavel por gerar uma lista que contenha todas as chaves utilizadas na cifra de bloco AES.
def generateRoundKeys(key):
    round_keys = []
    round_keys.append(key)
    temp = []
    aux = []
    list_temp = []
    for i in range(10):
        for j in range(4):
            if j == 0:                                      # CASO INICIAL
                temp = round_keys[i][12:16]                         # amostrando 4 ultimas letras
                temp.append(temp.pop(0))                            # rotacao de coluna
                temp = subBytes(temp)                               # traducao pela tabela subBytes
                aux = listXOR(RCONTABLE[i], round_keys[i][0:4])      #
                list_temp = listXOR(temp, aux)                       # XOR com coluna da tabela Rcon e com 4 primeiras letras da ultima chave
            else:                                           # CASO INTERMEDIARIO
                temp = list_temp[j*4 - 4 : j*4]                     # amostrando 4 ultimas letras geradas
                aux = round_keys[i][j*4 : j*4 + 4]                  #
                temp = listXOR(temp, aux)                            # XOR com letras de 4 colunas à esquerda
                for k in range(4):
                    list_temp.append(temp[k])
        round_keys.append(list_temp)                # armazenando chave de rodada
    return round_keys

def addRoundKey(msg, round_key):
    temp = []
    for i in range(len(msg)):
        temp.append(chr(ord(msg[i]) ^ ord(round_key[i])))
    return temp

def subBytes(msg):
    msb = 0
    lsb = 0
    for i in range(len(msg)):
        msb = int((ord(msg[i]) & 240) / 16)     # 240 = 0b11110000
        lsb = ord(msg[i]) & 15                  # 15  = 0b00001111
        msg[i] = chr(BYTESTABLE[msb][lsb])
    return msg

def shiftRows(msg):
    new_row2 = listRotate([msg[1], msg[5], msg[9], msg[13]], 1)
    new_row3 = listRotate([msg[2], msg[6], msg[10], msg[14]], 2)
    new_row4 = listRotate([msg[3], msg[7], msg[11], msg[15]], 3)
    new_msg = []
    for i in range(4):
        new_msg.append(msg[4*i])
        new_msg.append(new_row2[i])
        new_msg.append(new_row3[i])
        new_msg.append(new_row4[i])
    return new_msg

def mixColumns(msg):
    ints = [int(ord(x)) for x in msg]
    new_ints = []
    for i in range(4):
        new_ints += np.matmul(GALOISMATRIX, np.array(ints[i : i+4], dtype=np.uint8)).tolist()
    return [chr(x) for x in new_ints]

# Tamanho da mensagem: 128 bits - 16 caracteres
def block_encryption(msg_in, key_in):

    msg = string2List(msg_in)
    key = string2List(key_in)

    round_keys = generateRoundKeys(key)
    msg = addRoundKey(msg, round_keys[0])
    for i in range(1, 10):
        msg = subBytes(msg)
        msg = shiftRows(msg)
        msg = mixColumns(msg)
        msg = addRoundKey(msg, round_keys[i])
    msg = subBytes(msg)
    msg = shiftRows(msg)
    msg = addRoundKey(msg, round_keys[10])

    msg_in = list2String(msg)
    key_in = list2String(key)

    return msg_in

def CTRmode(message, key):
    count = 0
    str_nonce = ''
    plaintext_block = ''
    cipher_block = ''
    final_message = ''

    for i in range(0, int(len(message)/16)):
        count = i
        str_nonce = int2String(NONCE + count)
        plaintext_block = message[i * 16: i * 16 + 16]
        cipher_block = block_encryption(str_nonce, key)
        final_message += list2String(listXOR(cipher_block, plaintext_block))
    
    remainder = len(message) % 16
    if remainder != 0:
        plaintext_block = message[len(message) - remainder:]
        count += 1
        str_nonce = int2String(NONCE + count)
        cipher_block = block_encryption(str_nonce, key)
        for i in range(16 - remainder):
            plaintext_block += '0'
        final_message += list2String(listXOR(cipher_block, plaintext_block)[:remainder])

    return final_message
