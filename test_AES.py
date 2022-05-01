from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import binascii
import AES as local_AES

#inputs
plaintext = 'Sample Text'
key = "CHAVE_AES_CTR128"
key_bin = b"CHAVE_AES_CTR128"

print("Mensagem: ", plaintext)
print("Chave: ", key)

#Encryption
def _encrypt(plaintext):
    data_bytes = bytes(plaintext, 'utf-8')
    AES_obj = AES.new(key_bin, AES.MODE_CTR)
    ciphertext = AES_obj.encrypt(data_bytes)
    return ciphertext, AES_obj.nonce

ciphertext, nonce = _encrypt(plaintext)
print("Biblioteca Crypto:")
print(binascii.hexlify(ciphertext))

ciphertext2 = local_AES.CTRmode(plaintext, key)
print("Nossa implementação:")
for i in range(len(ciphertext2)):
    print(hex(ord(ciphertext2[i]))[2:], end = '')

#Decryption
# def _decrypt(ciphertext, nonce):
#     AES_obj = AES.new(key, AES.MODE_CTR, nonce = nonce)
#     raw_bytes = AES_obj.decrypt(ciphertext)
#     return raw_bytes

# plaintext = _decrypt(ciphertext, nonce)
# print(plaintext)
# print(plaintext.decode('ascii'))
