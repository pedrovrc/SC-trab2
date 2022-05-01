# Este modulo deve ser utilizado para testar isoladamente as funcionalidades do moodulo "miller-rabin.py".

import miller_rabin as MR

length = 16
P = MR.getPrimeCandidate(length)
while(not(MR.isPrime(P))):
    P = MR.getPrimeCandidate(length)

Q = MR.getPrimeCandidate(length)
while(not(MR.isPrime(Q))):
    Q = MR.getPrimeCandidate(length)

print(P)
print(Q)