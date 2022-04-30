def generateList(N):
    prime_list = [x for x in range(2, N)]
    p = prime_list[0]
    index = 0
    while(p < N):
        for i in range(2, N):
            if (p * i >= N):
                break
            elif p * i in prime_list:
                prime_list.remove(p * i)
        
        index += 1
        if index >= len(prime_list):
            break
        else:
            p = prime_list[index]
    return prime_list
    