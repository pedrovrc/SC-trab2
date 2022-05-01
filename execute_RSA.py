
import RSA

pk, sk = RSA.generateKeys()

print("Insira a mensagem:")
message = input()
print("Tamanho da mensagem inserida:", len(message))

encrypted_message = RSA.encrypt(message, pk)
print("Mensagem criptografada: ")
print(encrypted_message)

decrypted_message = RSA.decrypt(encrypted_message, sk)
print("Mensagem recuperada: ")
print(decrypted_message)
print("Tamanho da mensagem recuperada:", len(decrypted_message))
