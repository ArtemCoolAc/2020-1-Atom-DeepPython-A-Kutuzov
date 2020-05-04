def i_hate_it(In):
    pref = [1]*(len(In)+1)
    for i in range(1, len(In)+1):
        pref[i] = pref[i-1]*In[i-1]
    suf = [1]*(len(In)+1)
    for i in range(len(In)-1, -1,-1):
        suf[i] = suf[i+1] * In[i]
    res = [1]*(len(In))
    for i in range(1,len(In)+1):
        res[i-1] = pref[i-1]*suf[i]
    return res


def i_dont_know(a):
    product = 1
    l = len(a)
    result = []
    for i in range(l):
        result.append(product)
        product = product * a[i]
    product = 1
    for i in range(l-1, -1,-1):
        result[i] = result[i] * product
        product = product * a[i]
    return result
