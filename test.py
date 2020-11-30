# A Python program to print all  
# combinations of given length 
from itertools import combinations 
  
# Get all combinations of [1, 2, 3] 
# and length 2 
lst = [(2, 0), (2, 2), (1, 2)]
comb = combinations(lst, 2) 
  
# Print the obtained combinations 
for i in list(comb): 
  print (list((set(lst)-set(i)))[0])
  print (list(i)) 