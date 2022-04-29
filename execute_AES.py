import AES

# ROTINA PRINCIPAL ---------------------------------------------------------------------------------------------
#   Rotina que cuida da recepcao de inputs e entrega de outputs para um usuario. Feita para iniciar a execucao
# do algoritmo em questao.

print("Insira a chave de cifracao (16 caracteres)")
key = input()

print("Insira a mensagem a ser cifrada:")
message = input()

print("Entradas:")
print("Mensagem, texto:", message)
print("Mensagem, binario:", end = ' ')
for i in range(len(message)):
    print(bin(ord(message[i]))[2:], '|', end = '')
print("\nChave:", key)

encrypted_message = AES.CTRmode(message, key)

print("Saida:")
print("Mensagem:", encrypted_message)
print("Mensagem, binario:", end = ' ')
for i in range(len(encrypted_message)):
    print(hex(ord(encrypted_message[i]))[2:], '|', end = '')
