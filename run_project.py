import RSA
import AES

def list2HexString(list):
    string = ""
    for i in range(0, len(list)):
        string = string + str(hex(list[i]))[2:]
    return string

def str2Hex(string):
    ascii_values = []
    for character in string:
        ascii_values.append(ord(character))
    return list2HexString(ascii_values)

# SENDER -----------------------------------------------
def send(pk, enc_msg, enc_key, enc_hash):
    print("Enviando dados...")
    return

pk, sk = RSA.generateKeys()
AES_key = "CHAVE_AES_CTR_128"
message = "Sample Text"
print("\n-----------------------------------------------------------------------------------------------------------------------------")
print("CHAVES RSA (PK, SK):\t", pk, sk)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("CHAVE AES:\t\t", AES_key)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("MENSAGEM:\t\t", message)
print("-----------------------------------------------------------------------------------------------------------------------------")

encrypted_msg = AES.CTRmode(message, AES_key)
encrypted_key = RSA.encrypt(AES_key, sk)
encrypted_hash = RSA.encrypt(message, sk)
print("MENSAGEM CIFRADA (HEX):\t", str2Hex(encrypted_msg))
print("-----------------------------------------------------------------------------------------------------------------------------")
print("CHAVE CIFRADA (HEX):\t", hex(encrypted_key)[2:])
print("-----------------------------------------------------------------------------------------------------------------------------")
print("HASH CIFRADO (HEX):\t", hex(encrypted_hash)[2:])
print("-----------------------------------------------------------------------------------------------------------------------------\n")

send(pk, encrypted_msg, encrypted_key, encrypted_hash)

# RECEIVER ----------------------------------------------
recov_AES_key = RSA.decrypt(encrypted_key, pk)
recov_msg = AES.CTRmode(encrypted_msg, recov_AES_key)
recov_hash, recov_nonce = RSA.decrypt_hash(encrypted_hash, pk)
new_hash = RSA.oaep(recov_msg, recov_nonce)
print("\n-----------------------------------------------------------------------------------------------------------------------------")
print("CHAVE RECUPERADA (HEX)\t:", str2Hex(recov_AES_key))
print("-----------------------------------------------------------------------------------------------------------------------------")
print("MENSAGEM RECUPERADA: (HEX)\t", str2Hex(recov_msg))
print("-----------------------------------------------------------------------------------------------------------------------------")
print("HASH RECUPERADO: (HEX)\t", hex(int(recov_hash,2))[2:])
print("-----------------------------------------------------------------------------------------------------------------------------")
print("HASH CALCULADO: (HEX)\t", hex(int(new_hash,2))[2:])
print("-----------------------------------------------------------------------------------------------------------------------------\n")

if new_hash == recov_hash:
    print("Assinatura confirmada.")
else:
    print("Assinatura inválida.")