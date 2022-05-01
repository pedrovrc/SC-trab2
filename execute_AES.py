# Este modulo deve ser utilizado para testar isoladamente as funcionalidades do modulo "AES.py".

import AES

# FUNCOES AUXILIARES --------------------------------------------------------------------------------------------------------------------
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


# ROTINA PRINCIPAL --------------------------------------------------------------------------------------------------------------------
key = "CHAVE_AES_CTR_128"
message = "The quick brown fox jumps over the lazy dog."
print("\n-----------------------------------------------------------------------------------------------------------------------------")
print("MENSAGEM:\t\t", message)
print("-----------------------------------------------------------------------------------------------------------------------------")

encrypted = AES.CTRmode(message, key)
print("MENSAGEM CIFRADA (HEX):\t", str2Hex(encrypted))
print("-----------------------------------------------------------------------------------------------------------------------------")
print("MENSAGEM RECUPERADA:\t", AES.CTRmode(encrypted, key))
print("-----------------------------------------------------------------------------------------------------------------------------\n")