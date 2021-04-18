# brute force
def bruteForce(out, max, arr, length):
    # global m1, m2, matrix
    for i in range(max):
        if length>0:
            temp = list(arr)
            temp.append(i)
            bruteForce(out, max, temp,length-1)
        else:
            if not arr in out:
                out.append(arr)
                #print(arr)
            # if len(out)==(max-1)**length:
            #     print(out)
    return out

print(bruteForce([], 5, [], 4))
