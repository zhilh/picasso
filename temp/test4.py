# -*- coding: utf-8 -*-

from itertools import permutations


str ='asdfctkymj'
a=list(permutations(str,3))
#print(a)
L = [i for i in permutations(str,3) if not ''.join(i).startswith('a') and not ''.join(i).endswith('j')]
#print(L)

rt=[]
for i in list(permutations(str,3)):
    if not ''.join(i).startswith('a') and not ''.join(i).endswith('j'):
        rt.append(list(i))
print(len(rt))