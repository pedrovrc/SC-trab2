from importlib.resources import read_binary
import miller_rabin as MR

# Geracao de chaves publica e privada
PK = MR.getPrimeCandidate(MR.KEY_LEN)
while(not(MR.isPrime(PK))):
    PK = MR.getPrimeCandidate(MR.KEY_LEN)

SK = MR.getPrimeCandidate(MR.KEY_LEN)
while(not(MR.isPrime(SK))):
    SK = MR.getPrimeCandidate(MR.KEY_LEN)

print(PK)
print(SK)