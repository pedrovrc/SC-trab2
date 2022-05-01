# Este modulo deve ser utilizado para testar isoladamente as funcionalidades do modulo "RSA.py".

import RSA

pk, sk = RSA.generateKeys()

print("Insira a mensagem:")
message = input()

encrypted_message = RSA.encrypt(message, pk)
print("Mensagem criptografada: ")
print(encrypted_message)

decrypted_message = RSA.decrypt(encrypted_message, sk)
print("Mensagem recuperada: ")
print(decrypted_message)
